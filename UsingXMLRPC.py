import xmlrpc.client

url = "http://127.0.0.1:8069"
db = "lifeline"
username = "demouser"
password = "demouser"

check_odoo_version = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))

# Log in the system/ Authenticate to access odoo db and models
uid = check_odoo_version.authenticate(db, username, password, {})

# Connect to Odoo to read data from a model
connect_to_odoo_to_read_data = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# Return all records for a model using the search operation and whose state is invoice
return_all_lifeline_records = connect_to_odoo_to_read_data.execute_kw(db, uid, password, 'lifeline.client', 'search',
                                                                      [[['state', '=', 'invoice']]])
# Return only 10 records for a model using the search operation and whose state is invoice
return_only_10_lifeline_records = connect_to_odoo_to_read_data.execute_kw(db, uid, password, 'lifeline.client',
                                                                          'search',
                                                                          [[['state', '=', 'invoice']]], {'limit': 10})

# Count number of records for a model using the search_count operation
count_number_of_records_in_lifeline = connect_to_odoo_to_read_data.execute_kw(db, uid, password, 'lifeline.client',
                                                                              'search_count', [[]])

# Read record fields for a model using the read operation
read_record_fields_in_lifeline = connect_to_odoo_to_read_data.execute_kw(db, uid, password, 'lifeline.client',
                                                                         'read', [return_all_lifeline_records],
                                                                         {'fields': ['id', 'full_name']})

# Read record fields for a model using the read operation
search_and_read_record_fields_in_lifeline = connect_to_odoo_to_read_data.execute_kw(db, uid, password,
                                                                                    'lifeline.client',
                                                                                    'search_read', [[]],
                                                                                    {'fields': ['id', 'full_name',
                                                                                                'state']})
for record in search_and_read_record_fields_in_lifeline:
    print(record)
