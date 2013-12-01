import json
from restkit import Resource, BasicAuth, Connection, request
from socketpool import ConnectionPool
import sys
import git,datetime,re,os
from git import *

team=["arthur johnston"]	

def get_pullrequest_by_team(repoToCheck):
	repo = Repo(repoToCheck)
	pr="Merge pull request #"
	cutoff=int((datetime.datetime.now()-datetime.timedelta(days=21)).strftime('%s')); 
	assert repo.bare == False
	for c in repo.iter_commits('master', max_count=500): #todo make these not magic numbers
		if((c.committed_date>cutoff)and c.message.startswith(pr) and any(str(c.author)==t for t in team)):
			yield re.search("\d+",c.message).group(0);
def get_pullrequest_merges(repoToCheck):
	
	repo = Repo(repoToCheck)
	pr="Merge pull request #"
	cutoff=int((datetime.datetime.now()-datetime.timedelta(days=14)).strftime('%s')); 
	assert repo.bare == False
	for c in repo.iter_commits('master', max_count=500): #todo make these not magic numbers
		if((c.committed_date>cutoff)and c.message.startswith(pr)):
			yield re.search("\d+",c.message).group(0);

#this section is for github specific stuff
def is_pullrequest_tested(pr,token,owner,repo):	
	url='https://api.github.com/repos/'+owner+'/'+repo+'/pulls/'+pr+'/files' 
	
	resource = Resource(url, pool=pool)
	
	headers = {'Content-Type' : 'application/json' }
	headers['Authorization'] = 'token %s' % token
	response = resource.get(headers = headers)
	files = json.loads(response.body_string())
	#print 'NORMAL:', json.dumps(files, sort_keys=True,indent=2)
	for x in files:
		if 'test' in x['filename'].lower():
			return True;
	return False;

if __name__ == "__main__":
	pool = ConnectionPool(factory=Connection)
	serverurl="https://api.github.com"
	 
	user = sys.argv[1]
	password = sys.argv[2]
	auth=BasicAuth(user, password)
	#assumes you're running this script from the repo you want to check
	repo=os.path.basename(os.getcwd())
	#move a directory up, because it's required for git module and
	#you don't want to pollute yourrepo 
	os.chdir('..')
	
	# Use your basic auth to request a token
	# This is just an example from http://developer.github.com/v3/
	authreqdata = { "scopes": [ "repo" ], "note": "admin script" }
	resource = Resource('https://api.github.com/authorizations', 
	                    pool=pool, filters=[auth])
	response = resource.post(headers={ "Content-Type": "application/json" }, 
	                         payload=json.dumps(authreqdata))
	token = json.loads(response.body_string())['token']
	 
	prs=get_pullrequest_merges(repo)
	for pr in prs:
		if is_pullrequest_tested(pr,token,user,repo):
			pass;
		with open("untested_pullrequests.txt","a") as file:
			file.write("https://github.com/{}/{}/pull/{}\n".format(user,repo,pr))
		who_did_pullrequest(pr,token,user,repo)
	prs= get_pullrequest_by_team(repo)
	for pr in prs:
		with open("by_team_pullrequests.txt","a") as file:
			file.write("https://github.com/{}/{}/pull/{}\n".format(user,repo,pr))
	