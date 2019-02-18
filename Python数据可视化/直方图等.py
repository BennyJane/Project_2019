3.9 直方图
---------------------------------------------------------
	*表示一定间隔下数据点频率的垂直矩形——称为bin
	bin以固定的间隔创建——直方图的面积=数据点点数量
	bin图也可以显示数据点相对频率，而不是使用数据点绝对值，在这种情况下，总面积=1
	*直方图，也常用在图像处理软件中，作为可视化图像属性（如 给定颜色通道上光的分布）的一种方式，
	*这些图像直方图，进一步可以应用在计算机视觉算法来检测峰值，用来辅助进行边缘检测、图像分割
	*想要得到正确的bin数量，但是没有严格的规则来说明什么是最优bin 数量，所以很难做到这一点。？？？🤔️
	怎么计算bin数量有几种不同的理论，最简单的一个是基于取整（ceiling）函数，这时（bins（k））= ceiling(max(x)-min(y)/x),x是绘制的数据集合，h为期望的bin宽


import numpy as np
import matplotlib.pyplot as plt

mu = 100
sigma = 15
x = np.random.normal(mu, sigma, 10000) #?

ax = plt.gca()

#the histogram of the date. histgram 直方图
ax.hist(x, bins=35, color='red')

ax.set_xlabel('Values')
ax.set_ylabel('Frequency')

ax.set_title(r'$\mathrm{Histogram:}\ \mu=%d,\ \sigram=%d$' %(mu, sigram))

plot.show()

'补充'
#Matplotlib绘图的过程中，可以为各个轴的Label，图像的Title、Legend等元素添加Latex风格的公式。
#只需要在Latex公式的文本前后各增加一个$符号，Matplotlib就可以自动进行解析，示例代码如下：
r'$\name$'

 plt.scatter(x,y,label=r'$\alpha =\frac{1}{2}\ln(\frac{1-\varepsilon}{\varepsilon })$')
plt.xlabel(r'$\varepsilon$',fontsize=20)
plt.ylabel(r'$\alpha$',fontsize=20)


3.9 直方图
---------------------------------------------------------











3.12 绘制带填充区域的图表
---------------------------------------------------------
	对曲线下面 或者 两个曲线之间的区域进行填充
	plot() fill_between()

from matpoltlib.pyplot import figure, show , gca
import numpy as np

x = np.arange(0.0, 2, 0.01)
# two different signals are measured
y1 = np.sin(2*np.pi*x)
y1 = 1.2*np.sin(4*np.pi*x)

fig = figure()
ax = gca()

#plot and fill between y1 and y2 where a logical condition is met ax.plt(x,y1,xy2,color = 'black')

ax.fill_between(x, y1, x, y2, where=y2>=y1, facecolor ='dariblue', interpolate = True)
ax.fill_between(x, y1, x, y2, where=y2<=y1, facecolor='deeppink', interpolate = True)
	#interpolate 插入  where 需要等号吗？
	#where参数来指定一个条件来填充曲线，where参数接受布尔值（可以是表达式），只会填充满足where条件的区域

ax.set_title('filled between')

show()

补充：
fill_between()方法，可接受许多参数
	hatch
	线条选修（linewidth linestyle）

fill_betweenx() 相似的填充特性，主要针对 '水平曲线'
fill() 更通用，可对任意'多边形填充颜色' or '隐形线'



3.12 绘制带彩色标记的散点图
---------------------------------------------------------
	*如果有两个变量，想标记处它们之间的相关关系（correlation）——散点图
	*可以作为更高级的多维数据可视化的基础，比如绘制散点图矩阵（scatter plot matrix）
	自变量（无关变量）：independent variable
	应变量（相关变量）：dependent variable
	scatter()——'参数'
	marker 设置点状标记，默认circle
	alpha 透明度
	edgecolors 标记的边界颜色
	label 图例框

import matplotlib.pyplot as plt
import numpy as np

x = np.random.randn(1000)

y1 = np.random.randn(len(x)) #与x数组相同长度

y2 = 1.2 + np.exp(x)

ax1 = plot.subplot(121)
plt.scatter(x, y1, color='indigo', alpha=0.3, edgecolors='white', label='no correl') #右上角的图例
plt.xlabel('no correlation') #axis轴的名称
plt.grid(True)
plt.legend() #legend 传说 图例

ax2 = plot.subplot(122, sharey=ax1, sharex=ax1)
plt.scatter(x, y2, color='green', alpha=0.3,edgecolors='grey', label='correl')
plt.xlabel('strong correlation')
plt.grid(True)
plt.legend()

plt.show()
