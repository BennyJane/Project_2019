from pprint import pprint
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

# 统计该爬虫的消耗时间
print('*' * 50)
t3 = time.time()

#将第二段段代码生成的文件路径拷贝到下方
#该文件包含了圆点-三角形点的时间和价格
FirstResult_filepath="E:/编程接单/2019-4-14/最终成果/Second_result.csv"
df=pd.read_csv(FirstResult_filepath)
# print(df)

#求总收益，每2行一组，需要判断第一行为买进操作，还是卖出操作
sum=0
nums=df.shape[0]
# print(nums)
for i in range(0,nums,2):
    try:
        End_price01=df.iloc[i,3]
        print(End_price01)
        End_price02=df.iloc[i+1,3]
    except Exception as e:
        End_price01=0
        End_price02=0
    #需要判断第一行是升，还是降
    if (df.iloc[0,3]-df.iloc[0,1]) >=0:
        #第一行为升，此刻选择卖出
        sum=sum+(End_price01-End_price02)
    else:
        #第一行为降，此刻选择买进，付款，所以为负数
        sum = sum + (End_price02 - End_price01)


print("这段时间交易赚取的金额数值为：%s " %sum)


t4 = time.time()
print('总共耗时：%s' % (t4 - t3))

