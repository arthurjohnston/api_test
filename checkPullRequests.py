import json
from restkit import Resource, BasicAuth, Connection, request
from socketpool import ConnectionPool
import sys
def IsPullRequestTested(pr,token,owner):	
	resource = Resource('https://api.github.com/repos/'+owner+'/api_test/pulls/'+pr+'/files', pool=pool)
	
	headers = {'Content-Type' : 'application/json' }
	headers['Authorization'] = 'token %s' % token
	response = resource.get(headers = headers)
	files = json.loads(response.body_string())
	#print 'NORMAL:', json.dumps(files, sort_keys=True,indent=2)
	for x in files:
		if'test' in x['filename'].lower():
			return True;
	return False;

pool = ConnectionPool(factory=Connection)
serverurl="https://api.github.com"
 
user = sys.argv[1]
password = sys.argv[2]
auth=BasicAuth(user, password)
 
# Use your basic auth to request a token
# This is just an example from http://developer.github.com/v3/
authreqdata = { "scopes": [ "repo" ], "note": "admin script" }
resource = Resource('https://api.github.com/authorizations', 
                    pool=pool, filters=[auth])
response = resource.post(headers={ "Content-Type": "application/json" }, 
                         payload=json.dumps(authreqdata))
token = json.loads(response.body_string())['token']
 
prs=['1','2','5']
for pr in prs:
	print IsPullRequestTested(pr,token,user);

