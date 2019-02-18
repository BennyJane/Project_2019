2.8 从数据库中导入数据
-----------------------------------------------------------







'学习更多关于 异常值清理，常规数据清理的知识'
		概率模型（statistical models）
		采样理论（sampling theory）


2.9 清除异常值（outlier）——统计学、领域知识、慧眼
----------------------------------------------------------
1 MAD（中位数绝对偏差）Median absolute deviation
	描述单变量（包含一个变量）样本在定量数据中可变性的一种标准
	用来 度量统计分布，因为 MAD会落在一组稳健统计数据中，因此对异常值有抵抗力
2 通过人工检查数据

'补充'
shape函数是numpy.core.fromnumeric中的函数，它的功能是读取矩阵的维度。
例：
shape(matrixA) 返回matrixA的（行数，列数）元组
shape(matrixA) [0]  ==》 行数
shape(matrixA) [1]  ==》 列数
shape的输入参数可以使一个实数，一个一维列表（数组），二维数组，也可以是一个矩阵。

---------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt

def is_outlier(points, threshold=3.5):
	
	if len(points.shape) == 1:
		points = points[:,None]

	#计算中位数，只有一个'数值'
	median = np.median(points, axis=0) 		#axis=0 代表行
	#计算了标准差，仍然是列表！
	diff = np.sum((points - median)**2, axis=-1) 
	#计算方差，每个数字都开方
	diff = np.sprt(diff)
	#计算MAD
	med_abs_deviation = np.median(diff) #此时，diff应该只有一个值？？为什么还要用 median（）函数。
	
	modified_z_score = 0.6745*diff / med_abs_deviation
		#0,6745 怎么来的？

	reutrn modified_z_score > threshold

x=np.random.random(100)

buckets = 50 #histogram buckets 直方图中柱子的数量

#add in a few outliers
x = np.r_[x, -49, 95, 100, -100]

filtered = x[~is_outlier(x)] #在Numpy中，'~'操作符，被重载为一个逻辑操作符，作用在布尔数组上，取非操作。


plt.figure() #画直方图

plt.sublot(211) #增加画布上的一个子图
plt.hist(x, buckets)
plt.xlabel('Raw')

plt.subplot(212)
plt.hist(filtered, buckets)
plt.xlabel('Cleaned')

plt.show()


箱线图（box plot）
---------------------------------------------------------
	显示中值、上四分位数、下四分位数、远离箱体的异常值
	箱体 从数据的低四分位数延伸到高四分位数，在中值附近有一条线，箱体延伸出的箱须（whiskers）显示数据的范围，超出箱须末端的点，就是异常值。
补充：
* numpy.random.rand(d0,d1,…dn) 
	以给定的形状创建一个数组，并在数组中加入在[0,1]之间均匀分布的随机样本。



from pulab import *

spread=rand(50)*100
center = ones(25)*100			#生成全是1点一维矩阵，扩大100

flier_high = rand(10)*100+100
flier_low = rand(10)-100

data = concatenate((spread, center, flier_high, flier_low), 0) #合并个数据 concatenate()

#箱体图
subplot(311)
#'gx' defining the outlier plotting properties
boxplot(data, 0 , 'gx') # boxplot() #？

#对比散点图01
subplot(312)
spread_1 = concatenate((spread, flier_high, flier_low), 0)				#总共70个数值
center_1 = ones(70) * 25		#ones（num）* A；将A重复num次
scatter(center_1, spread_1)
xlim([0,50])		#?xlim() 横坐标范围

#对比散点图02
subplot(313)
center_2 = rand(70) * 50		#np.randam.rand()在[0,1]内生成70个随机，再扩大50倍
scatter(cneter_2, spread_1)		#表示，x、y值
xlim([0, 50]) 

show()
