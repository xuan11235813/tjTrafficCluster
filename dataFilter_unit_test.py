from dataFilter import *
from sql import *

'''
['55Y0E142', '55Y0E152', '556L6016', '556L6004', '55Y0E144', '55Y0E133', '55Y0E135', '55Y0E145', '556L5484', 
'556L6115', '55Y0E140', '556L6114', '55Y0E136', '55Y0E148', '55Y0E149', '55Y0E151', '55S0N103', '55Y0E150', 
'55Y0E147', '556L6010', '556L6027', '556L6002', '55S0N102', '55Y0E137', '55Y0E134', '55Y0E146', '556L6022', 
'55Y0E143', '55Y0E138', '556L6013', '55S0N101', '55Y0E139', '55Y0E141']

'''

para = Para()
sql = SQL(para)
dataProcess = DataProcess()
precond = ['distinct']
routeID = '10066'
busID = '\'55Y0E139\''
colName = ['bus_id', 'station_id']
tableName = 'record_bus_gpsdata_20181001'
conditions = ['type=41','bus_id=\'BE45746234\'']
data = sql.getSpeedTimeFromID(tableName, routeID, busID)
data_ = dataProcess.filter(data)


print(len(data_))
print(len(data))

print(dataProcess.getFeature(data_))

group = dataProcess.setRegularGroupGetFeatures(data_)

for i in range(len(group)):
	print(dataProcess.getFeature(group[i]))
	print(dataProcess.getGroupProperty(group[i]))