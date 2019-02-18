Matplotlib 绘制图表

Matplotlib 绘制并定制化图表
-----------------------------------------------------------
在'IPyton'中操作

柱状图、线状图、堆积柱状图
----------------------------------------------------
'01'
plot([1,2,3,4,3,2,1])
绘制基本图表

plot()的值为y轴的值；plot()为x轴提供默认值

'02'
plot([4,3,2,1],[1,2,3,4])

注释：
	调用 hold(False) 可以关闭 hold属性；打开 hold() 属性，则接下来所有图表都绘制在相同的坐标轴下。这是 IPython 的pylab模式的默认行为。————在编写常规Oython脚本中，hold 属性默认是关闭。
'03'
from matplotlib.pyplot import *

x = [1,2,3,4]
y = [5,4,3,2]

figure()		#调用figure（）创建一个新的图表。

subplot(231) #divide subplots into 2*3 grid, and select #1
			#将画布分为 2行3列，选择第一个图
			#subplot(2,3,1)
plot(x, y)

subplot(232)
bar(x, y)

subplot(233) #horizontal bar-charts
barh(x, y) 

subpl0t(234)
bar(x, y)

y1 = [7,8,5,3]	#we need more data for stacked bar charts
				#更多数据， 堆叠柱状图 ；和上面一张图画在同一个表
bar(x, y1, bottom=y, color = 'r') # bottom = y 将y值作为y1的起点。将第二个柱状图，叠加在第一个柱状图上面。

subplot(235)
boxplot(x)

subplot(236)
scatter(x,y)

show


绘制正余弦图像
---------------------------------------------------------



设置坐标轴长度和范围
---------------------------------------------------------
axis() #调用不带参数的axis()方法，将返回坐标轴的默认值。

>>>1 = [-1,1,-10,10]
>>>axis(1) #xmin xmax ymin ymax
[-1,1,-10,10]

matplotlib自动使用最小值，刚好展示所有的数据点；
axis()小于数据集合中的最大值，部分数据不可见。
autoscale() 计算坐标轴的最佳大小以适应数据的显示
matplotlib.pyplot.axes()
rect
left
bottom
width
height
axisbg

sharex/sharey
(x/y)
polar
pplar axes

向当前图中添加一条线，可以调用：
	matplotlib.pyplot.axhline()
	axhline() #axis high line 参数：y向位置、xmin xmax
	matplotlib.pyplot.axvline()
	axvline() #axis vertical 参数：x向位置，ymin ymax
	#当不调用参数时，使用默认值 0 ，axhline()绘制一条y=0的水平线axuline() x=0的垂直线
添加跨坐标轴的水平带（矩形）：
	matplotlib.pyplot.axhspan()
	axhspan() #必须使用 ymin ymax参数，指定水平带带宽度
	matplotlib.pyplot.axvspan()
	axvspan() xmin xmax

图形中的网格属性，默认时关闭的；
	matplotlib.pyplot.grib() 切换网格显示状态，控制参数：
	which: 指定绘制的网格刻度类型、(major、 minor、 both)
	axis: 指定绘制哪组网格线、(both x y)
坐标轴的内部实现上由几个Python类表示:
	其中一个父类，matplotlib.axis.Axes 包含操作坐标轴的大多方法
	单独一个坐标轴由 matplotlib.axis.Axis 表示，
	matplotlib.axis.XAxis
	matplotlib.axis.YAxis y轴

设置图表的线型、属性、格式化字符串
---------------------------------------------------------
plot(x, y, linewidth(1.5))

line = plot(x,y) # line, = plot(x,y)
line.set_linewidth(1.5)

使用MATLAB（c）的人，
lines = plot(x, y)
setp(lines, 'linewidth', 1.5)

setp(lines, linewidth=1.5)

线条的所有属性都包含在 matplotlib.lines.Line2D类中

'属性'
alpha
color/c 
dashes
label
linestyle/Is
linewidth/Iw
marker
markeredgecolor/mec
markeredgewidth/mew
markerfacecolor/mfc
markersize/ms
solid_joinstyle
visible
xdata
ydata
Zorder #控制叠加样式的顺序 # artist 艺术样式

'线条的样式'

'线条的标记'

'颜色'
matplotlib.pylot.colors() 获得matplotlib支持的所有颜色

其他方式：
第一，HTML十六进制字符串
color = '#eeefff'
或者使用合法的HTML颜色名字。('red', 'chartreuse')
第二，归一化到[0,1]的RGB元组
color = (0.3, 0.4 ,0.5)

title('Title in a custom color', color = '#123456')

背景色
向matplotlib.pyplot.axes()/matplotlib.pyplot.subplot()提供一个 axisbg参数（axis background），设置坐标轴的背景色
matplotlib.pyplot.subplot(111, axisbg = (0.3, 0.4 ,0.5))
