# topic coverd 
# list iterators
# logical statements
# regix exp
# logic building
import re

data_set = [
     {'user_id': None, 'customer': 'Money Received From SYEDA YUMNA HAIDER ZAIDI-HMB 6990429308714266298 STAN(868049)', 'amount': 5600.0, 'date': '2022-12-06'},
     {'user_id': None, 'customer': 'Money Received From SOHAIB AKHTAR-HBL 01350077224001 STAN(135573)', 'amount': 22100.0, 'date': '2022-12-07'},
     {'user_id': None, 'customer': 'Money Transferred To FAHAD FIAZ A/C 1258-0105457069 STAN (606148)', 'amount': 17693.0, 'date': '2022-12-08'},
     {'user_id': None, 'customer': 'Money Received From NADIR WAQAR A/C 0188-0101301012 STAN (613581)', 'amount': 11100.0, 'date': '2022-12-09'},
     {'user_id': None, 'customer': 'Money Transferred To MUHAMMAD UMAIR-ABL 0665001007012677001 STAN(175776)', 'amount': 111000.0, 'date': '2022-12-06'},
     {'user_id': None, 'customer': 'Money Transferred To MOHAMMAD ADNAN BUTT-ABL 0555001003454540002 STAN(193420)', 'amount': 13213.0, 'date': '2022-12-06'},
     {'user_id': None, 'customer': 'Money Received From M BILAL UMAR-HBL 14087900970903 STAN(109979)', 'amount': 8500.0, 'date': '2022-12-06'},
     {'user_id': None, 'customer': 'Money Transferred To MUHAMMAD UMAIR-ABL 0665001007012677001 STAN(175776)', 'amount': 151850.0, 'date': '2022-12-06'},
     {'user_id': None, 'customer': 'Money Received From FAZEEL AHMED-UBL 1921280800839 STAN(527078)', 'amount': 22500.0, 'date': '2022-12-06'},
     {'user_id': None, 'customer': 'Money Transferred To MUHAMMAD UMAIR-ABL 0665001007012677001 STAN(175776)', 'amount': 151850.0, 'date': '2022-12-06'}
]
    
validate_data = [
     {'user_id': 16522704, 'customer': 'Syeda Tazeen Zahra Naqvi', 'amount': 110500.0, 'date': '2022-12-06'},
     {'user_id': 16522555, 'customer': 'Sohaib Akhtar', 'amount': 22100.0, 'date': '2022-12-06'},
     {'user_id': 16522548, 'customer': 'Fiaz Ahmed', 'amount': 12000.0, 'date': '2022-12-06'},
     {'user_id': 16522408, 'customer': 'nadir waqar', 'amount': 11100.0, 'date': '2022-12-06'},
     {'user_id': 16522399, 'customer': 'Muhammad Rehman', 'amount': 111000.0, 'date': '2022-12-06'},
     {'user_id': 16522369, 'customer': 'Mohammad Arslan saeed', 'amount': 25000.0, 'date': '2022-12-06'},
     {'user_id': 16522302, 'customer': 'Umar Farooq', 'amount': 3500.0, 'date': '2022-12-06'},
     {'user_id': 16522203, 'customer': 'Muhammad Adnan', 'amount': 57000.0, 'date': '2022-12-06'},
     {'user_id': 16522031, 'customer': 'Fazeel Ahmed', 'amount': 22500.0, 'date': '2022-12-06'},
     {'user_id': 16522005, 'customer': 'Muhammad Nisar', 'amount': 6500.0, 'date': '2022-12-06'}
 ]






ONLY_ONE_AMOUNT_DATA = []

FULL_NAME_AMOUNT_DATA = []

NOT_MATCHED_DATA = []

ONLY_AMOUNT_DATA = []


index = 0
def find_entire_item(data, key, allowed):
        return list(filter(lambda x: key in x and x[key] in allowed, data))

def match_combination(data_set, validate_data):
     for bank in data_set:
          matched = find_entire_item(validate_data, 'amount', (bank.get('amount'),))
          if len(matched):
               user_id = matched[0].get('user_id')
               bank['user_id'] = user_id
               ONLY_AMOUNT_DATA.append(bank)
          else:
               NOT_MATCHED_DATA.append(bank)
          
     status = [NOT_MATCHED_DATA, ONLY_ONE_AMOUNT_DATA, FULL_NAME_AMOUNT_DATA]

     for only_amount_mahched in ONLY_AMOUNT_DATA:     
          name = str(only_amount_mahched.get('customer')).lower()
          name_cleaned = re.split('[-()]|a/c|from|to', name)
          splitted_names = ''
          if len(name_cleaned)>1:
               splitted_names = str(name_cleaned[1].strip()).split(" ")

          the_matched_item = []
          user_id = only_amount_mahched.get('user_id')
          the_matched_item = find_entire_item(validate_data, 'user_id', (user_id,))
          
          if the_matched_item:
               required_names = str(the_matched_item[0].get('customer')).lower().split(' ')

               if type(splitted_names) == list:
                    index = 0
                    for names in splitted_names:
                         if names in required_names:
                              index +=1
                    status[index].append(only_amount_mahched)
        

match_combination(data_set, validate_data)

                    
print('NOT_MATCHED_DATA', len(NOT_MATCHED_DATA))
print('-----------------------------------------')
print('ONLY_ONE_AMOUNT_DATA', len(ONLY_ONE_AMOUNT_DATA))
print('-----------------------------------------')
print('FULL_NAME_AMOUNT_DATA', len(FULL_NAME_AMOUNT_DATA))
