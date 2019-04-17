#!/user/bin/env Python
#coding=utf-8

from pprint import pprint
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure,gca,show
import time

# 统计该爬虫的消耗时间
print('*' * 50)
t3 = time.time()

#设置子图数量位置figsize=(15,8),

fig, ax = plt.subplots(2,1)

#导入第一段代码处理的数据
FirstResult_filepath="E:/编程接单/2019-4-14/first_result.csv"
first_df=pd.read_csv(FirstResult_filepath)
#处理日期数据
def get_time(self,data):
    data=data[4:18]
    return data
first_df["exchange_tim"]=first_df.apply(lambda x:get_time(x,"exchange_tim"),axis=1)

#处理日期的显示问题
end_num=first_df.shape[0]
for i in range(0,end_num):
    first_df.iloc[i,1]=first_df.iloc[i,1][5:19]
    # print(first_df.iloc[i,1])
# print(first_df)


#筛选第一段数据中的'exchange_time','bid_ask_mean'两列
filter_01=first_df[['exchange_time','bid/ask_price']]
filter_01=filter_01.set_index("exchange_time")


#设置横坐标的准确数值;放大图的显示,绘制底图
#9：00-10：15 、10：30-11:30、13：30-15:00
# plot_picture=filter_01.plot(linewidth='0.8',color='k',title='Picture Title',sharex=True,sharey=True,ax=ax[1])


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


Simple_Col_red=pd.DataFrame(columns=['exchange_time','bid/ask_price'])
#先画转折的线，红色
for i in range(0,nums):
    Simple_Col_red = Simple_Col_red.append(Left_df.iloc[i,:], ignore_index=True)
    Simple_Col_red = Simple_Col_red.append(Right_df.iloc[i,:], ignore_index=True)

Simple_Col_red=Simple_Col_red.set_index("exchange_time")
filter_01=pd.concat([filter_01,Simple_Col_red],axis=1)
plot_picture=filter_01.plot(linewidth='0.8',color='k',title='Picture Title',sharex=True,sharey=True,ax=ax[1])

#移除图例
ax[1].legend_.remove()
# plt.xticks(rotation=45)
#设置横纵标签
plt.xticks(rotation=0)
plt.ylabel(r"price",fontsize=20)
plt.xlabel(r"time",fontsize=20)

plt.show()

#
# for i in range(0,nums):
#     Simple_Col_red = Simple_Col_red.append(Left_df.iloc[i,:], ignore_index=True)
#     Simple_Col_red = Simple_Col_red.append(Right_df.iloc[i,:], ignore_index=True)
#     Simple_Col_red=Simple_Col_red.set_index("exchange_time")
#     print(Simple_Col_red)
#     Simple_Col_red.plot(linewidth='1', color='r',sharex=True,sharey=True,ax=ax[1])
#     Simple_Col_red = Simple_Col_red.reset_index()
#
#     Simple_Col_red.drop([0,1],inplace=True)
