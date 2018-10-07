import json
import os
import random
import string

from flask import flash, Flask, redirect, render_template, request, send_file, session
from flask_wtf import FlaskForm
from wtforms import *

# Call this to generate a secure key.
def gen_secure():
	s = os.urandom(16)
	return s

app = Flask(__name__)
app.config['SECRET_KEY'] = "qhjkzmalqertzmalqpdfgmal"  # Don't use this in a production env...
app.config['DEBUG'] = True
def file_name():
	return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))


class DeleteForm(FlaskForm):
	filedir = HiddenField("fildir")
	deletefile = SubmitField("Delete")

@app.route('/', methods = ['GET', 'POST'])
def page_main():
	delform = DeleteForm(request.form)
	if request.method == 'POST':
		users = json.loads(open("users.json", "r").read())
		data = request.form
      
		if ("deletefile" in data) and (data["deletefile"]) and ("filedir" in data):
			try:
				os.remove(data["filedir"])
				flash("File Deleted!")
			except:
				pass
				
		else:
			try:
				if not "username" in data:
					return "You didn't provide a username"
					
				if not data["username"] in users:
					return "You don't have an account"
					
				if not "key" in data:
					return "You didn't provide a key"
					 
				if data["key"] != users[data["username"]]:
					return "Your key is incorrect"
						
				if not os.path.exists("./files/"+data["username"]):
					return "You're out of space"
						   
				os.makedirs("./files/"+data["username"])
				if sum([sum(map(lambda fname: os.path.getsize(os.path.join(directory, fname)), files)) for directory, folders, files in os.walk("/filehost/files/" + data["username"] )]) / (1024*1024.0) < 500:
					name = file_name()
					upfile = request.files
					filename, extension = os.path.splitext(upfile["file"].filename)
					upfile["file"].save("/filehost/files/"+data["username"]+"/"+ name+extension)
					return "http://stop-storing-your-config-in-ya.ml/"+data["username"]+"/"+name+extension
			except:
				return "Unknown Error"
		
	session["username"] = "qwerty"
	files = [{"name": i, "size": round(os.path.getsize("/filehost/files/"+session["username"]+"/"+i)/1024.0, 2)} for i in os.listdir("/filehost/files/qwerty")]
	return render_template("mainpage.html", files=files, form=delform, spaceused=round(sum([sum(map(lambda fname: os.path.getsize(os.path.join(directory, fname)), files)) for directory, folders, files in os.walk("/filehost/files/" + session["username"] )])/(1024*1024.0), 2))




@app.route('/<string:username>/<string:fileid>')
def page_set(username, fileid):
	return send_file("/filehost/files/"+username+"/"+fileid)

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=80)
