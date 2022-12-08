# topic coverd 
# list iterators
# logical statements
# regix exp
# logic building
import re
from validated_data import validate_data
from data_set import data_set

FULL_NAME_AMOUNT_DATA = []
NOT_MATCHED_DATA = []
ONLY_AMOUNT_DATA = []

index = 0
def find_entire_item(data, customer, amount):
        return list(filter(lambda x: customer == x.get('customer') and x.get('amount') == amount, data))

def match_combination(data_set, validate_data):
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

match_combination(data_set, validate_data)


print('=+=+=+=+==================********TOTAL BANK DATA********==================+=+=+=+=')
print(len(data_set))
print('=+=+=+=+==================********TOTAL AUDIT DATA********==================+=+=+=+=')
print(len(validate_data))

print('==**********************************************==')
print('NOT_MATCHED_DATA', len(NOT_MATCHED_DATA))
print('-----------------------------------------')
print('FULL_NAME_AMOUNT_DATA', FULL_NAME_AMOUNT_DATA)
