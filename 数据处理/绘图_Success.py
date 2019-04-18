import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from dateutil import parser

#导入第一段代码处理的数据，单个对象的所有时间段数据
FirstResult_filepath="E:/编程接单/2019-4-14/first_result.csv"

#导入第二段代码额外导出的两个文件，Left and Right
Left_df_filepath="E:/编程接单/2019-4-14/Second/Left_df01.csv"
Right_df_filepath="E:/编程接单/2019-4-14/Second/Right_df01.csv"

#设置图片最后储存位置
filepath="E:/编程接单/2019-4-14/Second/Photo.png"
#设置图片标题
Picture_title="Photo Title"


fig = plt.figure(figsize=(20, 6), dpi=90)
ax1 = fig.add_subplot(1, 1, 1)

        #绘制第一段数据图形
# #导入第一段代码处理的数据，单个对象的所有时间段数据
# FirstResult_filepath="E:/编程接单/2019-4-14/first_result.csv"
first_df=pd.read_csv(FirstResult_filepath)

#提取第一段数据的时间序列;并将其解析为时间类型数据
data01_date_str = first_df.iloc[:, 1]
data01_date = list(map(parser.parse, data01_date_str))
print(data01_date)
# print(type(data01_date_str))
#提取第一段数据的均值序列
data01_mean=first_df.iloc[:, 2]

ax1.plot(data01_date, data01_mean, color='k', linewidth='0.5')


                  #绘制第二段数据图形
# #导入第二段代码额外导出的两个文件，Left and Right
# Left_df_filepath="E:/编程接单/2019-4-14/Second/Left_df01.csv"
# Right_df_filepath="E:/编程接单/2019-4-14/Second/Right_df01.csv"
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

# 先将左右两端数据合并到一个df文件中（可以改进合并的方式）
Simple_Col = pd.DataFrame(columns=['exchange_time', 'bid/ask_price'])
for i in range(0, nums):
    Simple_Col = Simple_Col.append(Left_df.iloc[i, :], ignore_index=True)
    Simple_Col = Simple_Col.append(Right_df.iloc[i, :], ignore_index=True)

# print(Simple_Col)
# 选取时间、均值作为横纵坐标
data02_date_str = Simple_Col.iloc[:, 0]  # 选择单一列数据
data02_date = list(map(parser.parse, data02_date_str))
# 提取第二段数据的均值序列
data02_mean = Simple_Col.iloc[:, 1]
# 查看选取出来的数据类型
# print(data02_mean)

Simple_nums = Simple_Col.shape[0]

A_list = []
B_list = []
for j in range(0, Simple_nums):
    # 每次读取两个数据，组成两个点
    A_list = data02_date[j:j + 2]
    B_list = data02_mean[j:j + 2]
    # print(A_list)
    if (j % 2) == 0:
        ax1.plot(A_list, B_list,color='r',linewidth='2',label='Overshoot')
    else:
        ax1.plot(A_list, B_list,color='g',linewidth='2',label='Directional')
    A_list=[]
    B_list=[]


# 配置横坐标
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%H:%M'))
plt.gcf().autofmt_xdate()  # 自动旋转日期标记
plt.title(Picture_title)
#图片储存
plt.savefig(filepath)
plt.show()
