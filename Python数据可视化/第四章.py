4.1 设置坐标轴标签的透明度与大小
---------------------------------------------------------
import matplotlib.pyplot as plt
from matplotlib import patheffects
import numpy as np

data = np.random.randn(70)

fontsize =18
plt.plot(data)

title = 'This is figure title'
x_label = 'This is x axis label'
y_label = 'This is y axis label'

title_text_obj = plt.title(title, fontsize=fontsize, verticalalignment='bottom')
	#垂直对齐方式：center top baseline
title_text_obj.set_path_effects([patheffects.withSimplePatchShadow()])
#为标题添加阴影效果
#matplotlib.patheffects.withSimplePatchShadow(),不带参数直接调用，默认参数为：offset_xy = (2,-2) shadow_rgbFace = None patch_alpha = 0.7
❓#路径效果（path effects）是matplotlib的matplotlib.pathefffects 模块的部分功能，支持matplotlib.text.Text 与 matplotlib.patches.Patch

offset_xy = [-1, 1]		#set the 'angle' of the shadow
rgbRed = (1.0, 0.0, 0.0)	#set the color of the shadow
alpha = 0.8				#setup the transparency of the shadow

pe = patheffects.withSimplePatchShadow(offset_xy = offset_xy, shadow_rgbFace = rgbRed, patch_alpha = alpha)
	#customize shadow properties
❓	#实例化matplotlib.patheffects.withSimplePatchShadow对象，并将其引用保存在pe变量中，以供后面的代码重用它。？？

4.3 为图表线条添加阴影
---------------------------------------------------------
	*为了向图表中的 线条 or 矩形 添加阴影，需要使用matplotlib中的transformation框架，位于 matplotlib.transforms模块中
❓	*Transformation 知道如何将给定的坐标 从其坐标系转化到 显示坐标系中，与指导如何将 坐标从显示坐标系转化到它们自己的坐标系中
		*该框架 允许把现有对象 转化为一个偏移对象 == 把对象放置到偏移原来对象一段距离的地方
	*坐标系 data Axes Figure Display 四种

import numpy as np
import matplotlib.pylot as plt
import matplotlib.transforms as transforms

def setup(layout=None):
	assert layout is not None
	
	fig = plt.figure()
	ax = fig.add_subplot(layout)
	return fig, ax 

def get_signal():
	t = np.arange(0, 2.5, 0.01)
	s = np.sin(5*np.pi*t)
	return t, s

def plot_signal(t, s):
	line = axes.plot(t, s, linewidth = 5, color = 'magenta')
	return line

def make_shadow(fig, axes, line, t, s):  ❓ 
	#偏移的值是以点为单位的，点尺寸 1/72英寸，想有偏移2pt，向下偏移2pt
	delta = 2/72 #how many points to move the shadow 
	offset = transforms.ScaledTranslation(delta, -delta, fig.dpi_scale_trans)	#设置偏移方向、距离；
	offset_transform = axes.transData + offset
	#创建了一个偏移对象，
	
	# we plot the same data, but now using offset transform
	# zorder -- to render it below the line
	axes.plot(t, s , linewidth=5, color='gray', transform=offset_transform, zorder=0.5*line.get_zorder())

if __name == "__main__":
	fig, axes = setup(111)
	t, s = get_signal()
	line = plot_signal(t, s)
	
	make_shadow(fig, axes, line, t, s)
	
	axes.set_title('Shadow effect using an offset transform')
	plt.show() 


4.4 向图标中添加数据表
---------------------------------------------------------
import matplotlib.pylot as plt
import numpy as np 

plt.figure()
ax = plt.gca()
y = np.random.randn(9)

col_labels = ['col1','col2','col3']
row_labels = ['row1','row2','row3']
table_vals = [[11,12,13],[21,22,23],[31,32,33]]
row_colors = ['red','gold','green']

my_table = plt.table(
				cellText = table_vals,
				colWidths=[0.1]*3,
				rowLabels=row_labels,
				colLabels=col_labels,
				rowColours=row_colors,
				loc='upper right')

plt.plot()
plt.show()

使用plt.table()方式，创建一个带单元格的表格，并把它添加到当前坐标轴中。
plt.table(cellText=Nont, cellColours=None,
		cellloc='right', colWidths=None,
		rowLabels=None, rowColours=None, rowLoc='left',
		colLabels=None, colColours=None, rowLoc='center',
		loc='bottom', bbox=None)
该函数返回一个matplotlib.table.Table 实例，
Axes.add_table(table)方法，把table实例添加到axes， 



