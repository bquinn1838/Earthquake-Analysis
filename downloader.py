import sys
from pymongo import MongoClient
#connect to MongoDB cluster
client = MongoClient("mongodb+srv://m001-Brian-Quinn:m001-mongodb-basics@m001-pbvpm.mongodb.net/test?retryWrites=true&w=majority")

import time
import json
import urllib.request, urllib.parse, urllib.error
from datetime import datetime
def last_earthquake_time(earthquakes, endtime):
    last_earthquake = earthquakes.find_one(sort=[("properties.time", 1)])
    if last_earthquake is not None:
        ts = int(last_earthquake["properties"]["time"])/1000
        endtime = datetime.utcfromtimestamp(ts).isoformat()
    return endtime

#initial settings that control the data download
earthquakeURL = "https://earthquake.usgs.gov/fdsnws/event/1/query?"
paramD = dict()
paramD["format"] = "geojson" #data format
paramD["starttime"] = "2010-01-01T00:00:00" #starting 01/01/2010
paramD["endtime"] = "2019-12-31T23:59:59" #ending 12/31/2019
paramD["minmag"] = 6 #minimum magnitude of 6
paramD["limit"] = 1000 #maximum number of quakes to return

#connect to mongodb database earthquakesdb and collection earthquakes
db = client["earthquakesdb"]
earthquakes = db.earthquakes

#checks to see if we are restarting the download
#if earthquake data eissts, reset endtime to be date of earliest earthquake

paramD["endtime"] = last_earthquake_time(earthquakes, paramD["endtime"])

#begin the download of new data, count the number of earthquakes downloaded
count = paramD["limit"]
while count >= paramD["limit"]:
    #create a URL based on base URL plus parameters
    params = urllib.parse.urlencode(paramD)
    print(earthquakeURL+params)

    try:
        #open the URL using urllib library
        document = urllib.request.urlopen(earthquakeURL+params)
        #get all text from document
        text = document.read().decode()

        if document.getcode() != 200 :
            print("Error code=",document.getcode(),erathquakeURL+params)
            break
    except KeyboardInterrupt:
        print('')
        print("Program interupted by user...")
        break
    except: 
        print("Unable to retrieve or parse page",earthquakeURL+params)
        print(sys.exc_info()[0])
        break

#load the JSON terxt from the URL into a dict using the JSON library
js = json.loads(text)

#get the number of earthquakes downloaded in this file
#if count < limit the loop will terminate after this iteration
count = int(js["metadata"]["count"])
print(count)
if count > 0 :
    new_earthquakes = earthquakes.insert_many(js["features"])

paramD["endtime"] = last_earthquake_time(earthquakes, paramD["endtime"])
time.sleep(2)
print("done")