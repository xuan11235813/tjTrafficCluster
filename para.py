class Para:

    def __init__(self):
        self.sqlHost = 'localhost'
        self.user = 'gzx'
        self.password = 'Dingtian@1993'
        self.dataBaseName = 'test1'
        self.monthDaysNormal = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        self.monthDaysLeap = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        self.prefix = 'record_bus_gpsdata_'

    def getDBProperty(self):
        return self.sqlHost, self.user, self.password, self.dataBaseName

    def getTableNameArray(self, start_time, end_time):
        # time in this form:
        # e.g. 20181001
        dateList = []

        startTimeList = list(start_time)
        endTimeList = list(end_time)

        if len(startTimeList) != 8 or len(endTimeList) != 8:
            print('wrong date input')
        else:

            startYear = int(startTimeList[0] + startTimeList[1] +
                            startTimeList[2] + startTimeList[3])
            endYear = int(endTimeList[0] + endTimeList[1] +
                          endTimeList[2] + endTimeList[3])
            startMonth = int(startTimeList[4] + startTimeList[5])
            endMonth = int(endTimeList[4] + endTimeList[5])

            startDay = int(startTimeList[6] + startTimeList[7])
            endDay = int(endTimeList[6] + endTimeList[7])

            for year in range(startYear, endYear + 1):
                for month in range(startMonth, endMonth + 1):
                    if month == startMonth:
                        monthStart = startDay
                    else:
                        monthStart = 1

                    if month == endMonth:
                        for day in range(monthStart, endDay + 1):
                            yearStr = str(year)
                            if month <= 9:
                                monthStr = '0' + str(month)
                            else:
                                monthStr = str(month)
                            if day <= 9:
                                dayStr = '0' + str(day)
                            else:
                                dayStr = str(day)
                            strItem = yearStr + monthStr + dayStr
                            dateList.append(strItem)
                    else:
                        if year % 4 == 0:
                            monthEnd = self.monthDaysLeap[month - 1]
                        else:
                            monthEnd = self.monthDaysNormal[month - 1]
                        for day in range(monthStart, monthEnd + 1):
                            yearStr = str(year)
                            if month <= 9:
                                monthStr = '0' + str(month)
                            else:
                                monthStr = str(month)
                            if day <= 9:
                                dayStr = '0' + str(day)
                            else:
                                dayStr = str(day)
                            strItem = yearStr + monthStr + dayStr
                            dateList.append(strItem)

        for i in range(len(dateList)):
            dateList[i] = self.prefix + dateList[i]

        return dateList
'''
para = Para()
print(para.getTableNameArray('20181001', '20181001'))
'''
