# Earthquake-Analysis

The purpose of this project was to practice using Python and SQL to manipulate and 
analyze data through various methods. The data in question comes from a database of
earthquake data from around the world, stored in JSON format on the USGS website. 
The project consists of 4 programs. Below is a description of the purpose and function
of each program.

1. The downloader.py program downloads the data from the USGS website and stores it in 
a MongoDB cluster in geojson format. The parameters for this project were to store data
for earthquakes with a magnitude greater than 6 worldwise, with a date range of 1/1/2010
to 12/31/2019, in order to collect data on at least 2500 individual earthquakes. 

2. The earthquakes_database program connects to the MongoDB cluster and cleans the data
by iterating a function to remove or change common used directional and regional words
and abreviations, such as changing CA to California and removing descriptions such as 
"southeast of the ______ region" to make the data consistent and in a uniform format.
The progam then uses sqlite to create a SQL database to store the earthquake data. The 
program creates/updates the index.sqlite file based on the data in the MongoDB cluster.

3. The stats.py program stores data from the index.sqlite file using NumPy indexes and 
runs basic statistical analysis to answer a series of questions.

4. The plots.py program stores data from the index.sqlite file using NumPy indexes and
creates 2 histograms to illustrate the distrubution of different magnitudes from the collection
of earthquake data.
