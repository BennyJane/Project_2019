import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtk


file = "E:/编程接单/2019-4-14/提取数据11.csv"
df = pd.read_csv(file, parse_dates=[0])
end_num = df .shape[0]
for i in range(0, end_num):
    # print(df .iloc[i, 1])
    df .iloc[i, 1] = df .iloc[i, 1][0:19]
# print(df)

file02 ="E:/编程接单/2019-4-14/Simple_Col.csv"
Simple_Col = pd.read_csv(file02, parse_dates=[0])
end_num = Simple_Col .shape[0]
for i in range(0, end_num):
    # print(type(Simple_Col .iloc[i, 0]))
    Simple_Col .iloc[i, 0] = str(Simple_Col .iloc[i, 0])[0:19]
# print(Simple_Col)


#设置图片最后储存位置
filepath="E:/编程接单/2019-4-14/Photo.png"
#设置图片标题
Picture_title="Photo Title"


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

#·························绘制图形····························
fig = plt.figure(figsize=(20, 6), dpi=90)
ax1 = fig.add_subplot(1,1,1)
# decorateAx(ax1, df['exchange_time'], df['bid/ask_price'], None)
decorateAx(ax1, idx_pxy, df['bid/ask_price'], x_fmt_func)
#·························绘制图形····························

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
        print(list1)
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
#图片储存
plt.savefig(filepath)
plt.show()


