#!/usr/bin/python3
"""RZFeeser || Alta3 Research
Tracking student inventory within a sqliteDB accessed
via Flask APIs"""

# standard library
import sqlite3 as sql

# python3 -m pip install flask
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

# return home.html (landing page)
@app.route('/')
def home():
    return render_template('home.html')



# return all entries from our sqliteDB as HTML
@app.route('/list')
def list_students():
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    
    cur = con.cursor()
    cur.execute("SELECT * from students")           # pull all information from the table "students"
    
    rows = cur.fetchall()
    return render_template("list.html",rows = rows) # return all of the sqliteDB info as HTML

if __name__ == '__main__':
    try:
        # ensure the sqliteDB is created
        con = sql.connect('database.db')
        print("Opened database successfully")
        # ensure that the table students is ready to be written to
        con.execute('CREATE TABLE IF NOT EXISTS students (name TEXT, addr TEXT, city TEXT, pin TEXT)')
        print("Table created successfully")
        con.close()
        # begin Flask Application 
        app.run(host="0.0.0.0", port=2224, debug = True)
    except:
        print("App failed on boot")

