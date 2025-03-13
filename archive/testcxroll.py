from utility.cx_zero import cx_zero

switch_user='admin'
switch_password = 'admin'

db ='me'

response = cx_zero(switch_user, switch_password, db)

print(response)
