import openpyxl
import requests
import json
import os
from json2html import *
import pandas as pd

wb_obj = openpyxl.load_workbook(filename="dealroom_test.xlsx")
sheet = wb_obj.active

vendors = []

for i, row in enumerate(sheet.iter_rows(values_only=True)):
	if i != 0:
		vendors.append(str(row[0]).strip())
	
	if i == 150:
		break		

apikey = '588a931e56656752558c37c5c2bb0d83883a6dd7'
	
#for vendor in vendors:
	
#	print("Writing to " + vendor + " JSON file")
	
#	try:
#		data = {
#			"keyword": vendor,
#			"keyword_type": "name",
#			"keyword_match_type": "exact",
#			"fields": "id,name,hq_locations,industries,path",
#			"sort": "last_updated",
#			"limit":100,
#			"offset":0
#		}
	
#		headers = { 'Content-Type': 'application/json' }
		
		#r = requests.post(url='https://api.dealroom.co/api/v1/companies', data=json.dumps(data), headers=headers,auth=requests.auth.HTTPBasicAuth(apikey, ''))
		                  
		#if r.status_code >= 400:
		#	raise ValueError("Request for " + vendor + " failed")
		
		#file = open("json_outputs/" + vendor + ".json", "w")
			
		#file.write(r.text)
		
		#file.close()
		
#	except ValueError as e:
#		print(e.message)
		
failed = 0
found = 0
multiple = 0
total = 0

failed_companies = []
company_ids = []
multiple_companies = []

for file in os.listdir('json_outputs'):
	
	if "_funding" in file:
		continue
	
	total = total + 1
	filename = os.path.join('json_outputs', file)
	
	f = open(filename, 'r')
	
	data = json.load(f)
	
	if data['total'] == 0:
		failed = failed + 1
		failed_companies.append(file.replace('.json', ''))
			
	if data['total'] == 1:
		found = found + 1
		for element in data['items']:
			company_ids.append({'id': str(element['id']), 'name': element['name']})
			
	if data['total'] > 1:
		multiple = multiple + 1
		for element in data['items']:
			multiple_companies.append(element['name'])
			break
			
	f.close()

print(len(multiple_companies))	
print("Mutiple Companies Found\n ==============================")
print(multiple_companies)
print(len(failed_companies))
print("Failed Companies\n ==============================")
print(failed_companies)
df = pd.DataFrame(failed_companies)
df.to_csv('not_found.csv', index=False)
print("Success Percentage\n=============================")
print((len(company_ids))/total)
print(len(company_ids))

#for element in company_ids:
#	funding_url = 'https://api.dealroom.co/api/v1/companies/' + element['id'] + '/fundings'
	
#	headers = { 'Content-Type': 'application/json' }
	
#	try:
#		r = requests.get(url=funding_url,headers=headers,auth=requests.auth.HTTPBasicAuth(apikey, ''))
	
#		if r.status_code >= 400:
#			raise ValueError("Request for " + vendor + " failed")
		
#		print('Writing to ' + element['name'] + " funding JSON")
		
#		file = open("json_outputs/" + element['name'] + "_funding.json", "w")
			
#		file.write(r.text)
		
#		file.close()
	
#	except ValueError as e:
#		print(e.message)


merged_data = []

report = open("report.html", "a")
report.write("<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1, shrink-to-fit=no\"><link rel=\"stylesheet\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css\" integrity=\"sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm\" crossorigin=\"anonymous\"></head><body><div id=\"accordion\">")

count = 0

for element in company_ids:
	if os.path.exists('json_outputs/'+ element['name'] + '_funding.json'):
		count = count + 1
		#print('json_outputs/'+ element['name'] + '.json')
		f1 = open('json_outputs/'+ element['name'] + '.json', 'r')
		f2 = open('json_outputs/'+ element['name'] + '_funding.json', 'r')
		j1 = json.load(f1)
		j2 = json.load(f2)
		report.write("<div class=\"card\">")
		report.write("<div class=\"card-header\" id=\"heading" + element['name'] + "\">")
		report.write("<h5 class=\"mb-0\">")
		report.write("<button class=\"btn btn-link collapsed\" data-toggle=\"collapse\" data-target=\"#collapse" + element['name'] + "\" aria-expanded=\"false\" aria-controls=\"collapse" + element['name'] + "\">")
		#report.write("<h1 class=\"p-1\">" + element['name'] + "</h1>")
		report.write(element['name'])
		report.write("</button")
		report.write("</h5>")
		report.write("</div>")
		report.write("<div id=\"collapse" + element['name'] + "\" class=\"collapse\" aria-labelledby=\"heading" + element['name'] + "\" data-parent=\"#accordion\">")
		report.write("<div class=\"card-body\">")
		report.write(json2html.convert(json={'company': j1, 'funding': j2}, table_attributes="class=\"table table-condensed table-bordered table-hover\""))
		report.write("</div>")
		report.write("</div>")
		report.write("</div>")
		f1.close()
		f2.close()

report.write("</div>")
report.write("<script src=\"https://code.jquery.com/jquery-3.2.1.slim.min.js\" integrity=\"sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN\" crossorigin=\"anonymous\"></script>")
report.write("<script src=\"https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js\" integrity=\"sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q\" crossorigin=\"anonymous\"></script>")
report.write("<script src=\"https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js\" integrity=\"sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl\" crossorigin=\"anonymous\"></script>")
report.write("</body>")
report.close()
print("HTML report ready")
print(count)



