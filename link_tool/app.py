from flask import Flask, render_template,flash, redirect,url_for,session,logging,request
import pymongo
from urllib.parse import urlparse
import urllib
from sel_script import sel_get
from scrape import GetProfile
from bson import ObjectId
from register import Register_User
from update import Update_Profile_Picture, Update_Story_Info, Update_Headline_Info, Update_Experience_Info, Update_Education_Info, Update_Language_Info, Update_Accomplishments_Info, Update_Interests_Info

from sales import Get_Sales_Data
from sales_scrape import Sales_GetProfile
from sales_update import Sales_Update_Profile_Picture, Sales_Update_Story_Info, Sales_Update_Headline_Info, Sales_Update_Experience_Info, Sales_Update_Education_Info, Sales_Update_Language_Info, Sales_Update_Accomplishments_Info, Sales_Update_Interests_Info


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["linkedin"]
users = mydb["users"]

app = Flask(__name__)



@app.route("/")
def index():
    return render_template("index.html")


@app.route("/import_profile", methods=["GET", "POST"])
def import_profile():
    if request.method == "POST":
        link = request.form["linkedin_link"]
        sel_get(link)
        data = GetProfile()
        _id = users.insert(data)
        return redirect(url_for("imported_profile", _id=_id))
    return render_template("import_profile.html")


@app.route('/imported_profile', methods=['GET', 'POST'])
def imported_profile():
    if request.method == "POST":
        _id = request.form.get("_id")
        username = request.form.get('uname')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        b_day = request.form.get('bdate').split("/")[0]
        b_day = int(b_day)
        b_month = request.form.get('bdate').split("/")[1]
        b_year = request.form.get('bdate').split("/")[2]
        gender = request.form.get('gender')
        gender = gender.lower()
        
        additional = {
            "username" : username,
            "email" : email,
            "phone" : phone,
            "password" : password,
            "b_day" : b_day,
            "b_month" : b_month,
            "b_year" : b_year,
            "gender" : gender,
            "registered" : False
        }

        print(additional)
        users.update_one({"_id" : ObjectId(_id)}, {"$set" : additional})
        # Register User
        Register_User(_id)

        # Update Profile Pciutre
        Update_Profile_Picture(_id)

        # Update Story Info
        Update_Story_Info(_id)

        # Update Headline Info
        Update_Headline_Info(_id)

        # Update Interests Info
        Update_Interests_Info(_id)

        # Update Accomplishments Info
        Update_Accomplishments_Info(_id)

        # Update Language Info
        Update_Language_Info(_id)

        # Update Education Info
        Update_Education_Info(_id)

        # Update Experience Info
        Update_Experience_Info(_id)

        return redirect(url_for("success"))
    _id = request.args.get('_id')
    data = users.find_one({"_id" : ObjectId(_id)})
    return render_template("imported_profile.html", data=data)


@app.route('/success', methods=['GET', 'POST'])
def success():
    if request.method == "POST":
       print("GOOD JOB")
    return render_template("success.html")


@app.route('/registered', methods=['GET', 'POST'])
def registered():
    if request.method == "POST":
       print("Why did you send this method?")
    data = []
    _all = users.find({"registered" : True})
    for each in _all:
        data.append(each)
    return render_template("registered.html", data=data)


@app.route('/delete_user/<_id>')
def delete_user(_id):
    print(_id)
    users.update_one({"_id" : ObjectId(_id)}, {"$set" : {"registered" : False } })
    return redirect(url_for('registered'))


@app.route('/sales', methods=['GET', 'POST'])
def sales():
    if request.method == "POST":
        print("I'll handle the post request later")
    data = Get_Sales_Data()
    return render_template("sales.html", data=data)


@app.route('/sales_update', methods=['POST'])
def sales_update():
    link = request.form.get('linkedin_link')
    _id = request.form.get("_id")
    sel_get(link)
    
    # Update sales Database and Profile Info
    Sales_GetProfile(_id)

    Sales_Update_Profile_Picture(_id)

    Sales_Update_Story_Info(_id)

    Sales_Update_Headline_Info(_id)

    Sales_Update_Experience_Info(_id)

    Sales_Update_Education_Info(_id)

    Sales_Update_Language_Info(_id)

    Sales_Update_Accomplishments_Info(_id)

    Sales_Update_Interests_Info(_id)

    return redirect(url_for('success'))