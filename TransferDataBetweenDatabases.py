import xmlrpc.client

# LIFELINE DATABASE CONNECTION
url = "http://127.0.0.1:8069"
db = "lifeline"
username = "demouser"
password = "demouser"

check_odoo_version_lifeline = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
connect_to_odoo_to_read_data_lifeline = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
uid_lifeline = check_odoo_version_lifeline.authenticate(db, username, password, {})

# PRACTICE DATABASE CONNECTION
url_2 = "http://127.0.0.1:8000"
db_2 = "practice"
username_2 = "demouser"
password_2 = "demouser"

check_odoo_version_practice = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url_2))
connect_to_odoo_to_read_data_practice = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url_2))
uid_practice = check_odoo_version_practice.authenticate(db_2, username_2, password_2, {})

# INSERT INVOICE DATA FROM LIFELINE TO PRACTICE
invoice_data_lifeline = connect_to_odoo_to_read_data_lifeline.execute_kw(db, uid_lifeline, password, 'account.invoice',
                                                                         'search_read', [[]],
                                                                         {'fields': ['name', 'origin', 'amount_total', 'amount_untaxed', 'amount_untaxed_signed',
                                                                                     'amount_tax', 'amount_total_signed', 'amount_total_company_signed', 'display_name']})
total_count = 0
for invoice in invoice_data_lifeline:
    print("INVOICE : ", invoice)
    total_count += 1
    insert_into_practice_database = connect_to_odoo_to_read_data_practice.execute_kw(db_2, uid_practice, password_2,
                                                                                     'account.invoice', 'create',
                                                                                     [invoice])
print("Total Created : ", total_count)
