from flask import Flask,render_template,request,redirect,url_for
from flask_mysqldb import MySQL
import MySQLdb
db=MySQLdb.connect("localhost","root","Goodluck","pm")
mysql = MySQL()
import plotly
import random
import plotly.express as px
from collections import deque
import mysql.connector
import pandas as pd
import itertools
app=Flask(__name__)
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/form",methods=["GET","POST"])
def form():
    if request.method == 'POST':
        search=request.form['A_code']
        db=MySQLdb.connect("localhost","root","Goodluck","dbms")
        cur=db.cursor()
        query="select * from location where Area_code="+search
        cur.execute(query)
        m=cur.fetchone()
        cur.close()
    return render_template("result.html" ,m=m)
@app.route("/sendreport",methods=["GET","POST"])
def sednreport():
    if request.method=="POST":
        pd=request.form
        Area_code=pd['fname']
        Area_name=pd['lname']
        City=pd['cname']
        State=pd['sname']
        Total_waste=pd['wtot']
        db=MySQLdb.connect("localhost","root","Goodluck","pm")
        cur=db.cursor()
        cur.execute("INSERT INTO Report(Area_code,Area_name,City,State,Total_waste) VALUES(%s,%s,%s,%s,%s)",(Area_code,Area_name,City,State,Total_waste))
        db.commit()
        cur.close()
        return render_template("check.html")
@app.route('/maindata',methods=['POST','GET'])
def maindata():
	if request.method=="POST":
		yar=request.form["yr"]
		print(yar)
		yar=str(yar)
		'''conn =mysql.connector.connect(host='localhost',user='root',passwd='Alohomora123',db='WMS')
		cursor=conn.cursor()
		sql="select L.area_name,W.total_waste_generated from waste_details W,location L where W.area_code=L.area_code and W.g_year=%s "
		cursor.execute(sql,(yar,))
		desc = cursor.description
		column_names = ['States','TW','Year']
		data = [dict(zip(column_names, row))  
        for row in cursor.fetchall()]
		print(data)
		maxtstate=max(data,key=data.get)
		maxtw=data[maxstate]
		print(maxtstate)'''
		return redirect(url_for('get_data',y=yar))
@app.route('/get_data/<y>')
def get_data(y):
    conn =mysql.connector.connect(host='localhost',user='root',passwd='Goodluck',db='pm')
    cursor=conn.cursor()
    sql="select L.area_name,W.total_waste_generated from waste_details W,location L where W.area_code=L.area_code and W.year=%s"
    cursor.execute(sql,(y,))
    records=cursor.fetchall()
    print(records)
    df1=records
    df=pd.DataFrame([j for j in i] for i in df1)
    df.rename(columns={0:'Area name',1:'Total waste generated'},inplace=True)
    fig = px.pie(df, values='Total waste generated', names='Area name', title='Have an idea how much waste we generate?')
    fig.show()
    return render_template("index.html")
if __name__ == '__main__':
    app.run(debug=True)