from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
import logging
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
import re
from uploadstatement.models import BankStatement, DepositRequest, WithdrawalRequest

# @login_required
def dashboard_audit(request):
    return render(request, "search_data.html")


# Create your views here.
@login_required
def uploadstatement(request):
    readSuccess = False
    audit_type = ""
    if "GET" == request.method:
        return render(request, 'uploadstatement.html')
    else:
        data_check = request.POST 
        audit_types = ["WithDrawal Requests", "Deposit Requests"]
        if data_check.get('fileType') == "2":
            messages.error(request, "Please Select Audit Type")
            return HttpResponseRedirect(reverse("uploadstatement"))
        
        try:
            auditFile = request.FILES["auditFile"]
            bankstatement = request.FILES["bankstatement"]
            if not auditFile.name.endswith('.csv') and not bankstatement.name.endswith('.csv'):
                messages.error(request,'Please provide both files in csv format')
                return HttpResponseRedirect(reverse("uploadstatement"))

            audit_type = audit_types[int(data_check.get("fileType"))]

            auditFileData = auditFile.read().decode("utf-8")
            bankFileData = bankstatement.read().decode("utf-8")
            auditFilelines = auditFileData.split("\n")
            bankFilelines = bankFileData.split("\n")
            auditDataDict = []
            bankDataDict = []
            auditHeaders = auditFilelines[0].split(",")
            bankHeaders = bankFilelines[0].split(",")

            for i in range(1, len(auditFilelines)-1):						
                auditFields = auditFilelines[i].split(",")
                collectionData = {}
                for index, head in enumerate(auditHeaders):
                    collectionData.update({
                        head: auditFields[index],
                    })
                auditDataDict.append(collectionData)

            # Bank statement
            for i in range(1, len(bankFilelines)-1):						
                bankFields = bankFilelines[i].split(",")
                collectionData = {}
                for index, head in enumerate(bankHeaders):
                    collectionData.update({
                        head: bankFields[index],
                    })
                bankDataDict.append(collectionData)
            
            readSuccess = True
            contents = {
                'status': readSuccess,
                'audit_type': audit_type,
                'auditHeaders': auditHeaders,
                'auditDataDict': auditDataDict,
                'bankHeaders': bankHeaders,
                'bankDataDict': bankDataDict,
            }
            return render(request, 'uploadstatement.html', contents)
        except Exception as ex:
            print("========================ERROR=========================")
            print(ex)
            messages.error(request, str(ex)+', please check columns must be in this format: name, amount')
            return HttpResponseRedirect(reverse("uploadstatement"))
            print("========================ERROR=========================")
    

# ==================================================================

FULL_NAME_AMOUNT_DATA = []
NOT_MATCHED_DATA = []

index = 0
def find_entire_item(data, customer, amount):
        return list(filter(lambda x: customer == x.get('customer') and x.get('amount') == amount, data))

def filter_maches(data_set, validate_data):
     for i in validate_data:
          i['customer'] = ' '.join(sorted(str(i['customer']).lower().strip().split()))

     for bank_obj in data_set:     
          name = str(bank_obj.get('customer')).lower().replace('asaan account','').replace('asaan ac','').replace('()', '').replace('asaanaccount', '')
          name_cleaned = re.split('-|a/c|from|to|pk|/', name)
          
          splitted_names = ''
          if len(name_cleaned)>1:
               splitted_names = str(name_cleaned[1]).strip().split(" ")

          splitted_names_sorted = ' '.join(sorted(splitted_names))

          matched = find_entire_item(validate_data, splitted_names_sorted, bank_obj.get('amount'))
          if len(matched):
               user_id = matched[0].get('user_id')
               bank_obj['user_id'] = user_id
               FULL_NAME_AMOUNT_DATA.append(bank_obj)
          else:
               NOT_MATCHED_DATA.append(bank_obj)
# ==================================================================


suditTypes = ["Withdrawal Requests", "Deposit Requests"]

@login_required
def search(request):
    if "GET" == request.method:
        return render(request, "search_data.html")


    searchFields = request.POST
    audit_date = searchFields.get('searchDate')
    auditType = searchFields.get("fileType")
    auditObj = WithdrawalRequest if not auditType else DepositRequest
    
    if int(auditType) == 2:
        messages.warning(request, "Please select audit type")        
        return HttpResponseRedirect(reverse("search"))

    auditData = auditObj.objects.filter(audit_date=audit_date)
    # bankStatementData, auditRequestData = match(request.POST)

    auditObj = WithdrawalRequest if auditType == '0' else DepositRequest

    auditFilterWithDate = auditObj.objects.filter(audit_date=audit_date)
    bankFilterWithDate = BankStatement.objects.filter(audit_date=audit_date)

    auditFilterWithDate_converted = list(auditFilterWithDate.values())
    bankFilterWithDate_converted = list(bankFilterWithDate.values())
    
    filter_maches(bankFilterWithDate_converted, auditFilterWithDate_converted)    
    
    # print(f"Bank Total: {len(bankFilterWithDate_converted)}, Audit Total: {len(auditFilterWithDate_converted)},\
    #  ONLY_ONE_AMOUNT_DATA: {len(ONLY_ONE_AMOUNT_DATA)}, FULL_NAME_AMOUNT_DATA: {len(FULL_NAME_AMOUNT_DATA)}, \
    #  NOT_MATCHED_DATA: {len(NOT_MATCHED_DATA)}, ONLY_AMOUNT_DATA: {len(ONLY_AMOUNT_DATA)}\
    #  ")

    print(auditFilterWithDate_converted)


    contenxt = {
        "bankStatementData": [],
        "auditRequestData": [],
        "FULL_NAME_AMOUNT_DATA": FULL_NAME_AMOUNT_DATA,
        "NOT_MATCHED_DATA": NOT_MATCHED_DATA,
        "audit_date": audit_date,
        "auditType": auditType,
        "auditTypeHeading": suditTypes[int(auditType)],
        'posted_data': request.POST
    }
    return render(request, "search_data.html", contenxt)


