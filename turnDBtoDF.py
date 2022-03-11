#!/usr/bin/python3
  
import numpy as np
import pandas as pd
import sqlite3 as sql

filepath = 'database.db'
con = sql.connect(filepath)
df = pd.read_sql('Select * from beers;', con)
def turnDBintoDF():
    print("Here is a dataframe of the databasae\n", df)

if __name__ == "__main__":
    turnDBintoDF()
