from sql import *


para = Para()
sql = SQL(para)
precond = ['distinct']
routeID = '10066'
busID = '\'55Y0E146\''
colName = ['bus_id', 'station_id']
tableName = 'record_bus_gpsdata_20181001'
conditions = ['type=41','bus_id=\'BE45746234\'']
print(sql.getBusID(tableName, routeID))
print(sql.getSpeedTimeFromID(tableName, routeID, busID))
