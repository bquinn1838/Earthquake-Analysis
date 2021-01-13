## import numpy as np
import sqlite3
from collections import Counter
import numpy as np

#Input validation
while True:
    try:
        howmany = int(input("How many earthquake locations to show?"))
    except ValueError:
        print("Invalid input. Please try again.")
    if howmany < 1 :
        print("Input must be at least 1. Please try again.")
        continue
    elif  howmany > 20 :
        print("Input cannot exceed 20. Please try again.")
        continue
    else: 
        print("Showing ", howmany, " earthquakes.")
        break

#connect to index.sqlite database
conn = sqlite3.connect('index.sqlite')
conn.text_factory = str 
cur = conn.cursor()
cur.execute("SELECT * FROM Earthquakes")


#Variables to store data
placecounts = dict()
regioncounts = dict()
mag = []
felt = []
tsunami = []
depth = []
places = []
regions = []

#Iterate through Earthquakes and store values 

rows = cur.fetchall()
for row in rows:
    mag.append(row[2])
    felt.append(row[5])
    tsunami.append(row[6])
    depth.append(row[9])
    places.append(row[3])
    regions.append(row[4])
    #Counter function creates dictionary from places/regions list where key,value = place/region, count
    placecounts = Counter(places)
    regioncounts = Counter(regions)

print('')
#Display top n places
print('Top',howmany,'earthquake places:')


x = sorted(placecounts, key=placecounts.get, reverse=True)
for k in x[:howmany]:
    print(k, placecounts[k])
    if placecounts[k] < 10 : break    

#Display top n regions
print('\nTop',howmany,'earthquake regions:') 

x = sorted(regioncounts, key=regioncounts.get, reverse=True)
for k in x[:howmany]:
    print(k, regioncounts[k])
    if regioncounts[k] < 10 : break 

#Basic statistics for magnitude using numpy
print("\nBasic Statistics for all earthquakes:")
np_mag = np.array(mag)
print("Total number of earthquakes: ", len(np_mag))
print("Biggest earthquaqke: ", np.amax(np_mag))
print("Mean magnitude: ", np.mean(np_mag))
print("Median magnitude: ", np.median(np_mag))
print("Standard deviation: ", np.std(np_mag))

#Boolean index for felt > 0 to get magnitudes for felt quakes
npfilter = np.array(felt)
filterB = npfilter > 0

magF = np_mag[filterB == True]

#Basic statistics filtered for felt quakes
print("\nBasic Statistics for felt earthquakes:")
print("Total number of felt earthquakes: ", len(magF))
print("Biggest felt earthquaqke: ", np.amax(magF))
print("Mean magnitude: ", np.mean(magF))
print("Median magnitude: ", np.median(magF))
print("Standard deviation: ", np.std(magF))