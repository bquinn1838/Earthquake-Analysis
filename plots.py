import sqlite3
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab


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

#numpy array to store all magnitudes
np_mag = np.array(mag)

#boolean index for felt earthquakes
npfilter = np.array(felt)
filterB = npfilter > 0

#filtering magnitude numpy array to store only felt earthquakes
magF = np_mag[filterB == True]

#Pyplot histogram for all earthquakes
plt.style.use('fivethirtyeight')
plt.tight_layout()
plt.hist(np_mag, bins=12, edgecolor='black')
plt.title('Magnitudes of All Earthquakes')
plt.xlabel('Magnitude')
plt.ylabel('# of Earthquakes')
plt.savefig('Magnitude.png')
plt.show()

#Pyplot histogram for felt earthquakes
plt.style.use('fivethirtyeight')
plt.tight_layout()
plt.hist(magF, bins=12, edgecolor='black')
plt.title('Magnitudes of Felt Earthquakes')
plt.xlabel('Magnitude')
plt.ylabel('# of Earthquakes')
plt.savefig('Magnitude_Felt.png')
plt.show()