4.4 使用subplots子区
---------------------------------------------------------
	*subplot 派生自axes？？
	*matplotlib.figure.SubplotParams类，包含了subplot的所有参数，尺寸是被归一化的图标的宽度 or 高度。
		#如果不指定 任何定制化的值，subplot将会从'rc'参数重读取参考值？？
	*matplotlib.pyplot.subplots()用来方便地创建普通布局的子区，指定网格的大小——子区网格的行数与列数
	*使用 sharex or sharey 关键字参数，创建共享x or y 轴的子区
		#sharex 参数可以设置为 True——x轴就被所有的子区共享，刻度标签只在最后一行的子区可见
			#也可以设置为 字符串，枚举值如 
			row：每一个子区行共享x轴坐标
			col：每一个子区共享y轴坐标
			all：== True，x轴被所有子区共享
			none：== False
	*matplotlib.pyplot.subplots_adjust 来调整子区的布局，
		#关键字参数指定 图中子区的坐标 left right bottom top
		#其值是归一化值的图标大小的值
		#可以用 wspace hspace参数，指定子区间空白区域的大小，数值为响应宽度和高度的归一化值
	* subplot2grid() 定义网格的几何形状 与 子区的位置，
		*⚠️位置是基于0， 而不是像在plot.subplot()中 基于1
		*可以使用 colspan or rowspan 来让子区跨越给定网格中的多个行与列
	*ax.get_xticklabels() 得到x轴的标签列表
	*subtitle（"name"）添加整个figure的标题
	*axes.set_title("name") 设置单个图标的标题

'创建图标，并通过subplot2grid天乩不同的子区布局，并重新配置刻度标签大小'

import matplotlib.pyplot as plt

plt.figure(0)
axes1 = plt.subplot2grid((3,3), (0,0), colspan=3)
axes1 = plt.subplot2grid((3,3), (1,0), colspan=2)
axes1 = plt.subplot2grid((3,3), (1,1))# colspan=1 默认是1
axes1 = plt.subplot2grid((3,3), (2,0))
axes1 = plt.subplot2grid((3,3), (2,1), colspan=2)

#tidy up tick labels size
all_axes = plt.gcf().axes
for ax in all_axes:
	for ticklabel in ax.get_xticklabels() + ax.get_yticklabels():
		ticklabel.set_fontsize(10)

plt.subtitle("Demo of subplot2grid")
plt.show()


			补充： 另一种定制化当前 axes or subplot 的例子：

axes = fig.add_subplot(111) #创建图标axes实例 
rectangle = axes.patch		#引用rectangle实例的patch❓
rectangle.set_facecolor('blue')
'注释'
	此字段，代表当前axes实例的背景，可以更新该实例的属性，进而更新axes的背景：改变颜色、加载图像、添加水印保护❓

*也可以，先创建一个补片（patches），再将其添加到axes的背景中

fig = plt.figure()
axes = fig.add_subplot(111)
rect = matplotlib.patches.Rectangle((1,1), width=6, height=12)		#（1，1）rectangle左下角坐标
axes.add_patche(rect)
#we have to. manually force a figure draw
axes.figure.canvas.draw()


4.4 定制化网格
---------------------------------------------------------
matplotlib.pyplot.grid（） 设置网格可见度、密度、风格、是否显示

plt.gird() 不调用参数，设置开关
	* 通过主刻度 次刻度 同时通过两个刻度来操作网格
		which 'major' 'minor' 'both'
	axis 分别控制着水平刻度 垂直刻度， 参考值 'x' 'y' 'both'

	*所有其他属性通过 'kwargs'参数传入，代表一个matplotlib.lines.Line2D实例可以接受的标准属性集合。 
ax.grid(color = 'g', linestyle='--', linewidth=1)

深入了解 matplotlib 与 mpl_toolkits 找到一个简单且可管理的方式创建坐标轴网格 AxesGrid

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid	#?
from matplotlib.cbook import get_sample_data	#?

#从matplotlib的样本数据目录中加载数据 ❓
def get_demo_image():
	f = get_simple_data("axes_grid/bivariate_normal.npy", asfileobj=False)
	#z is a numpy array of 15*15
	Z = np.load(f)
	return Z, (-3, 4, -4, 3) #同时返回了两个值

#grid列表保存了axes网格（此例子中是 ImageGrid）
#layout 图标代称，nrows_ncols 为 （x，y）
def get_grid(fig=None, layout=None, nrows_ncols=None):
	assert fig is not None
	assert layout is not None 
	assert nrows_ncols is not None
	#❓
	grid = ImageGrid(fig, layout, nrows_ncols=nrows_ncols, axes_pad=0.5, add_all=True, label_mode='L')
	#axes_pad 间距？ add_all 应用于所有图标 label_mode 
	return grid

