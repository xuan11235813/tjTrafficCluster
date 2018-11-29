import datetime


class DataProcess:

    def __init__(self):

        # define the allowed number of existent zeros before and after current
        # sample
        self.preZeros = 2
        self.laterZeros = 2
        self.subSumLimit = 0.2

        # maximal allowed time interval in seconds
        self.maxmalTimeInterval = 20

        # sudden accelerate/decelerate threshold
        self.accelerateTheshold = 1.3

        # the regular group size
        self.regularGroupSize = 100

    def filter(self, data):
        # data structure should be [(speed, second)]

        _data = []
        if len(data) >= 8:
            for i in range(self.preZeros):
                _data.append(data[i])
            # 0 for actual previous item of original dataset has been written
            # 1 for previous exist at least 1 abnormal data
            preFlag = 0

            for i in range(self.preZeros, len(data) - self.laterZeros):

                # flag for current item abnormal or not
                # 1 for abnormal
                # 0 for normal
                # default is normal
                currentFlag = 0
                preSum = 0.0
                laterSum = 0.0
                for j in range(i - self.preZeros, i):
                    preSum = preSum + data[j][0]
                for j in range(i + 1, i + self.laterZeros + 1):
                    laterSum = laterSum + data[j][0]
                if (abs(laterSum) <= self.subSumLimit) and (abs(preSum) <= self.subSumLimit) and float(data[i][0]) < 0.1:
                    currentFlag = 1
                timeInterval = 0

                if preFlag == 0:
                    timeInterval = data[i][1] - data[i - 1][1]
                else:
                    timeInterval = data[i + 1][1] - data[i][1]
                if timeInterval >= self.maxmalTimeInterval:
                    currentFlag = 1

                if currentFlag == 0:
                    _data.append(data[i])
                    preFlag = 0
                else:
                    preFlag = 1
        return _data

    def getFeature(self, data):
        # feature 1 for speed in 40 -55
        # feature 2 for speed above 55
        # feature 3 for sudden accelerate/decelerate
        N = len(data)
        feature1 = 0.0
        feature2 = 0.0
        feature3 = 0.0
        for i in range(1, len(data)):
            previousItem = data[i - 1]
            currentItem = data[i]
            speedDelta = abs(currentItem[0] - previousItem[0])
            timeDelta = abs(currentItem[1] - previousItem[1])
            speed = currentItem[0] * 3.6
            if timeDelta > 0:
                if (speed >= 40) and (speed <= 55):
                    feature1 = feature1 + 1
                elif speed > 55:
                    feature2 = feature2 + 1
                isSudden = (speedDelta / float(timeDelta)
                            ) >= self.accelerateTheshold
                if isSudden:
                    feature3 = feature3 + 1

        feature1 = feature1 / N
        feature2 = feature2 / N
        return [feature1, feature2, feature3]

    def setRegularGroupGetFeatures(self, data):

        N = len(data)
        groupNum = float(N) / self.regularGroupSize
        group = []
        if groupNum <= 1:
            print('group size too large')
        else:
            if groupNum - int(groupNum) >= 0.5:
                groupNum = int(groupNum) + 1
            else:
                groupNum = int(groupNum)
            for i in range(groupNum):
                groupItem = []
                start = i * self.regularGroupSize
                end = (i + 1) * self.regularGroupSize
                if end >= N:
                    end = N
                for j in range(start, end):
                    groupItem.append(data[j])
                group.append(groupItem)
        return group

    def getGroupProperty(self, data):

        startTime = datetime.datetime(
            1970, 1, 1) + datetime.timedelta(0, data[0][1])
        endTime = datetime.datetime(1970, 1, 1) + \
            datetime.timedelta(0, data[-1][1])
        if(startTime.year < 10):
            startTimeYear = '0' + str(startTime.year)
        else:
            startTimeYear = '' + str(startTime.year)
        if(startTime.month < 10):
            startTimeMonth = '0' + str(startTime.month)
        else:
            startTimeMonth = '' + str(startTime.month)
        if(startTime.day < 10):
            startTimeDay = '0' + str(startTime.day)
        else:
            startTimeDay = '' + str(startTime.day)
        if(startTime.hour < 10):
            startTimeHour = '0' + str(startTime.hour)
        else:
            startTimeHour = '' + str(startTime.hour)
        if(startTime.minute < 10):
            startTimeMinute = '0' + str(startTime.minute)
        else:
            startTimeMinute = '' + str(startTime.minute)
        if(startTime.second < 10):
            startTimeSecond = '0' + str(startTime.second)
        else:
            startTimeSecond = '' + str(startTime.second)
        if(startTime.year < 10):
            startTimeYear = '0' + str(startTime.year)
        else:
            endTimeYear = '' + str(endTime.year)
        if(endTime.month < 10):
            endTimeMonth = '0' + str(endTime.month)
        else:
            endTimeMonth = '' + str(endTime.month)
        if(endTime.day < 10):
            endTimeDay = '0' + str(endTime.day)
        else:
            endTimeDay = '' + str(endTime.day)
        if(endTime.hour < 10):
            endTimeHour = '0' + str(endTime.hour)
        else:
            endTimeHour = '' + str(endTime.hour)
        if(endTime.minute < 10):
            endTimeMinute = '0' + str(endTime.minute)
        else:
            endTimeMinute = '' + str(endTime.minute)
        if(endTime.second < 10):
            endTimeSecond = '0' + str(endTime.second)
        else:
            endTimeSecond = '' + str(endTime.second)

        startTimeStr = '' + str(startTimeYear) + '-' + str(startTimeMonth) + \
            '-' + str(startTimeDay) + ' ' + str(startTimeHour) + \
            ':' + str(startTimeMinute) + ':' + str(startTimeSecond)
        endTimeStr = ''
        endTimeStr = '' + str(endTimeYear) + '-' + str(endTimeMonth) + \
            '-' + str(endTimeDay) + ' ' + str(endTimeHour) + \
            ':' + str(endTimeMinute) + ':' + str(endTimeSecond)
        return [startTimeStr, endTimeStr]
