import sqlite3
from pymongo import MongoClient
#Connect to MongoDB cluster
client = MongoClient("mongodb+srv://m001-Brian-Quinn:m001-mongodb-basics@m001-pbvpm.mongodb.net/test?retryWrites=true&w=majority")

#Directional words commonly found in the data set to be removed with cleanPlace function

directions = ['Southeast', 'Southwest', 'southeast', 'southwest', 'southern', 'South', 'south']
directions += ['Notheast', 'Northwest', 'northeast', 'northwest', 'Northern', 'northern', 'North', 'north']
directions += ['Eastern', 'eastern', 'East', 'east', 'Western', 'western', 'West', 'west']
stopwords = ['Region', 'region', 'Central', 'central']

#Remove discrepencies between similar region names for data consistency
subs = {"CA": "California", "TX": "Texas", "MX" : "Mexico", "Fiji Islands": "Fiji"}

#cleanPlace function parses data and makes changes
def cleanPlace(place):
    pl = place + ""
    if(pl.find(", ") > 0):
        plist = pl.split(", ")
        pl = plist[len(plist)-1]
    elif(pl.find(" of the ") > 0):
        pl = pl.split(" of the ")[1]

    for w in stopwords :
        if(pl.find(w) > 0):
            pl = pl.replace(w, "")
            break

    for w in directions :
        if(pl.find(w + " of") > 0):
            pl = pl.replace(w + " of", "")
            break
    
    pl = pl.replace( "  ", " ")
    pl = pl.strip()

    for key in subs:
        if(pl == key):
            pl = subs[key]
            break
    
    return pl

#connect to sqlite database
conn = sqlite3.connect('index.sqlite')

#forces database to return strins for text attributes
conn.text_factory = str

#get the cursor for the connection
cur = conn.cursor()

#drop table earthquakes each time code is run to capture data and prevent duplicate info being stored
cur.execute('DROP TABLE IF EXISTS Earthquakes')

#sql script to create table to store earthquake data
cur.execute('''CREATE TABLE IF NOT EXISTS Earthquakes
    (eid TEXT PRIMARY KEY, time INTEGER, mag REAL, place TEXT, 
    region TEXT, felt INTEGER, tsunami INTEGER, title TEXT, lat REAL,
    lng REAL, depth REAL, alert TEXT)''')

#MongoDB Database = earthquakesdb, collection = earthquakes
db = client['earthquakesdb']
earthquakes = db.earthquakes

count = 0

#loops through JSON earthquake data stored in MongoDB
for entry in earthquakes.find() :

    #Extgract data and store in individual variables
    eid = entry["id"]
    etime = int(entry["properties"]["time"])
    lng = float(entry["geometry"]["coordinates"][0])
    lat = float(entry["geometry"]["coordinates"][1])
    dep = float(entry["geometry"]["coordinates"][2])
    place = entry["properties"]["place"]
    alert = entry["properties"]["alert"]
    if(alert == None): alert="blue"
    region = cleanPlace(place)

    mag = float(entry["properties"]["mag"])
    felt = 0
    tsunami = 0
    try:
        felt = int(entry["properties"]["felt"])
        tsunami = int(entry["properties"]["tsunami"])
    except:
        tsunami=0
    title = entry["properties"]["title"]

    #insert statement to store data into earthquake table
    cur.execute('''INSERT OR IGNORE INTO Earthquakes (eid,time, mag, place, region, felt, tsunami, title, lat, lng, depth, alert)
                        VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                        (eid, etime, mag, place, region, felt, tsunami, title, lat, lng, dep, alert))
    #commit the insert statement and print some lines to show progress (#'s divisible by 100)
    if count%100==0:
        print(count, title)
        conn.commit()
  
  #increment count
    count = count + 1

conn.commit()
print(count, "earthquakes processed")

#close connectionss
cur.close()
conn.close()


