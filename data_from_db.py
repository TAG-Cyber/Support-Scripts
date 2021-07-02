import mysql.connector
import pandas
import json

db_host = 'tag-rp-prod-db-1.cgdth7hqndrg.us-east-1.rds.amazonaws.com'

db_password = '8HHGCeogZ3ovjadekdjG'

# Vendor connections
vendor_conn = mysql.connector.connect(user='admin', password=db_password, host=db_host, port=3306, database='vendors')

portal_conn = mysql.connector.connect(user='admin', password=db_password, host=db_host, port=3306, database='portal')

cursor = vendor_conn.cursor()

print("connection cursor found")

query = ("SELECT name, website, overview, headquarters, uuid FROM vendors where deleted_at is null")

vendor_dict = {}

cursor.execute(query)

vendors_df = pandas.DataFrame(cursor.fetchall())

query = ("SELECT name, uuid FROM vendors where deleted_at is null")

cursor.execute(query)

portal_cursor = portal_conn.cursor()
category_cursor = portal_conn.cursor() 

for (name, uuid) in cursor:
	print(uuid)
	get_category_uuids = "SELECT category_uuid FROM category_vendor WHERE vendor_uuid = '{0}'".format(uuid)
	print(get_category_uuids)
	portal_cursor.execute(get_category_uuids)
	temp = []
	for (category_uuid,) in portal_cursor:
		category_query = "SELECT name FROM portal.categories where portal.categories.uuid = '{0}'".format(category_uuid)
		print(category_query)
		category_cursor.execute(category_query)
		for (name,) in category_cursor:
			temp.append(name)
		print(temp)
	vendor_dict[name] = temp

category_cursor.close()
portal_cursor.close()
cursor.close()

vendors_df.to_csv('vendors.csv')

with open("controls.json", "w") as outfile: 
    json.dump(vendor_dict, outfile)

