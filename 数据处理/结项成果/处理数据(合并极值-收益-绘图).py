#!/user/bin/env Python
#coding=utf-8

#4-29调整，每天数据重新判断开始的趋势。
#代码完成寻找极值，绘制图像，计算收益功能，并能保存图片，与收益表

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtk


                         #待输入的数据
#将第一段代码生成的文件路径拷贝到下方
FirstResult_filepath="E:/编程任务/2019-4-14/结项整理/代码重构/First_data_01-04.csv"
#变化的比率调整
The_Limition=0.003

                        #保存极值列表
Final_filename="E:/编程任务/2019-4-14/Second_four_data429_01-04.csv"
SimpleCoul_filename = "E:/编程任务/2019-4-14/Simple_Col429_01-04.csv"

                        # 图像相关变量调整
#设置图片最后储存位置
filepath="E:/编程任务/2019-4-14/Photo429_01-04.png"
#设置图片标题
Picture_title="Photo Title:0.001"
xlabel=The_Limition

                        # 收益相关变量调整
#收益文件储存位置，包含极值数据。
Sales_filepath="E:/编程任务/2019-4-14/Sales429_0304.csv"


#-----------------------------------------------------------------------------------------------------------------------
df=pd.read_csv(FirstResult_filepath)
df.rename(columns={"bid/ask_price":"means"},inplace=True)
# print(df)
# print(df.info())

#求变化率
#下降
def compute01(num1,num2):
    result=(num1-num2)/num1
    return result
#上升
def compute02(num1,num2):
    result=(num1-num2)/num2
    return result

#将不同的日期的数据分割开
def get_eachday(data):
    startday=0
    oneday = []
    EachDay_list=[]
    for i in range(data.shape[0]-1):
        now_day=data.iloc[i,1]
        # print(now_day[5:11])
        Previous_day=data.iloc[i+1,1]
        if now_day[5:11]!=Previous_day[5:11]:
            endday=i
            EachDay_list.append([startday,endday])
            startday=i+1
    EachDay_list.append([startday,data.shape[0]])
    return EachDay_list

def Get_ExtremeValues(data,start_num,end_num):
    # 储存起始点
    Left_df = pd.DataFrame()
    Right_df = pd.DataFrame()

    # 储存最值索引号为列表，用于画图
    MAX_MIN_List = []

    # 输入第一段代码处理的数据结果
    k = 1
    first_break_point = 0

    # 从第二个数据开始读取
    for i in range(start_num, end_num):
        Current_Process = data.loc[start_num:i, "means"]  # 带有索引号
        # print(Current_Process)
        # print(Current_Process)
        first_max_price = Current_Process.max()
        max_id = Current_Process.idxmax()
        first_min_price = Current_Process.min()  # 只有最值，没有索引号
        min_id = Current_Process.idxmin()
        last_price = Current_Process.loc[i]
        # print(first_max_price,first_min_price, "\t",last_price,"\t",)
        if min_id < i:
            # up
            result = compute02(last_price, first_min_price)
            # print(result)
            if result >= The_Limition:
                first_break_point = i
                k = k + 1
                # print(last_price, first_max_price)
                # 找出最值所在行的索引，注意保存的先后顺序
                MAX_MIN_List.append(min_id)
                MAX_MIN_List.append(max_id)
                # print(MAX_MIN_List)
                # 选出整行数据储存，保留索引，输出的时候再考虑删除多余数据，考虑合并
                Left_df = Left_df.append(data.loc[min_id])
                Right_df = Right_df.append(data.loc[max_id])
                # 先完成一段数据的查找
                print("该数据以UP趋势开头: 0")
                break

        elif max_id < i:
            # down
            result = compute01(first_max_price, last_price)
            # print(result)
            if result >= The_Limition:
                first_break_point = i
                # print(first_break_point)
                k = k
                # print(last_price, first_min_price)
                # 找出最小值所在的行，注意保存的顺序
                MAX_MIN_List.append(max_id)
                MAX_MIN_List.append(min_id)
                # print(MAX_MIN_List)
                # 选出时间和价格，分别保存到起、终点的dataframe中，最后再考虑合并
                Left_df = Left_df.append(data.loc[max_id])  # 只取出时间和价格
                Right_df = Right_df.append(data.loc[min_id])  # 只取出时间和价格
                print("该数据以DOWN趋势开头: 0")
                # 先完成一段数据的查找
                break
        else:
            continue

    n = first_break_point
    j = first_break_point
    while True:
        j = j + 1
        if j < end_num:
            if (k % 2) == 0:
                # 上一个K为偶数，下一个找下降,Down
                # 保证可以取到2个数以上
                N_Process = df.loc[n:j, "means"]
                # print(N_Process)
                N_max_price = N_Process.max()
                max_id = N_Process.idxmax()
                last_price = N_Process.loc[j]
                # 最后一个极值必须是最小值
                if max_id < j:
                    result = compute01(N_max_price, last_price)
                    # print(result)
                    if result >= The_Limition:
                        # print(j)
                        k = k + 1
                        n = j
                        # 找出最大值所在的行，注意保存的顺序
                        max_id = N_Process.idxmax()
                        min_id = j
                        MAX_MIN_List.append(max_id)
                        MAX_MIN_List.append(min_id)
                        # print(MAX_MIN_List)
                        # 选出时间和价格，分别保存到起、终点的dataframe中，最后再考虑合并到一张表中
                        Left_df = Left_df.append(df.loc[max_id])
                        Right_df = Right_df.append(df.loc[min_id])
                        # 完成一段数据的查找
                        print('完成了一对极值的查找：%s' %(k-1))

            else:
                # 上一个K为奇数，下一个要找升
                # 保证可以取到2个数以上
                N_Process = df.loc[n:j, "means"]
                # print(N_Process)
                N_min_price = N_Process.min()
                min_id = N_Process.idxmin()
                last_price = N_Process.loc[j]
                if min_id < j:
                    result = compute02(last_price, N_min_price)
                    if result >= The_Limition:
                        k = k + 1
                        n = j
                        # print(last_price, N_min_price, N_max_price)
                        # 找出最小值所在的行，注意保存的顺序
                        max_id = j
                        min_id = N_Process.idxmin()
                        MAX_MIN_List.append(min_id)
                        MAX_MIN_List.append(max_id)
                        # print(MAX_MIN_List)
                        # 选出时间和价格，分别保存到起、终点的dataframe中，最后再考虑合并到一张表中
                        Left_df = Left_df.append(df.loc[min_id])
                        Right_df = Right_df.append(df.loc[max_id])
                        # 先完成一段数据的查找
                        print('完成了一对极值的查找：%s' %(k-1))

        else:
            break

    return MAX_MIN_List,Left_df,Right_df

