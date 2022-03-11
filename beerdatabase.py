#!/usr/bin/python3

import json
# read database
with open('beerdb.json') as beerdb:
    data = json.load(beerdb)

obj = json.loads(data)

print("Brewery names: " + str(obj["brewery_name"]))