#变量image1、image2、image3、保存了Z的切片数据，这些数据是根据gird列表的多个坐标轴切分的
#遍历所有网格，调用imshow()方法绘制image1···的数据，
#❓
def load_images_to_grid(grid, z, *images): #*images 重复
	min, max = Z.min(), Z.max()
	for i, image in enumerate(images):
		axes = grid[i]
		axes.imshow(image, origin='lower', vmin=min, vmax=max, interpolation='nearest')


if __name__ == "__main__":
	fig = plt.figure(1,(8.6))
	grid = get_grid(fig, 111, (1,3)) #一个表分了三段
	z, extent = get_demo_image()
	
	#Slice image
	image1 = Z
	image2 = Z[:, :10]
	image3 = Z[:, 10:] #❓怎么解释？
	
	load_images_to_gird(grid, Z, image1, image2, image3)
	
	plt.draw()
	plt.show()



4.7 绘制等值线
---------------------------------------------------------
Z矩阵的等高线图是由许多等高线表示，Z被视作相对于X-Y平面的高度，
	Z的最小值为2，并且必须包含至少两个不同的值。
	*X、Y、Z的形状、维度存在一定的限制，例如：
		X Y可以是二维的，与Z形状相同
		X Y如果是一维的，则X的长度等于Z的列数，Y的长度将等于Z的行数

等高线图要点：
	*必须添加标签
	*确定如何选择要绘制的等值线（isolines）数量（过密、过少）
函数：
	*标签 clabel() 
	*添加颜色 colormaps
	*contour() 绘制等高线
	*countourf() 绘制填充的等高线

import numpy as np
import matplotlib as mpl
import matplotlib.pylot as plt

def process_siganls(x, y):
	return (1 - (x ** 2 + y**2)) * np.exp(-y**3/3)

x = np.arange(-1.5, 1.5, 0.1)
x = np.arange(-1.5, 1.5, 0.1)

x, y = np.meshgrid(x, y)

z = process_signals(x, y)

# Number of isolines
N = np.arange(-1, 1.5, 0.3)

CS = plt.contour(Z, N, linewidth=2, cmap=mpl.cm.jet) 
	#颜色映射表?? ❓
plt.clabel(CS, inline=True, fmt='%1.1f', fontsize=10)
plt.colorbar(CS) #等高线的柱状图

plt.title("My function: $z=(1-x^2+y^2) e^{-(y^3)/3}$")
plt.show()




4.8 填充图表底层区域
---------------------------------------------------------
matplotlib.pyplot.fill:绘制一个填充多边形的基本方式
	接受的参数（与plot相似）：多个x、y对与其他Line2D属性，
	返回 '被添加Patch实例'的列表 ❓
matplotlib.pyplot.fill_between()
	*填充y轴的值之间的区域
	*接受参数 x（数据的x轴数组）与 y1 y2（数据的y轴数组），指定要填充的区域
	*条件为 布尔条件，通常指定y轴值范围，默认值为None，表示填充所有区域

matplotlib.pyplot.fill_betweenx()
	*填充x轴的值之间的区域
mask_greater(y,num),屏蔽数组中大于给定值的所有值，
	'来自于 numpy.ma包中的方法，用来处理缺失、无效的值'




import numpy as np
import matplotlib.pyplot as plt
from math import sprt

t = range(1000)
y = [sprt(i) for i in t]
plt.plot(t, y, color='red', lw=2)
plt.fill_between(t, y, color='silver')
plt.show()



4.9 绘制极线图
---------------------------------------------------------
数据需要先转化为 '极坐标' 的形式，才能用 极线图 来把它显示出来
	极坐标 半径（r） + 角度 （theta）：弧度、角度

'极线图' 通常用来显示本质上是 '射线'的信息
ploar()函数绘制极线图：
	*接收 两个长度相同的参数数组 theta 和 r
	*其他格式化参数
告诉matplotib坐标轴要在极限坐标系统中，这可以通过向add_axes or add_subplot 提供 ploar=True 参数来完成
matplotlib.pyplot.rgrids()
	切换半径网格的显示 or 设置标签
matplotlib.pyplot.thetagrid()
	配置角度刻度和标签
zip(list1，list2···)
	zip() 函数用于将可迭代的对象作为参数，将对象中对应的元素打包成一个个元组，然后返回由这些元组组成的对象，这样做的好处是节约了不少的内存。
	可以使用 list() 转换来输出列表。
	如果各个迭代器的元素个数不一致，则返回列表长度与最短的对象相同，利用 * 号操作符，可以将元组解压为列表。
lambda 表达式
	匿名函数lambda：是指一类无需定义标识符（函数名）的函数或子程序。 函数可以接收任意多个参数 (包括可选参数) 并且返回单个表达式的值。
a = lambda x,y,z:(x+8)*y-z
print(a(5,6,8))

