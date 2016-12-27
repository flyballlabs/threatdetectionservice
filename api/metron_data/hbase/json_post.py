from api.metron_data.hbase.common import *
import json, base64, requests, os, os.path
from collections import OrderedDict

# Delete table if it exists
#request = requests.get(hbaseBaseURL + "/" + hbaseTableName + "/" + hbaseSiteName, headers={"Accept" : "application/json"})

#if issuccessful(request):
#	request = requests.get(hbaseBaseURL + "/" + hbaseTableName + "/" + hbaseSiteName, headers={"Accept" : "application/json"})
#
#	if issuccessful(request):
#		print("Deleted table " + hbaseTableName)
#	else:
#		print("Errored out.  Status code was " + str(request.status_code) + "\n" + request.text)
#		
#
# Create Messages Table


bleats = json.loads(request.text)

for row in bleats['Row']:
	message = ''
	lineNumber = 0
	username = ''

	for cell in row['Cell']:
		columnname = base64.b64decode(cell['column'])
		value = cell['$']
		
		if value == None:
			continue

		if columnname == hbaseCFName + ":" + messagecolumn:
			message = base64.b64decode(value)
		elif columnname == hbaseCFName + ":" + linenumbercolumn:
			lineNumber = decode(str(value))
		elif columnname == hbaseCFName + ":" + usernamecolumn:
			username = base64.b64decode(value)

	rowKey = base64.b64decode(row['key'])

	# Output only messages whose line numbers are divisible by 10
	# and have the word again in them.
	if lineNumber % 10 == 0 and message.find("again") != -1:
		print(rowKey + ":" + str(lineNumber) + ":" + username + ":" + message);

content =   {"name":"test5", "column_families":
				[{
		            "name":"columnfam1",
		            "bloomfilter":True,
		            "time_to_live":10,
		            "in_memory":False,
		            "max_versions":2,
		            "compression":"", 
		            "max_value_length":50,
		            "block_cache_enabled":True
            	}]
			}

request = requests.post(hbaseBaseURL + "/" + hbaseTableName + "/" + hbaseSiteName, data=content, headers={"Content-Type" : "application/json", "Accept" : "application/json"})

if issuccessful(request):
	print ("Created table " + hbaseTableName)
else:
	print ("Errored out while creating table.  Status code was " + str(request.status_code) + "\n" + request.text)
	quit()


# Create a message  for every work of Shakespeare
sourceDir = "shakespeare"

for filename in os.listdir(sourceDir):
	shakespeare = open(os.path.join(sourceDir, filename), "rb")
	
	lineNumber = 0;
	
	rows = []
	jsonOutput = { "Row" : rows }
	
	for line in shakespeare:
		rowKey = username + "-" + filename + "-" + str(lineNumber).zfill(6)
		rowKeyEncoded = base64.b64encode(rowKey)
		
		line = base64.b64encode(line.strip())
		lineNumberEncoded = encode(lineNumber)
		usernameEncoded = base64.b64encode(username)
	
		cell = OrderedDict([
			("key", rowKeyEncoded),
			("Cell", 
			[
				{ "column" : messagecolumnencoded, "$" : line },
				{ "column" : usernamecolumnencoded, "$" : usernameEncoded },
				{ "column" : linenumbercolumnencoded, "$" : lineNumberEncoded },
			])
		])
		
		rows.append(cell)
		
		lineNumber = lineNumber + 1
		
	# Submit JSON to REST server
	request = requests.post(hbaseBaseURL + "/" + hbaseTableName + "/" + rowKey, data=json.dumps(jsonOutput), headers={"Content-Type" : "application/json", "Accept" : "application/json"})

	if issuccessful(request):
		print("Added messages for " + filename)
	else:
		print("Errored out while loading data.  Status code was " + str(request.status_code) + "\n" + request.text)
		quit()