def Get_FinalData(extreme_list,data1,data2):
    Extremes_df = df.iloc[extreme_list, [1, 2]]
    # print(Extremes_df)
    # Extremes_df.to_csv(SimpleCoul_filename)

    # 将两张表合并,需要先去掉原来的索引号，这样“1”号的索引与另一个“1”号索引合并。
    data1 = data1.reset_index()
    data1 = data1.iloc[:, [1, 3]]

    data2 = data2.reset_index()
    data2 = data2.iloc[:, [1, 3]]

    Newdf = pd.concat([data1, data2], axis=1)
    return Extremes_df , Newdf

#······························求每天极值·························

EachDay_list = get_eachday(df)
print("当前正在处理%s天的数据！" %len(EachDay_list))
print("每天数据起始索引号：",EachDay_list)
MAX_MIN_List=[]
Extremes_1cols=pd.DataFrame()
Extremes_4cols=pd.DataFrame()
for i in EachDay_list:
    S=i[0]
    E=i[1]
    print(S,E)
    max_min_list, left_df, right_df=Get_ExtremeValues(df,S,E)
    extremes_1cols, extremes_4cols =Get_FinalData(max_min_list, left_df, right_df)
    MAX_MIN_List=MAX_MIN_List+max_min_list
    Extremes_1cols=pd.concat([Extremes_1cols,extremes_1cols])
    Extremes_4cols=pd.concat([Extremes_4cols,extremes_4cols])

# print(MAX_MIN_List,Extremes_1cols,"\n", Extremes_4cols)
#重新命名表的列名称,每行4条数据
Extremes_4cols.columns=['Extremity','Start_price', 'confirm_point','End_price']
Newdf=Extremes_4cols
# Newdf.to_csv(Final_filename,index=None)
# print(Newdf)


# print(Left_df,"\n",Right_df)
Simple_Col=df.iloc[MAX_MIN_List,[1,2]]
# print(Simple_Col)

#·························绘制图形····························
#设置图片大小，分辨率
fig = plt.figure(figsize=(20, 6), dpi=90)
ax1 = fig.add_subplot(1, 1, 1)

#-------------------------------------------------------------------------------------------------------------------
#用下标代理原始时间戳数据
idx_pxy = np.arange(df.shape[0])
# print(type(idx_pxy))
#下标-时间转换func
def x_fmt_func(x, pos=None):
    idx =np.clip(int(x+0.5), 0, df.shape[0]-1)
    return df['exchange_time'].iat[idx]
#绘图流程
def decorateAx(ax, xs, ys, x_func):
    ax.plot(xs, ys, color="k", linewidth=0.3, linestyle="-")
    # ax.plot(ax.get_xlim(), [0,0], color="blue", linewidth=0.5, linestyle="--")
    if x_func:
        #set数据代理func
        ax.xaxis.set_major_formatter(mtk.FuncFormatter(x_func))
    ax.grid(True)
    return

def decorateAx02(ax, xs, ys, x_func):
    ax.plot(xs, ys, color="r", linewidth=1, linestyle="-")
    # ax.plot(ax.get_xlim(), [0,0], color="blue", linewidth=0.5, linestyle="--")
    if x_func:
        #set数据代理func
        ax.xaxis.set_major_formatter(mtk.FuncFormatter(x_func))
    ax.grid(True)
    return

