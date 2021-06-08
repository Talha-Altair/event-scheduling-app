from flask import Flask,render_template, jsonify, request, url_for
import random
import json
import pymongo
from pymongo import MongoClient
from bson import json_util
from flask import Markup


value = Markup('First line.<br>Second line.<br>')
# cluster = MongoClient('mongodb+srv://admin-Ishita:ishita@cluster0.266b1.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
cluster = MongoClient('mongodb+srv://aswin:aswin@cluster0.g8od0.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')

# db = cluster["Event_Details"]
# col = db["Event_Name"]

db = cluster["Cluster0"]
col = db["Event_Name"]

app  = Flask(__name__)
PORT = 3000


@app.route("/", methods=["GET","POST"])
def startpy():

    return render_template("index.html")


@app.route("/submit", methods=["GET","POST"])
def submit():
    name  = request.form.get("feature-title")
    date  = request.form.get("date")
    day   = request.form.get("day") 
    # print(day)
    time  = request.form.get("time")


    query = { "Name": name , "Date": date ,"Time": time, "Day": day}
    col.insert_one(query)
    for x in col.find(query):

        val=x['Name']
        val2=x['Date'] 
        val3=x['Day'] 
        val4=x['Time']

    result = {
        'Name' : val ,
        'Date' : val2 ,
        'Day'  : val3,
        'Time' : val4
    }  

    print(result)
    
    return render_template('result.html', result = result)

    
@app.route("/file", methods=["GET"])
def file():
    response=[]
    for main in col.find():
        value  = main['Name']
        value2 = main['Date']
        value3 = main['Day']
        value4 = main['Time']

        main = {
             'Name' : value ,
             'Date' : value2 ,
             'Day'  : value3,
             'Time' : value4
        }  
        response.append(main)
        # print(response)

    # return json.dumps(response) 
    return render_template('main.html', main = response)


@app.route("/find/<day>", methods=["GET"])
def find(day):
    # db = cluster["Event_Details"]
    # col = db["Name"]
    mydata=[]

    days=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    index = days.index(day)
    # print(index)
    myquery={}

    for x in range(index+1):
        myquery = {"Day" : days[x]}
    # myquery = calculate_tasks(day,days)
    # myquery = { "Day": day }
        for mydoc in col.find(myquery):
            print(mydoc)
            mydata.append(mydoc)
    # print(mydata)
    return render_template('find.html', data=mydata)

@app.route("/details", methods=["GET","POST"])
def details():
   day   = request.form.get("day")  
   mydata=[]
   days=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
   index = days.index(day)
   myquery={}

   for x in range(index+1):
        myquery = {"Day" : days[x]}

        for mydoc in col.find(myquery):
            #  print(mydoc)
             mydata.append(mydoc)

   return render_template('find.html', data=mydata)

# @app.route("/date", methods=["GET","POST"])
# def date():
#    day   = request.form.get("date")  
#    mydata=[]
#    days=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
#    index = day.index(day)
#    myquery={}

#    for x in range(index+1):
#         myquery = {"Day" : days[x]}

#         for mydoc in col.find(myquery):
#             #  print(mydoc)
#              mydata.append(mydoc)

#    return render_template('find.html', data=mydata)

# @app.route("/date", methods=["GET","POST"])
# def date():
#    date = request.form.get("date")  
#    mydata=[]
#    date=["1","2","3","4","5","6","7","8","9","0"]
#    index = date.index(date)
#    myquery={}

#    for x in range(index+1):
#         myquery = {"Date" : date[x]}

#         for mydoc in col.find(myquery):
#             #  print(mydoc)
#              mydata.append(mydoc)

#    return render_template('find.html', data=mydata)
       




   
if __name__ == "__main__":
    app.run(debug = True,host="0.0.0.0",port = PORT)