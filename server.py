#!/usr/bin/python3

# Server for Beer database 


import sqlite3 as sql

# python3 -m pip install flask
from flask import Flask, render_template, request

app = Flask(__name__)

# landing page
@app.route('/')
def home():
    return render_template('home.html')

# return beer form
@app.route('/enternewbeer')
def new_student():
    return render_template('beerform.html')

@app.route('/addrecr',methods = ['POST'])
def addrec():
    try:
        nm = request.form['nm']                 # beer name
        style = request.form['style']           # beer style
        brewery = request.form['brewery']       # brewery name
        rating = request.form['rating']         # beer rating 
        

        # connect to sqliteDB
        with sql.connect("database.db") as con:
            cur = con.cursor()

            # place the info from our form into the sqliteDB
            cur.execute("INSERT INTO beers (name,style,brewery,rating) VALUES (?,?,?,?)",(nm,style,brewery,rating) )
            # commit the transaction to our sqliteDB
            con.commit()
        # if we have made it this far, the record was successfully added to the DB
        msg = "Beer record was successfully added"
        
    except:
        con.rollback()  # this is the opposite of a commit()
        msg = "There was an error in adding the beer"    # not successful

    finally:
        con.close()     # successful or not, close the connection to sqliteDB
        return render_template("result.html",msg = msg)

# return all entries from our sqliteDB as HTML
@app.route('/list')
def list_beers():
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    
    cur = con.cursor()
    cur.execute("SELECT * from beers")
    
    rows = cur.fetchall()
    return render_template("list.html",rows = rows) # return all of the sqliteDB info as HTML

@app.route('/remove', methods = ['DELETE'])
def remove():
    try:  # HTTP DELETE arrives at /remove?name=<name in DB to remove>

        name_to_remove = request.args.get("name") # peel off arguments and capture name to be removed

        with sql.connect("database.db") as con:
            cur = con.cursor()
            # place the info from our form into the sqliteDB
            cur.execute("DELETE FROM beers WHERE name=(?)",(name_to_remove,) )

            # commit the transaction to our sqliteDB
            con.commit()

            # if we have made it this far, the record was successfully added to the DB
            msg = "record successfully removed"

    except:
        msg = "error in removing the record"
    finally:
        return render_template("result.html",msg = msg) # return success

if __name__ == '__main__':
    try:
        # ensure the sqliteDB is created
        con = sql.connect('database.db')
        print("Opened database successfully")
        # ensure that the table students is ready to be written to
        con.execute('CREATE TABLE IF NOT EXISTS beers (name TEXT, style TEXT, brewery TEXT, rating INT)')
        print("Table created successfully")
        con.close()
        # begin Flask Application 
        app.run(host="0.0.0.0", port=2224, debug = True)
    except:
        print("App failed on boot")

