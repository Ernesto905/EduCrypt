from flask import Flask, render_template, url_for, request
import json

app = Flask(__name__)

def uploadJson(json):
    print(json)

def errorhandlerSelf(data):
    errors = []
    if(data["name"] == ""):
        errors.append("Name cannot be empty")
    if(data["discord"] == ""):
        errors.append("Discord id cannot be empty")
    elif((data["discord"][-5:][0] != "#") or (data["discord"][-4:].isdigit() == False)):
        errors.append("Discord id is not valid")
    return errors

def errorhandlerGroup(data):
    errors = []
    if(data["name"] == ""):
        errors.append("Name cannot be empty")
    if(len(data["discord"]) < 1):
        errors.append("More than 1 Discord ids needed")
    for dc in data["discord"]:
        if(dc==""):
            continue
        if((data["discord"][-5:][0] != "#") or (data["discord"][-4:].isdigit())):
            errors.append("One or more of the Discord ids is/are invalid")
            break
    return errors

@app.route("/")
@app.route("/home")
def home():
    return render_template("./index.html")

@app.route("/form")
def form():
    return render_template("./form.html", load="choice")

@app.route("/register_self", methods=['POST'])
def register_self():
    if request.method == 'POST':
        data = {
            "name": request.form["name"],
            "discord": request.form["discord"],
            "interval": request.form["interval"],
            "course": request.form["course"]
        }
        errs = errorhandlerSelf(data)
        if(errs == []):
            uploadJson(json.dumps(data))
            return "<script>window.onload = window.close();</script>"
        else:
            return render_template('./form.html', load="self", errors=errs)

@app.route("/register_group", methods=['POST'])
def register_group():
    if request.method == 'POST':
        data = {
            "name": request.form["name"],
            "discord": request.form["discord"].split(';'),
            "interval-course": request.form["interval-course"],
            "interval-meet": request.form["interval-meet"],
            "course": request.form["course"]
        }
        errs = errorhandlerGroup(data)
        if(errs == []):
            uploadJson(json.dumps(data))
            return "<script>window.onload = window.close();</script>"
        else:
            return render_template('./form.html', load="group", errors=errs)

if __name__ == "__main__":
    app.run()