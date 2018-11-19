# -*- coding: UTF-8 -*-

import copy
import math
import random
import time
import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import decimal

from para import *
from sql import *
from dataFilter import *


# 用于初始化隶属度矩阵U
global MAX
MAX = 10000.0
# 用于结束条件
global Epsilon
Epsilon = 0.00000001


def import_data_format_iris(file):
    """ 
    格式化数据，前四列为data，最后一列为cluster_location
    一共4列，读取2-4列信息
    """
    data = []
    cluster_location = []
    with open(str(file), 'r') as f:
        for line in f:
            current = line.strip().split(",")
            current_dummy = []
            for j in range(1, len(current)):
                current_dummy.append(float(current[j]))
            j += 1
# 			if  current[j] == "Iris-setosa\n":
# 				cluster_location.append(0)
# 			elif current[j] == "Iris-versicolor\n":
# 				cluster_location.append(1)
# 			else:
# 				cluster_location.append(2)
            data.append(current_dummy)
    print("加载数据完毕")
    return data


def import_data_from_database(parameter):
    # startTime, endTime should in format yyyymmdd, like 20181001

    startTime, endTime, routeID = parameter.getTimeAndRoute()

    data = []
    dataProperty = []
    # initialize parameters
    para = parameter

    # initialize sql
    sql = SQL(para)

    # initialize data process class
    dataProcess = DataProcess()

    # from time period get table name array
    tableNameList = para.getTableNameArray(startTime, endTime)

    # for each table get the distinct bus id
    # for each bus id get its data including speed and time
    for i in range(len(tableNameList)):
        tableName = tableNameList[i]

        # get distinct bus id
        busIDList = sql.getBusID(tableName, routeID)

        # for each bus id get its data
        for busID in busIDList:

            rawData = sql.getSpeedTimeFromID(tableName, routeID, '\'' + busID + '\'')

            # data after filter
            rawDataFiltered = dataProcess.filter(rawData)

            # divide into groups:
            groupedData = dataProcess.setRegularGroupGetFeatures(
                rawDataFiltered)

            # for each group get features and properties
            for item in groupedData:

                # get feature
                featureItem = dataProcess.getFeature(item)

                # get property
                propertyItem = dataProcess.getGroupProperty(item)

                # append data and property into list
                data.append(featureItem)

                # add bus id and table name to property ready for recall
                propertyItem = propertyItem + (busID, tableName,)
                dataProperty.append(propertyItem)

    return data, dataProperty


def randomise_data(data):
    """
    该功能将数据随机化，并保持随机化顺序的记录
    """
    order = list(range(0, len(data)))
    random.shuffle(order)
    new_data = [[] for i in range(0, len(data))]
    for index in range(0, len(order)):
        new_data[index] = data[order[index]]
    return new_data, order


def de_randomise_data(data, order):
    """
    此函数将返回数据的原始顺序，将randomise_data()返回的order列表作为参数
    """
    new_data = [[]for i in range(0, len(data))]
    for index in range(len(order)):
        new_data[order[index]] = data[index]
    return new_data


def print_matrix(list):
    """ 
    以可重复的方式打印矩阵
    """
    for i in range(0, len(list)):
        print(list[i])


def initialise_U(data, cluster_number):
    """
    这个函数是隶属度矩阵U的每行加起来都为1. 此处需要一个全局变量MAX.
    """
    global MAX
    U = []
    for i in range(0, len(data)):
        current = []
        rand_sum = 0.0
        for j in range(0, cluster_number):
            dummy = random.randint(1, int(MAX))
            current.append(dummy)
            rand_sum += dummy
        for j in range(0, cluster_number):
            current[j] = current[j] / rand_sum
        U.append(current)
    return U


def distance(point, center):
    """
    该函数计算2点之间的距离（作为列表）。我们指欧几里德距离。        闵可夫斯基距离
    """
    if len(point) != len(center):
        return -1
    dummy = 0.0
    for i in range(0, len(point)):
        dummy += abs(point[i] - center[i]) ** 2
    return math.sqrt(dummy)


def end_conditon(U, U_old):
    """
        结束条件。当U矩阵随着连续迭代停止变化时，触发结束
        """
    global Epsilon
    for i in range(0, len(U)):
        for j in range(0, len(U[0])):
            if abs(U[i][j] - U_old[i][j]) > Epsilon:
                return False
    return True


