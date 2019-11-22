import git
import os
import json
import datetime

class Record ():
	def __init__ (self,user,date,text,nicknames):
		self.user = user
		self.nickname = nicknames[user]
		self.date = datetime.datetime.fromtimestamp(date)
		self.text = text

	def GetTrendsetterLog (self):
		string = self.date.strftime("%m/%d/%y %H:%M | ") + self.nickname + ": " + self.text + "\n"
		return string

repo = git.Repo(".")

def add_to_cache (user):
	with open ("cache/usercache.txt","a") as cachefile:
		cachefile.write("\n" + user + " 0")

def add_to_nickname (user):

	with open ("nicknames.json","r") as nickfile:
		nicknames = json.load(nickfile)

	nicknames[user] = user

	with open ("nicknames.json","w") as nickfile:
		json.dump(nicknames,nickfile)

	return nicknames

def get_users (readlines):
	users = []
	for i in readlines: 
		if i != "": users.append(i)
	return users

def init ():
	print ("Initiating User ...")

	with open ("system/users.txt","r") as usersfile:
		users = get_users(usersfile.read().split("\n"))
		user = str(int(users[-1]) + 1)
		users.append(user)

	print ("User's name is",user)

	with open ("system/users.txt","a") as usersfile:
		usersfile.write("\n" + user)

	add_to_cache(user)

	print ("User's name added to register")

	nicknames = add_to_nickname(user)

	print ("User's nickname is registered as", nicknames[user])
	repo.git.add("system/users.txt")

	with open ("system/self.txt","w") as self_file:
		self_file.write(user)

	return (user, users, nicknames)


if not os.path.isfile("system/self.txt"):
	user_self, users, nicknames = init()
else:
	with open ("system/self.txt","r") as self_file:
		user_self = self_file.read()

	with open ("system/users.txt","r") as users_file:
		users = get_users(users_file.read().split("\n"))

	with open ("nicknames.json","r") as nickfile:
		nicknames = json.load(nickfile)

def commit (line):
	repo.git.add("cache/"+user_self)
	repo.git.commit(m = line)
	print("Committed, ", end = "")

def push ():
	repo.git.push()
	print("Pushed")

def pull ():
	repo.git.pull()
	print("Pulled, ", end = "")

def get_recs (user, ts):
	if not os.path.isfile("cache/"+user):
		with open("cache/"+user,"w") as cachefile: pass

	with open("cache/"+user,"r") as cachefile:
		lines = []
		for i in cachefile.read().split("\n"): 
			if i != "": lines.append(i)

	recs = []
	i = len(lines) - 1
	
	if len(lines) > 0:
		line = lines[i].split("|")
		timestamp = line[0]
	else:
		timestamp = str(datetime.datetime.now().timestamp())

	while i >= 0 and float(line[0]) > ts:
		recs.append(Record(user,float(line[0]),line[1],nicknames))
		i -= 1
		if i >= 0: line = lines[i].split("|")

	return (timestamp, recs)

def update_cache (user, timestamp):

	with open ("cache/usercache.txt","r") as cachefile:
		lines = cachefile.read().split("\n")

	for i in range(len(lines)):
		if lines[i].split(" ")[0] == user:

			text = "\n".join(lines[:i])
			if len(lines[:i]) > 0: text += "\n"
			text += user + " " + str(timestamp)
			if len(lines[i+1:]) > 0: text += "\n"
			text += "\n".join(lines[i+1:])
			break

	with open ("cache/usercache.txt","w") as cachefile:
		cachefile.write(text)

def update (line=None,topush=False):
	global nicknames
	if topush: commit(str(line))
	pull()
	if topush: push()

	caches = []

	if not os.path.isfile("cache/usercache.txt"):
		for u in users: add_to_cache(u)

	with open("cache/usercache.txt","r") as f:
		for line in f.read().split("\n"): 
			if line != "": caches.append(tuple(line.split(" ")))

	u_ts = []
	all_logs = []
	for user in users:
		logs = []
		found = False
		if user not in nicknames.keys(): nicknames = add_to_nickname(user)

		for u,ts in caches:
			ts = float(ts)
			if u == user:
				timestamp, logs = get_recs(u,ts)
				found = True

		if not found:
			add_to_cache(user)
			timestamp, logs = get_recs(user,"0")

		update_cache(user,timestamp)
		all_logs += logs

	all_logs.sort(key=lambda x: x.date)

	with open ("main.log","a") as trendsetterlog:
		for rec in all_logs:
			trendsetterlog.write(rec.GetTrendsetterLog())

	print("Updated Log")

def write (user,message):
	now = str(datetime.datetime.now().timestamp())
	line = now + "|" + message.replace("|","/")
	with open("cache/" + user,"a") as tmp_file:
		tmp_file.write(line + "\n")
	print("Written Locally")
	update(line,True)

print ("\nAlways enter quit to quit")
print ("Press enter to reload the log file\n")
update()

while True:
	print("?: ", end = "")
	x = input()
	if x != "quit" and x != "":
		write(user_self,x)
	elif x != "":
		break
	else:
		update()