def decorateAx03(ax, xs, ys, x_func):
    ax.plot(xs, ys, color="b", linewidth=1, linestyle="-")
    # ax.plot(ax.get_xlim(), [0,0], color="blue", linewidth=0.5, linestyle="--")
    if x_func:
        #set数据代理func
        ax.xaxis.set_major_formatter(mtk.FuncFormatter(x_func))
    ax.grid(True)
    return

#------------------------------------------------------------end-------------------------------------------------------
                                                #绘制所有数据的图像
decorateAx(ax1, idx_pxy, df['means'], x_fmt_func)

#······························02····························

                  #绘制第二段数据图形
Simple_nums = Simple_Col.shape[0]

A_list = []
B_list = []
for j in range(0, Simple_nums):
    # 每次读取两个数据，组成两个点
    try:
        mean_01 = Simple_Col.iloc[j, 1]
        mean_02=Simple_Col.iloc[j+1, 1]

        list1=[]
        list1.append(MAX_MIN_List[j])
        list1.append(MAX_MIN_List[j+1])
        Indes_two = np.array(list1)

        list2=[mean_01,mean_02]
        B_list=np.array(list2)
    except Exception as  e:
        print(e)
        continue

    if (j % 2) == 0:
        decorateAx02(ax1, Indes_two,B_list , x_fmt_func)
    else:
        decorateAx03(ax1, Indes_two,B_list , x_fmt_func)
    np.delete(B_list,(0,1),0)
    np.delete(Indes_two, (0, 1), 0)

# # 配置横坐标
# plt.gcf().autofmt_xdate()  # 自动旋转日期标记
# plt.title(Picture_title)
# # plt.ylabel(r"price",fontsize=20)
# # plt.xlabel(xlabel,fontsize=20)
# #图片储存
# plt.savefig(filepath)
# plt.show()


#······························收益数据导出·······················

Sales=pd.DataFrame(columns=["confirm_point","income"])

#求总收益，每2行一组，需要判断第一行为买进操作，还是卖出操作
sum=0
nums=Newdf.shape[0]
print(nums)

j=0
i=0
# 第一行为升，此刻选择卖出
while True:
    if i < nums:
        Now_time=Newdf.iloc[j,2]
        # 需要判断每天的开始的第一行是升，还是降
        if (Newdf.iloc[j, 3] - Newdf.iloc[j, 1]) >= 0:
            try:
                Start_time1=Newdf.iloc[i, 2]
                Start_time2 = Newdf.iloc[i+1, 2]
            except Exception as e:
                Start_time1='2019-03-01'
                Start_time2 = '2019-10-02'
                print(e)
            if Start_time1[6:11]==Now_time[6:11]:
                if Start_time2[6:11]==Now_time[6:11]:
                    try:
                        End_price01 = Newdf.iloc[i, 3]
                        End_price02 = Newdf.iloc[i + 1, 3]
                    except Exception as e:
                        End_price01 = 0
                        End_price02 = 0
                    # print(End_price01-End_price02)
                    sum=sum+(End_price01-End_price02)
                    Day = Start_time2
                    Sales.loc[Sales.shape[0] + 1] = [Day, sum]
                    i=i+2
                else:
                    j=i+1
                    i=i+1
                    sum = 0
                    # continue
            else:
                j=i
                sum=0
                # continue

        else:
            try:
                Start_time1=Newdf.iloc[i, 2]
                Start_time2 = Newdf.iloc[i+1, 2]
            except Exception as e:
                Start_time1=Newdf.iloc[i, 2]
                Start_time2 = '2019-10-02'
                print(e)
            if Start_time1[6:11]==Now_time[6:11]:
                if Start_time2[6:11]==Now_time[6:11]:
                    try:
                        End_price01 = Newdf.iloc[i, 3]
                        End_price02 = Newdf.iloc[i + 1, 3]
                    except Exception as e:
                        End_price01 = 0
                        End_price02 = 0
                    # print(End_price01 - End_price02)
                    sum = sum + (End_price02 - End_price01)
                    # print(sum)
                    Day = Start_time2
                    Sales.loc[Sales.shape[0] + 1] = [Day, sum]
                    i=i+2
                else:
                    j=i+1
                    i+=1
                    sum = 0
                    # continue
            else:
                j = i
                sum=0
                # continue
    else:
        break



#······························文件输出·······················

# 配置横坐标
plt.gcf().autofmt_xdate()  # 自动旋转日期标记
plt.title(Picture_title)
# plt.ylabel(r"price",fontsize=20)
# plt.xlabel(xlabel,fontsize=20)
#图片储存
# plt.savefig(filepath)
plt.show()

#sales 求的是当前时间之前的累计收益；每一天的最后一条信息里的金额，就是当天的总收益
Newdf02=pd.merge(Newdf, Sales, how="left",on="confirm_point")
print(Newdf02)
# Newdf02.to_csv(Sales_filepath,index=None)