def normalise_U(U):
    """
    在聚类结束时使U模糊化。每个样本的隶属度最大的为1，其余为0
    """
    for i in range(0, len(U)):
        maximum = max(U[i])
        for j in range(0, len(U[0])):
            if U[i][j] != maximum:
                U[i][j] = 0
            else:
                U[i][j] = 1
    return U

# m的最佳取值范围为[1.5，2.5]


def fuzzy(data, cluster_number, m):
    """
    这是主函数，它将计算所需的聚类中心，并返回最终的归一化隶属矩阵U.
参数是：簇数(cluster_number)和隶属度的因子(m)
    """
    # 初始化隶属度矩阵U
    U = initialise_U(data, cluster_number)
    # print_matrix(U)
    # 循环更新U
    while (True):
        # 创建它的副本，以检查结束条件
        U_old = copy.deepcopy(U)
        # 计算聚类中心
        C = []
        for j in range(0, cluster_number):
            current_cluster_center = []
            for i in range(0, len(data[0])):
                dummy_sum_num = 0.0
                dummy_sum_dum = 0.0
                for k in range(0, len(data)):
                    # 分子
                    dummy_sum_num += (U[k][j] ** m) * data[k][i]
                    # 分母
                    dummy_sum_dum += (U[k][j] ** m)
                # 第i列的聚类中心
                current_cluster_center.append(dummy_sum_num / dummy_sum_dum)
        # 第j簇的所有聚类中心
            C.append(current_cluster_center)

        # 创建一个距离向量, 用于计算U矩阵。
        distance_matrix = []
        for i in range(0, len(data)):
            current = []
            for j in range(0, cluster_number):
                current.append(distance(data[i], C[j]))
            distance_matrix.append(current)

        # 更新U
        for j in range(0, cluster_number):
            for i in range(0, len(data)):
                dummy = 0.0
                for k in range(0, cluster_number):
                    # 分母
                    dummy += (distance_matrix[i][j] /
                              distance_matrix[i][k]) ** (2 / (m - 1))
                U[i][j] = 1 / dummy

        if end_conditon(U, U_old):
            print("结束聚类")
            break

    print("标准化 U")
    print('聚类中心:')
    for i in range(0, len(C)):
        print("Center of Cluster %d  is:" % (i + 1))
        print(C[i])

    U = normalise_U(U)
    return U


def cluster_detail(final_location, original_data):
    cluster1 = []
    cluster2 = []
    cluster3 = []
    cluster4 = []
    for i in range(0, len(final_location)):
        current_cluster = final_location[i]
        if current_cluster[0] == 1:
            cluster1.append(original_data[i])
        elif current_cluster[1] == 1:
            cluster2.append(original_data[i])
        elif current_cluster[2] == 1:
            cluster3.append(original_data[i])
        else:
            cluster4.append(original_data[i])
    return cluster1, cluster2, cluster3, cluster4

def clusterMain(parameter):

    # 加载数据,填入数据数据文件名
    # original_data = import_data_format_iris("iris2.csv")
    original_data, dataProperties = import_data_from_database(parameter)
    #print_matrix(original_data)
    #print("--------------------------------------------------------------------------------------------------------------------------------")

    # 随机化数据
    data, order = randomise_data(original_data)
    #print_matrix(data)
    #print("--------------------------------------------------------------------------------------------------------------------------------")

    start = time.time()
    # 现在我们有一个名为data的列表，它只是数字
    # 我们还有另一个名为cluster_location的列表，它给出了正确的聚类结果位置
    # 调用模糊C均值函数
    final_location = fuzzy(data, 4, 2)

    # 还原数据
    final_location = de_randomise_data(final_location, order)
    #print_matrix(final_location)
    cluster1, cluster2, cluster3, cluster4 = cluster_detail(
        final_location, original_data)
    '''
    # 准确度分析
    print("用时：{0}".format(time.time() - start))
    print_matrix(cluster1)
    print("Above is cluster1---------------------------------------------------------------------------------------------------------------")

    print_matrix(cluster2)
    print("Above is cluster2---------------------------------------------------------------------------------------------------------------")

    print_matrix(cluster3)
    print("Above is cluster3---------------------------------------------------------------------------------------------------------------")

    print_matrix(cluster4)
    print("Above is cluster4---------------------------------------------------------------------------------------------------------------")
	'''
    return final_location, dataProperties