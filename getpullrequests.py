import git,datetime,re,os


from git import *

toCheck=os.getcwd()
os.chdir('..')
repo = Repo(toCheck)
pr="Merge pull request #"
cutoff=int((datetime.datetime.now()-datetime.timedelta(days=7)).strftime('%s')); 
assert repo.bare == False
for c in repo.iter_commits('master', max_count=500): #todo make these not magic numbers
	if((c.committed_date>cutoff)and c.message.startswith(pr)):
		print re.search("\d+",c.message).group(0);
	