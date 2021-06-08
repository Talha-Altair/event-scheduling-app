from flask import Flask,render_template, jsonify, request, url_for
import random
import json
import pymongo
from pymongo import MongoClient
from bson import json_util
from flask import Markup
import datetime 
from datetime import date




cluster = MongoClient('mongodb+srv://aswin:aswin@cluster0.g8od0.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')

db = cluster["event-calendar"]
col = db["events"]

app  = Flask(__name__)

def get_week_num(date):
    year,week_num,day_of_week = date.isocalendar()

    return week_num


@app.route("/", methods=["GET","POST"])
def startpy():

    return render_template("index.html")



@app.route("/submit", methods=["GET","POST"])
def submit():
    name  = request.form.get("feature-title")
    date  = request.form.get("date")
    time  = request.form.get("time")
    day = datetime.datetime.strptime(date,'%Y-%m-%d')
    week_num = get_week_num(day)
    # print(date)
    day_name= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
    day = datetime.datetime.strptime(date,'%Y-%m-%d').weekday()
    # print(day)
    # print(day_name[day]) 
    final_day = day_name[day]

    query = { "Name": name , "Date": date ,"Time": time,"day":final_day,"week_num":week_num}
    col.insert_one(query)
    for x in col.find(query):

        val=x['Name']
        val2=x['Date']
        val3=x["day"]
        val4=x['Time']
        val5=x['week_num']

    result = {
        'Name' : val ,
        'Date' : val2 ,
        'day'  : val3,
        'Time' : val4,
        'week_num':val5
    }  

    # print(result)
    
    return render_template('result.html', result = result)


@app.route("/details", methods=["GET","POST"])
def details():
    today = date.today()
    current_week_num = get_week_num(today)
    print(current_week_num)
    day   = request.form.get("day")  
    mydata=[]
    days=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    index = days.index(day)
    myquery={}

    for x in range(index+1):
        
        myquery = { "$and": [ {"day" : days[x]} , {"week_num":current_week_num} ] }

        for mydoc in col.find(myquery):
            #  print(mydoc)
            mydata.append(mydoc)

    return render_template('find.html', data=mydata)



if __name__ == "__main__":
    app.run(debug = True,host="0.0.0.0")