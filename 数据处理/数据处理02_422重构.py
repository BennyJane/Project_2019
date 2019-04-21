#!/user/bin/env Python
#coding=utf-8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtk


                         #变量调整
#将第一段代码生成的文件路径拷贝到下方
FirstResult_filepath="E:/编程接单/2019-4-14/提取数据11.csv"
#变化的比率调整
The_Limition=0.001
#最值文件保存的位置及文件名，4列，每列两个点
Final_filename="E:/编程接单/2019-4-14/Second_data02.csv"

#设置图片最后储存位置
filepath="E:/编程接单/2019-4-14/Photo.png"
#设置图片标题
Picture_title="Photo Title"
xlabel=The_Limition


#-----------------------------------------------------------------------------------------------------------------------

df=pd.read_csv(FirstResult_filepath)
#处理数据
end_num = df .shape[0]
for i in range(0, end_num):
    # print(df .iloc[i, 1])
    df .iloc[i, 1] = df .iloc[i, 1][0:19]
# print(df)

#求变化率
#下降
def compute01(num1,num2):
    result=(num1-num2)/num2
    return result

  def compute02（num1,num2):
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
    Current_Process =df.iloc[:i,"means"]  #带有索引号
    # print(Current_Process)
    first_max_price = Current_Process.max()
    first_min_price = Current_Process.min() #只有最值，没有索引号
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

#·························绘制图形····························
#设置图片大小，分辨率
fig = plt.figure(figsize=(20, 6), dpi=90)
ax1 = fig.add_subplot(1, 1, 1)

#-------------------------------------------------------------预设值
#用下标代理原始时间戳数据
idx_pxy = np.arange(df.shape[0])
print(type(idx_pxy))
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
decorateAx(ax1, idx_pxy, df['bid/ask_price'], x_fmt_func)

#······························02····························

                  #绘制第二段数据图形

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

# Simple_Col.to_csv("E:/编程接单/2019-4-14/Simple_Col.csv", index=None)

end_num = Simple_Col .shape[0]
for i in range(0, end_num):
    # print(type(Simple_Col .iloc[i, 0]))
    Simple_Col .iloc[i, 0] = str(Simple_Col .iloc[i, 0])[0:19]
# print(Simple_Col)

Simple_nums = Simple_Col.shape[0]

A_list = []
B_list = []
for j in range(0, Simple_nums):
    # 每次读取两个数据，组成两个点
    try:
        price_01 = Simple_Col.iloc[j, 1]
        price_02=Simple_Col.iloc[j+1, 1]
        date1 = Simple_Col.iloc[j, 0]
        date2 = Simple_Col.iloc[j + 1, 0]


        list1 = []
        a = df[(df["exchange_time"] == date1)&(df['bid/ask_price'] == price_01)].index.tolist()
        b = df[(df["exchange_time"] == date2)&(df['bid/ask_price'] == price_02)].index.tolist()
        list1.append(a[0])
        list1.append(b[0])
        # print(list1)
        Indes_two = np.array(list1)

        list2=[]
        list2=[price_01,price_02]
        B_list=np.array(list2)

        # print(B_list,Indes_two,'/n')
    except:
        continue
    # print(A_list)
    if (j % 2) == 0:
        decorateAx02(ax1, Indes_two,B_list , x_fmt_func)
    else:
        decorateAx03(ax1, Indes_two,B_list , x_fmt_func)
    np.delete(B_list,(0,1),0)
    np.delete(Indes_two, (0, 1), 0)

# 配置横坐标
plt.gcf().autofmt_xdate()  # 自动旋转日期标记
plt.title(Picture_title)
# plt.ylabel(r"price",fontsize=20)
plt.xlabel(xlabel,fontsize=20)
#图片储存
plt.savefig(filepath)
plt.show()

#······························end····························

#将两张表合并
Newdf=pd.concat([Left_df,Right_df],axis=1)
#print(Newdf)

#重新命名表的列名称
Newdf.rename(columns={'exchange_time':'extreme_point', 'bid/ask_price':'Start_price', 'exchange_time':'confirm_point','bid/ask_price':'End_price'}, inplace = True)
Newdf.to_csv(Final_filename,index=None)
