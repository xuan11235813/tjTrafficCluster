#!/usr/bin/python
import MySQLdb
 


db = MySQLdb.connect(host="localhost",  # your host 
                     user="gzx",       # username
                     passwd="Dingtian@1993",     # password
                     db="test1")   # name of the database
 
# Create a Cursor object to execute queries.
cur = db.cursor()
 
# Select data from table using SQL query.
cur.execute("select * from record_bus_gpsdata_20181001 where route_id = 10066")
 
# print the first and second columns      
data = cur.fetchall()

print(len(data))