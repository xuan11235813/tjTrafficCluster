import MySQLdb
from para import *
import datetime


class SQL:

    def __init__(self, parameter):
        _host, _user, _password, _databaseName = parameter.getDBProperty()
        self.db = MySQLdb.connect(host=_host,  # your host
                                  user=_user,       # username
                                  passwd=_password,     # password
                                  db=_databaseName)   # name of the database
        self.cur = self.db.cursor()
        self.type = '41'

    def selectInstruction(self, precond, colName, tableName, conditions):
        instruction = []
        instruction.extend(['select', ' '])
        for word in precond:
            instruction.append(word)
            instruction.append(' ')
        for word in colName:
            instruction.append(word)
            instruction.append(',')
        instruction[-1] = ' from '
        instruction.append(tableName)
        instruction.append(' where ')
        for cond in conditions:
            instruction.append(cond)
            instruction.append(' ')
            instruction.append('and')
            instruction.append(' ')
        del instruction[-1]
        del instruction[-1]
        instructString = ''
        for word in instruction:
            instructString = instructString + word
        return instructString

    def getBusID(self, tableName, routeID):
        precond = ['distinct']
        colName = ['bus_id']
        conditions = ['type=' + self.type, 'route_id=' + routeID]
        instruction = self.selectInstruction(
            precond, colName, tableName, conditions)
        busIDList = []
        print('Get bus id from database')
        try:
            self.cur.execute(instruction)
            data = self.cur.fetchall()
            for name in data:
                busIDList.append(name[0])
        except Exception, e:
            print(instruction)
            print(str(e))
            print('wrong input/sql error')
            busIDList = []
        print('Done!')
        return busIDList

    def getSpeedTimeFromID(self, tableName, routeID, busID):

        result = []
        precond = []
        colName = ['speed', 'updatetime']
        conditions = ['type=' + self.type,
                      'route_id=' + routeID, 'bus_id=' + busID]
        instruction = self.selectInstruction(
            precond, colName, tableName, conditions)
        print('Get speed and time id of '+ busID + 'from table ' + tableName + ' :')
        try:
            self.cur.execute(instruction)
            data = self.cur.fetchall()
            for item in data:
                result.append((float(item[0]), float(
                    (item[1] - datetime.datetime(1970, 1, 1)).total_seconds())))
        except Exception, e:

            print(instruction)
            print(str(e))
            print('wrong input/sql error')

            result = []
        print('Done!')
        return result
