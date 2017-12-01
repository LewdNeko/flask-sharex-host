from flask import Flask, render_template, redirect, session, request, send_file
import json
import string
import random
import os
from wtforms import *

app = Flask(__name__)
app.config['SECRET_KEY'] = "qhjkzmalqertzmalqpdfgmal"
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
      
      if "deletefile" in data:
         if data.deletefile:
            if "filedir" in data:
               try:
                  os.remove(data.filedir)
               except:
                  pass
      
      try:
         if "username" in data:
            if data["username"] in users:
               if "key" in data:
                  if data["key"] == users[data["username"]]:
                     if not os.path.exists("./files/"+data["username"]):
                        os.makedirs("./files/"+data["username"])
                     if sum([sum(map(lambda fname: os.path.getsize(os.path.join(directory, fname)), files)) for directory, folders, files in os.walk("/filehost/files/" + data["username"] )]) / (1024*1024.0) < 500:
                        name = file_name()
                        upfile = request.files
                        filename, extension = os.path.splitext(upfile["file"].filename)
                        upfile["file"].save("/filehost/files/"+data["username"]+"/"+ name+extension)
                        return "http://stop-storing-your-config-in-ya.ml/"+data["username"]+"/"+name+extension

                     else:
                        return "You're out of space"
                  else:
                     return "Your key is incorrect"
               else:
                  return "You didn't provide a key"
            else:
               return "You don't have an account"
         else:
            return "You didn't provide a username"
      except:
         return "Unknown Error"
   session["username"] = "qwerty"
   files = [{"name": i, "size": round(os.path.getsize("/filehost/files/"+session["username"]+"/"+i)/1024.0, 2)} for i in os.listdir("/filehost/files/qwerty")]
   return render_template("mainpage.html", files=files, form=delform)
                  



@app.route('/<string:username>/<string:fileid>')
def page_set(username, fileid):
    return send_file("/filehost/files/"+username+"/"+fileid)

if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0", port=80)
