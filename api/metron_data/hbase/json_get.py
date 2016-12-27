from api.metron_data.hbase.common import *
import json, base64, requests

# Get the bleats
request = requests.get(hbaseBaseURL + "/" + hbaseTableName + "/" + hbaseSiteName, headers={"Accept" : "application/json"})

if issuccessful(request) == False:
	print("Could not get messages from HBase. Text was:\n" + request.text)
	quit()

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
		