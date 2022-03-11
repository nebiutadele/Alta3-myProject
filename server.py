#!/usr/bin/python3

# Server for Beer database 


import sqlite3 as sql

# python3 -m pip install flask
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

# return home.html 
@app.route('/')
def home():
    return render_template('home.html')

# return student.html (a way to add a student to our sqliteDB)
@app.route('/enternew')
def new_student():
    return render_template('beerform.html')

# if someone uses student.html it will generate a POST
# this post will be sent to /addrec
# where the information will be added to the sqliteDB
@app.route('/addrec',methods = ['POST'])
def addrec():
    try:
        nm = request.form['nm']                 # beer name
        style = request.form['style']           # beer style
        brewery = request.form['brewery']       # brewery name
        

        # connect to sqliteDB
        with sql.connect("database.db") as con:
            cur = con.cursor()

            # place the info from our form into the sqliteDB
            cur.execute("INSERT INTO beers (name,style,brewery) VALUES (?,?,?)",(nm,style,brewery) )
            # commit the transaction to our sqliteDB
            con.commit()
        # if we have made it this far, the record was successfully added to the DB
        msg = "Beer record was successfully added"
        
    except:
        con.rollback()  # this is the opposite of a commit()
        msg = "There was an error in adding the beer"    # we were NOT successful

    finally:
        con.close()     # successful or not, close the connection to sqliteDB
        return render_template("result.html",msg = msg)    #

# return all entries from our sqliteDB as HTML
@app.route('/list')
def list_beers():
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    
    cur = con.cursor()
    cur.execute("SELECT * from beers")           # pull all information from the table "students"
    
    rows = cur.fetchall()
    return render_template("list.html",rows = rows) # return all of the sqliteDB info as HTML

if __name__ == '__main__':
    try:
        # ensure the sqliteDB is created
        con = sql.connect('database.db')
        print("Opened database successfully")
        # ensure that the table students is ready to be written to
        con.execute('CREATE TABLE IF NOT EXISTS beers (name TEXT, style TEXT, brewery TEXT)')
        print("Table created successfully")
        con.close()
        # begin Flask Application 
        app.run(host="0.0.0.0", port=2224, debug = True)
    except:
        print("App failed on boot")

