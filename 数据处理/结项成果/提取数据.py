# !usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import os

                        #更换参数

#将待处理的CSV文件全部放到一个文件夹内，再将路径复制到下面，修改为 “/”
#用自己本地文件路径更换下面的 "E:/编程接单/2019-4-14/raw0301"
all_csv_filepath="E:/编程接单/2019-4-14/raw0301"
#all_csv_filepath01=["E:/编程接单/2019-4-14/raw0301","E:/编程接单/2019-4-14/raw0310","E:/编程接单/2019-4-14/raw0320","E:/编程接单/2019-4-14/raw0401"]

#设置选中的ID，并挑选出包含该id的所有行
Select_instrument_id='rb1905'
#设置日期，“2019-03-01”用“03-01”代替， “2019-0304”——“03-04”，等等；允许多个不连续日期，但日趋顺序必须正确；
#四月份的单独处理，需要在下面修改月份
days=["03-01","03-04"]


#设置最后文件保存位置
final_filepath="E:/编程接单/2019-4-14/提取数据18_01-04.csv"


#------------------------------------------------------------------------------------------------------
#新建一张表，将读取的文件合并到新的表中
alldf=pd.DataFrame()
Simple_IDs=pd.DataFrame()

filename=os.listdir(all_csv_filepath)
print(filename)
for file in filename:
    filepath=all_csv_filepath+"/"+file
    df=pd.read_csv(filepath)
    alldf=pd.concat([alldf,df])

Simple_ID = alldf[alldf['instrument_id'] == Select_instrument_id]
# Simple_IDs = pd.concat([Simple_IDs, Simple_ID])

#求出每行的均值，mean()求出每列的均值，生成了新的表，只包含生成的均值
bid_ask_mean=Simple_ID[['bid_price','ask_price']].mean(1)

#筛选出'instrument_id','exchange_time'两列
filter_01=Simple_ID[['instrument_id','exchange_time']]

#合并列，axis=1，必须设置；合并后发现均值列，没有列名，默认为数值 0
filter_02=pd.concat([filter_01,bid_ask_mean],axis=1)

# #处理日期显示问题
# end_num = filter_02 .shape[0]
# for i in range(0, end_num):
#     filter_02 .iloc[i, 1] = filter_02 .iloc[i, 1][0:19]

#筛选时间段，转换为data格式，[]号
filter_02['exchange_time'] = pd.to_datetime(filter_02['exchange_time'])


#小括号（），将时间设置为索引
filter_03 = filter_02.set_index("exchange_time")

all_data=pd.DataFrame()
#选取9：00-10：15 、10：30-11:30、13：30-15:00段的数据，修改日期范围来扩大选择范围
for i in days:
    first_data01 = filter_03["2019-{} 09:00:00".format(i):"2019-{} 10:15:00".format(i)]
    first_data02 = filter_03["2019-{} 10:30:00".format(i):"2019-{} 11:30:00".format(i)]
    first_data03 = filter_03["2019-{} 13:30:00".format(i):"2019-{} 15:00:00".format(i)]
    all_data = pd.concat([all_data,first_data01, first_data02, first_data03])

# all_data.info()
print(all_data)

#调整标题序号
all_data=all_data.reset_index()
order = ['instrument_id','exchange_time',0]
all_data_order = all_data[order]

#修改表头，并输出
all_data_order.rename(columns={0:'bid/ask_price'},inplace=True)
all_data_order.sort_values(by=["exchange_time"],inplace=True)

all_data_order.info()

all_data_order.to_csv(final_filepath,index=None)
