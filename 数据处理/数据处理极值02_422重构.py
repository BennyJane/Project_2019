#!/user/bin/env Python
#coding=utf-8

#最后一位不一定是最值。



from pprint import pprint
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

                         #变量调整

#将第一段代码文件路径拷贝到下方
FirstResult_filepath="E:/编程接单/2019-4-14/提取数据1704.csv"
#变化的比率调整
The_Limition=0.001
#最后文件保存的位置及文件名
Final_filename="E:/编程接单/2019-4-14/Second_data00.csv"


df=pd.read_csv(FirstResult_filepath)
df.rename(columns={"bid/ask_price":"means"},inplace=True)
# print(df)
# print(df.info())

Left_df = pd.DataFrame()
Right_df = pd.DataFrame()


#储存最值索引号为列表，用于画图
MAX_MIN_List=[]

#求变化率
#下降
def compute01(num1,num2):
    result=(num1-num2)/num1
    return result
#上升
def compute02(num1,num2):
    result=(num1-num2)/num2
    return result

end_num = df .shape[0]

# 利用k值的奇偶性，来记录数值变化趋势
# 上一个k为奇数代表降，下一个找升；上一个k偶数代表上升，下一个要找降
k = 1
first_break_point = 0
# series 类型
endnum =df.shape[0]
#从第二个数据开始读取
for i in range(1, endnum):
    Current_Process =df.loc[0:i,"means"]  #带有索引号
    # print(Current_Process)
    # print(Current_Process)
    first_max_price = Current_Process.max()
    max_id = Current_Process.idxmax()
    first_min_price = Current_Process.min() #只有最值，没有索引号
    min_id = Current_Process.idxmin()
    last_price = Current_Process.iloc[i]
    print(first_max_price,first_min_price, "\t",last_price,"\t",)
    if min_id < i:
        #up
        result = compute02(last_price, first_min_price)
        print(result)
        if result >= The_Limition:
            first_break_point = i
            k = k + 1
            # print(last_price, first_max_price)
            # 找出最值所在行的索引，注意保存的先后顺序
            min_id = Current_Process.idxmin()
            max_id = i
            MAX_MIN_List.append(min_id)
            MAX_MIN_List.append(max_id)
            print(MAX_MIN_List)
            # 选出整行数据储存，保留索引，输出的时候再考虑删除多余数据，考虑合并
            Left_df=Left_df.append(df.iloc[min_id])
            Right_df=Right_df.append(df.iloc[max_id])
            # 先完成一段数据的查找
            print("该数据以UP趋势开头")
            break

    elif max_id<i:
        #down
        result = compute01(first_max_price,last_price)
        print(result)
        if result >= The_Limition:
            first_break_point = i
            print(first_break_point)
            k = k + 1
            #print(last_price, first_min_price)
            # 找出最小值所在的行，注意保存的顺序
            max_id = Current_Process.idxmax()
            min_id = i
            MAX_MIN_List.append(max_id)
            MAX_MIN_List.append(min_id)
            print(MAX_MIN_List)
            # 选出时间和价格，分别保存到起、终点的dataframe中，最后再考虑合并
            Left_df=Left_df.append(df.iloc[max_id])
            Right_df=Right_df.append(df.iloc[min_id])
            print("该数据以DOWN趋势开头")
            # 先完成一段数据的查找
            break
    else:
        continue


# print(Left_df,"\n",Right_df)
JiZhi_df=df.iloc[MAX_MIN_List,[0,2]]
print(JiZhi_df)

#将两张表合并,需要先去掉原来的索引号，这样“1”号的索引与另一个“1”号索引合并。
Left_df=Left_df.reset_index()
Left_df=Left_df.iloc[:,[1,3]]

Right_df=Right_df.reset_index()
Right_df=Right_df.iloc[:,[1,3]]

# Left_df=Left_df.append(Right_df,axis=1)

Newdf=pd.concat([Left_df,Right_df],axis=1)
print(Newdf)

#重新命名表的列名称
# Newdf.rename(columns={'exchange_time':'extreme_point', 'bid/ask_price':'Start_price', 'exchange_time':'confirm_point','bid/ask_price':'End_price'}, inplace = True)
# Newdf.to_csv(Final_filename,index=None)