>>>a = [1,2,3]
>>> b = [4,5,6]
>>> c = [4,5,6,7,8]
>>> zipped = zip(a,b)     # 返回一个对象
>>> zipped
<zip object at 0x103abc288>
>>> list(zipped)  # list() 转换为列表
[(1, 4), (2, 5), (3, 6)]
>>> list(zip(a,c))              # 元素个数与最短的列表一致
[(1, 4), (2, 5), (3, 6)]
 
>>> a1, a2 = zip(*zip(a,b))          # 与 zip 相反，zip(*) 可理解为解压，返回二维矩阵式
>>> list(a1)
[1, 2, 3]
>>> list(a2)
[4, 5, 6]




import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt

figsize = 7 
colormap = lambda r: cm.set2(r / 20 .) #参见colormap的使用方法
N = 18 # number of bars

fig = plt.figure(figsize=(figsize, figsize)) #700px*700px
ax = fig.add_axes([0.2, 0.2, 0.7, 0.7], polar=True) #??why is list?
 
theta = np.arange(0.0, 2 * np.pi, 2*np.pi/N)
radii = 20 * np.random.rand(N)
width = np.pi / 4 * np.random.rand(N) #生成极线条的宽度数据
bars = ax.bar(theta, radii, width=width, bottom=0.0)
#bar()函数，接收数组，所以不需要遍历整个数组
for r, bar in zip(radii, bars):		#zip（）
	bar.set_facecolor(colormap(r))
	bar.set_alpha(0.6)

plt.show()


4.10 使用极线条来可视化文件系统树
---------------------------------------------------------
步骤
1，实现一些helper函数来处理找到的文件夹 及其 内部的数据结构
2，实现绘图的主函数 draw()

import os
import matplotlib.pylot as plt
import matplotlib.cm as cm
import numpy as np

def build_folders(start_path):
	folders = []
	
	for each in get_directories(start_path):
		size = get_size(each)	#filename
		if size >= 25*1024*1024
			folders.append({'size': size, 'path': each})
	
	for each in folders:
		print("Path:" + os.path.basename(each['path']))
		#get pathname by filename 
		print("Size:" + str(each['size'] / 1024 / 1024) + "MB")	
	return folders

def get_size(path): #❓
	assert path is not None
	
	total_size = 0
	for dirpath, dirnames, filenames in os.walk(path):
		for f in filenames:
			fp = os.path.join(dirpath, f)
			try:
				size = os.path.getsize(fp)
				total_size += size
				#print "Size of '{0} is {1}".format(fp, size)"
			except OSError as err:
				print(srt(err))
				pass
	return total_size


def get_directories(path): #返回start_path下的子目录列表
	dirs = set()
	for dirpath, dirnames, filenames in os.walk(path):
	#dirpath 单一的 dirnames filenames 可能为多
		dirs = set([os.path.join(dirpath, x) for x in dirnames])
		break #we just want the first one
	return dirs


def draw(folders):
	"""Draw folder size for given folder"""
	figsize = (8, 8) #keep the figure square
	ldo, rup = 0.1, 0.8 #leftdown and right up normalized
	#❓
	fig = plt.figure(figsize = figsize)
	ax = fig.add_axes([ldo, ldo, rup, rup], polar = True)
	
	#transform data
	x = [os.path.basename(x['path']) for x in folders]
	y = [y['size'] / 1024 /1024 for y in folders]
	theta = np.arange(0.0, 2*np.pi, 2*np.pi / len(x))
	radii = y
	
	bars = ax.bar(theta, radii)
	middle = 90 / len(x) ？？
	theta_tiks = [t * (180 / np.pi) + middle for t in theta]
	lines, labels = plt.thetagrids(theta_ticks, labels=x, frac=0.5)
	for setp, each in enumatete(labels):
		each.set_rotation(theta[step] * (180 / np.pi + middle))
		each.set_fontsize(8)
	
	# configure bars
	colormap = lambda r: cm_set2(r / len(x))
	for r,each in zip(radii, bars):
		each.set_facecolor(colormap(x))
		each.set_alpha(0.5)
	
	plt.show()


3,接下来，实现main函数体

if __name__ == '__main__':
	if len(sys.argv) is not 2: #判断是否有输入路径？
		print("ERROR: Please supply path to folder.")
		sys.exit(-1)
	
	start_path = sys.argv[1] #sys.argv[0] 是文件本身
	
	if not os.path.exist(start_path): #路径不存在
		print("ERROR: Path must exist.")
		sys.exit(-1)
	
	folders = bulid_folders(start_path)
	if len(folders) < 1:
		print("ERROR: Path does not contain any folders.")
		sys.exit(-1)
	
	draw(folders)

在命令行输入命令：
$ python chO4_recll_filesystem.py /usr/lib/












------------------------------------------------------
