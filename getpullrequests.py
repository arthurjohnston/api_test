import git,datetime,re

from git import *
repo = Repo("api_test")
pr="Merge pull request #"
cutoff=int((datetime.datetime.now()-datetime.timedelta(days=21)).strftime('%s')); 
assert repo.bare == False
for c in repo.iter_commits('master', max_count=500): #todo make these not magic numbers
	if((c.committed_date>cutoff)and c.message.startswith(pr)):
		print re.search("\d+",c.message).group(0);
	