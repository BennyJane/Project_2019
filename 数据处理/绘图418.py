#!usr/bin/env python
# -*- coding: utf-8 -*-

import os 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates
from dateutil import parser

#控制图片大小、分辨率；只设置一个子图
plt.figure(figsize=(13,8), dpi=80)
plt.subplot(1,1,1)

                  #绘制第一段数据图形  

#提取第一段数据的时间序列;并将其解析为时间类型数据
data01_date_str = first_df.iloc[:, 1] #选择单一列数据
data01_date = list(map(parser.parse, data01_date_str))
#提取第一段数据的均值序列
data01_mean=first_df.iloc[:, 2]

#绘制第一段数据
plt.plot(data01_date, data01_mean, color='k', linewidth=0.8, label='predict')


                  #绘制第二段数据图形  
#导入第二段代码处理的数据
Left_df_filepath="E:/编程接单/2019-4-14/Second/Left_df01.csv"
Right_df_filepath="E:/编程接单/2019-4-14/Second/Right_df01.csv"
#导入左列数据，并处理日期
Left_df=pd.read_csv(Left_df_filepath)
end_num=Left_df.shape[0]
for i in range(0,end_num):
    Left_df.iloc[i,0]=Left_df.iloc[i,0][5:19]

#导入右列数据，并处理日期
Right_df=pd.read_csv(Right_df_filepath)
end_num = Right_df.shape[0]
for i in range(0, end_num):
    Right_df.iloc[i, 0] = Right_df.iloc[i, 0][5:19]


#排除两者不等长的情况，取较小的列
if Left_df.shape[0]!=Right_df.shape[0]:
    if Left_df.shape[0]>Right_df.shape[0]:
        nums=Right_df.shape[0]
    else:
        nums = Left_df.shape[0]
else:
    nums=Left_df.shape[0]

#先将左右两端数据合并到一个df文件中（可以改进合并的方式）
Simple_Col=pd.DataFrame(columns=['exchange_time','bid/ask_price'])
for i in range(0,nums):
    Simple_Col = Simple_Col.append(Left_df.iloc[i,:], ignore_index=True)
    Simple_Col = Simple_Col.append(Right_df.iloc[i,:], ignore_index=True)

#选取时间、均值作为横纵坐标
data02_date_str = Simple_Col.iloc[:, 0] #选择单一列数据
data02_date = list(map(parser.parse, data02_date_str))
#提取第二段数据的均值序列
data02_mean=Simple_Col.iloc[:, 1]
#查看选取出来的数据类型
print(type(data02_mean))

Simple_nums=Simple_Col.shape[0]
x=[]
y=[]
for j in range(0,Simple_nums):
    #每次读取两个数据，组成两个点
    x=data02_date[j:j+1]
    y=data02_mean[j:j+1]
    if (j%2)==0:
        plt.plot(data02_date, data02_mean, color='r', linewidth=1, label='Overshoot')
    else:
        plt.plot(data02_date, data02_mean, color='g', linewidth=1, label='Overshoot')
    del x[:]
    del y[:]
          

# 显示图示
plt.legend()

# 配置横坐标
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator())    # 按周显示,按日显示的话，WeekdayLocator()将改成DayLocator()
plt.gcf().autofmt_xdate()  # 自动旋转日期标记
plt.title('Photo Title')
#图片储存
plt.savefig("E:/编程接单/2019-4-14/Second/Photo.png")
plt.show()












#end

