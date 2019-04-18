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

