#!/user/bin/env Python
#coding=utf-8

from pprint import pprint
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

# 统计代码耗费时间的消耗时间
print('*' * 50)
t3 = time.time()

                         #变量调整

#将第一段代码文件路径拷贝到下方
FirstResult_filepath="E:/编程接单/2019-4-14/first_result.csv"
#变化的比率调整
The_Limition=0.001
#最后文件保存的位置及文件名
Final_filename="E:/编程接单/2019-4-14/Second/Second_data01.csv"


df=pd.read_csv(FirstResult_filepath)
# print(df)

#提取单独的均值列
Mean_df=df['bid/ask_price']
# print(Mean_df.info)

def compute(num1,num2):
    result=(num1-num2)/num2
    return result

# 构造储存的表
Left_df = pd.DataFrame(columns=['exchange_time', 'bid/ask_price'])
Right_df = pd.DataFrame(columns=['exchange_time', 'bid/ask_price'])

# 利用k值的奇偶性，来记录数值变化趋势
# 上一个k为奇数代表降，下一个找升；上一个k偶数代表上升，下一个要找降
k = 1
first_break_point = 0
# series 类型
end_num = Mean_df.shape[0]
#从第二个数据开始读取
for i in range(1, end_num):
    #切片，最后一个i位不输出
    Current_Process = Mean_df.iloc[:i]
    # Current_Process=Mean_df[:i]
    # print(Current_Process)
    first_max_price = Current_Process.max()
    first_min_price = Current_Process.min()
    last_price = Current_Process.iloc[i-1]
    result = compute(first_max_price, first_min_price)
    if result < The_Limition:
        continue
    else:
        first_break_point = i
        # >=The_Limition
        # 找到第一组最值
        # 判断升降
    if last_price == first_max_price:
        k = k + 1
        # print(last_price, first_max_price)
        # 找出最小值所在的行，注意保存的先后顺序
        min_id = Current_Process.idxmin()
        max_id = Current_Process.idxmax()
        # print(min_id, max_id)
        # 选出时间和价格，分别保存到起、终点的dataframe中，最后再考虑合并
        Left_df.loc[Left_df.shape[0]] = df.iloc[min_id, 1:]  # 只取出时间和价格
        Right_df.loc[Right_df.shape[0]] = df.iloc[max_id, 1:]  # 只取出时间和价格

        # 先完成一段数据的查找
        break

    else:
        # print(last_price, first_min_price)
        # 找出最小值所在的行，注意保存的顺序
        max_id = Current_Process.idxmax()
        min_id = Current_Process.idxmin()
        print(max_id, min_id)
        # 选出时间和价格，分别保存到起、终点的dataframe中，最后再考虑合并
        Left_df.loc[Left_df.shape[0]] = df.iloc[max_id, 1:]  # 只取出时间和价格
        Right_df.loc[Right_df.shape[0]] = df.iloc[min_id, 1:]  # 只取出时间和价格

        # 先完成一段数据的查找
        break

n=first_break_point
j=first_break_point
while True :
    j = j+1
    if j <end_num:
        #先判断第一段是升 or 降
        if (k % 2)==0:
            #上一个K为偶数，下一个找下降
            #保证可以取到2个数以上
            N_Process=Mean_df.iloc[n:j]
            # print(n,j)
            N_max_price = N_Process.max()
            N_min_price = N_Process.min()
            # print(type(N_Process))
            # print(N_Process.index)
            last_price = N_Process.loc[j-1]
            result = compute(N_max_price, N_min_price)
            if result >= The_Limition:
                # 最后一个极值必须是最小值
                if last_price == N_min_price:
                    # print(j)
                    k = k + 1
                    n = j
                    # 找出最大值所在的行，注意保存的顺序
                    # print(last_price,N_max_price, N_min_price)
                    max_id = N_Process.idxmax()
                    min_id = j-1
                    # print(max_id, min_id)
                    # 选出时间和价格，分别保存到起、终点的dataframe中，最后再考虑合并到一张表中
                    Left_df.loc[Left_df.shape[0]] = df.iloc[max_id, 1:]  # 只取出时间和价格
                    Right_df.loc[Right_df.shape[0]] = df.iloc[min_id, 1:]  # 只取出时间和价格
                    # 完成一段数据的查找
                    print('完成了一对极值的查找：%s' % k)

        else:
            #上一个K为奇数，下一个要找升
            #保证可以取到2个数以上
            N_Process=Mean_df.iloc[n:j]
            N_max_price=N_Process.max()
            N_min_price=N_Process.min()
            last_price=N_Process.loc[j-1]
            result=compute(N_max_price,N_min_price)
            if result >= The_Limition:
                #最后一个极值必须是最大值
                if last_price ==N_max_price:
                    k=k+1
                    n = j
                    # print(last_price, N_min_price, N_max_price)
                    #找出最小值所在的行，注意保存的顺序
                    max_id=j-1
                    min_id=N_Process.idxmin()
                    # print(min_id,max_id)
                    #选出时间和价格，分别保存到起、终点的dataframe中，最后再考虑合并到一张表中
                    Left_df.loc[Left_df.shape[0]] = df.iloc[min_id, 1:]#只取出时间和价格
                    Right_df.loc[Right_df.shape[0]] = df.iloc[max_id, 1:]#只取出时间和价格
                    #先完成一段数据的查找
                    print('完成了一对极值的查找：%s' % k)
                    #break
    else:
        break

Left_df.to_csv("E:/编程接单/2019-4-14/Second/Left_df01.csv",index=None)

Right_df.to_csv("E:/编程接单/2019-4-14/Second/Right_df01.csv",index=None)
# print(Left_df)
# print(Right_df)

#将两张表合并
Newdf=pd.concat([Left_df,Right_df],axis=1)
#print(Newdf)

#重新命名表的列名称
# Newdf.rename(columns={'exchange_time':'extreme_point', 'bid/ask_price':'Start_price', 'exchange_time':'confirm_point','bid/ask_price':'End_price'}, inplace = True)
Newdf.to_csv(Final_filename,index=None)


t4 = time.time()
print("总共耗时 %s 秒" %(t4-t3))
