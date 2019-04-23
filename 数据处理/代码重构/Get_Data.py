# !usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import os

#新建一张表，将读取的文件合并到新的表中
alldf=pd.DataFrame()


def read_csv(filepath):
    global alldf
    filename=os.listdir(filepath)
    print(filename)
    for file in filename:
        filepath=all_csv_filepath+"/"+file
        df=pd.read_csv(filepath)
        alldf=pd.concat([alldf,df])
    return alldf

def get_means(alldata, user_id):
    Simple_ID = alldata[alldata['instrument_id'] == user_id]
    #shape后不能跟括号
    max_col=Simple_ID.shape[1]
    print(max_col)  #11
    #求出每行的均值，mean()求出每列的均值，生成了新的表，只包含生成的均值
    #用insert()函数直接在表最后一列插入均值
    Simple_ID.insert(max_col,"means",Simple_ID[['bid_price','ask_price']].mean(1))
    #筛选出'instrument_id','exchange_time',"means"三列
    means_data=Simple_ID[['instrument_id','exchange_time',"means"]]
    return means_data

def get_period_data(Means_Data,period):
    # 处理日期问题: 先转date类型，再设置为索引号
    #筛选时间段，转换为data格式，[]号
    Means_Data['exchange_time'] = pd.to_datetime(Means_Data['exchange_time'])

    #小括号（），将时间设置为索引
    Means_Data.set_index("exchange_time", inplace=True)

    Period_data=pd.DataFrame()
    #选取9：00-10：15 、10：30-11:30、13：30-15:00段的数据，修改日期范围来扩大选择范围
    for i in period:
        first_data01 = Means_Data["2019-{} 09:00:00".format(i):"2019-{} 10:15:00".format(i)]
        first_data02 = Means_Data["2019-{} 10:30:00".format(i):"2019-{} 11:30:00".format(i)]
        first_data03 = Means_Data["2019-{} 13:30:00".format(i):"2019-{} 15:00:00".format(i)]
        Period_data = pd.concat([Period_data,first_data01, first_data02, first_data03])
    return Period_data


if __name__=="__main__":

    # 将待处理的CSV文件全部放到一个文件夹内，再将路径复制到下面，修改为 “/”
    # 用自己本地文件路径更换下面的 "E:/编程接单/2019-4-14/raw0301"
    all_csv_filepath = "E:/编程接单/2019-4-14/raw0301"
    # 设置选中的ID，并挑选出包含该id的所有行
    Select_instrument_id = 'rb1905'
    # 设置日期，“2019-03-01”用“03-01”代替， “2019-0304”——“03-04”，等等；允许多个不连续日期，但日趋顺序必须正确；
    # 四月份的单独处理，需要在下面修改月份
    days = ["03-01", "03-04"]
    # 设置最后文件保存位置
    final_filepath = "E:/编程接单/2019-4-14/提取数据18_01-04.csv"


    alldata = read_csv(all_csv_filepath)
    means_df=get_means(alldata,Select_instrument_id)
    Final_data=get_period_data(means_df,days)
    #将索引重新改为数值，并调整列表顺序
    Final_data.reset_index(inplace=True)
    order = ['instrument_id', 'exchange_time', "means"]
    Final_data = Final_data[order]
    Final_data.info()
    # Final_data.to_csv(final_filepath,index=None)