def formatData(item,  class_object_name, filter_columns=None, type=None):    
    filtered_data = class_object_name.objects.filter(amount__gte=(item.amount-3.0),amount__lte=(item.amount+3.0), audit_date=item.audit_date)

    # print('==================================date=============================')
    # if 'date_box' in filter_columns:
    if filter_columns.get('date_box'):
        audit_date = filter_columns.get('audit_date')
        date = datetime.strptime(audit_date, "%Y-%m-%d").date()
        before_day = filter_columns.get('days_before')
        after_day = filter_columns.get('days_after')
        before_date = date - timedelta(days=int(before_day))
        after_date = date + timedelta(days=int(after_day))
        filtered_data = filtered_data.filter(date__gte=before_date, date__lte=after_date)


    statuses = ["not matched", "parcialy matched", "fully matched", "only amount matched"] 
    status = statuses[0]
    colors = ["#fb7c7c", "#dbdb49", "#9cf576", "lightblue"] 
    color = colors[0]
    matched_id = 0
    trueIndex = 0
    splitted_names = str(item.customer).strip().split(" ")

    for find_dash in splitted_names:
        if '-' in find_dash:
            splitted_names.extend(find_dash.split('-'))
        

    for i, nms in enumerate(splitted_names):
        
        obj = filtered_data.filter(customer__icontains=nms)
        if obj:
            trueIndex +=1
            if trueIndex >=1 and trueIndex <len(statuses):
                status = statuses[trueIndex]
                color = colors[trueIndex]
                matched_id = obj.first().user_id
        else:
            if not type=="bank":
                if trueIndex > 0 and  trueIndex<len(statuses):
                    trueIndex -=1
                if trueIndex > -1:
                    status = statuses[trueIndex]
                    color = colors[trueIndex]
        if i == len(splitted_names)-1 and (filtered_data.filter(amount=item.amount).count() == 1 and status == "not matched"):
            status = "Only Amount Matched"
            color = "lightblue"
   
    return  {
                "ID": item.user_id, 
                "amount": item.amount, 
                "customar": item.customer, 
                "request_date": item.date, 
                "audit_date": item.audit_date,
                "matched_id":matched_id, 
                "status":status,
                'color': color
            }

            


def match(obj):    
    auditType = obj.get("fileType")
    audit_date = obj.get("searchDate")
    auditObj = WithdrawalRequest if auditType == '0' else DepositRequest

    auditFilterWithDate = auditObj.objects.filter(audit_date=audit_date)
    bankFilterWithDate = BankStatement.objects.filter(audit_date=audit_date)

    bankStatementData = list(map(lambda objected: formatData(objected, auditObj, obj, 'bank') ,bankFilterWithDate)) 
    auditRequestData = list(map(lambda objected: formatData(objected, BankStatement, obj, 'request'),auditFilterWithDate)) 
    
    return bankStatementData, auditRequestData



def convert_bank_statement(request):
    from datetime import datetime
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': f'attachment; filename="converted-{datetime.now()}-bank-statement.csv"'},
    )
    if request.method == "POST":
        excel_file = request.FILES["bank_statement"]
        import pandas as pd 
        
        import csv
        df=pd.read_excel(excel_file)
        df1=df.fillna (0)
        df2=df1[df1['cr']!=0]
        df2=df2.drop(['dr'], axis=1)
        df2['type']='cr'
        df3=df1[df1['dr']!=0]
        df3=df3.drop(['cr'], axis=1)
        df3['type']='dr'
        df3=df3.rename(columns={'dr':'cr'})
        df4=pd.concat([df2,df3])
        df4['date'] = df4['date'].dt.strftime("%Y-%d-%m")
        df4['audit_date'] = datetime.now().strftime("%Y-%m-%d")
        # data = df4.to_dict()
        listOfDFRows = df4.to_numpy().tolist()
        writer = csv.writer(response)
        writer.writerow(['date', 'customer', 'amount','type','audit_date'])
        for row in listOfDFRows:
            date = str(row[0]).split(' ')[0]
            row[0] = date
            
            writer.writerow(row)
        return response
        
    return render(request, 'convert_bank_statement.html')
    

