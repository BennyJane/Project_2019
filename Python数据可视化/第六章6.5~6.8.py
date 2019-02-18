'目录'
6.5使用Basemap 地图工具包
6.6 使用google map api 在地图上绘制数据
6.7 生成captcha图像（验证码）



6.5 Basemap 地图工具包
本身不进行任何绘图工作，知识把给定的地理坐标转换到地图投影，并把数据传给matplotlib进行绘图
---------------------------------------------------------------------------
在指定的 long、lat、坐标对的特定区域 绘制简单的墨卡托投影（Mercator projection）

'''绘制地球上一个区域的地图 ''''

from mal_toolkits.basemap import Basemap		#toolkits
import matplotlib.pyplot as plt
import numpy as np

map = Basemap(projection ='merc',
				resolution = 'h',
				area_thresh = 0.1,
		llcrnrlon = -126.619875, llcrnrlat=31.354158,  
		urcrnrlon = -59.647219, urcrnrlat =47.517613)		
		#projection = '' ???
		#resolution = ''
		#area_thresh = ''
		#设定经纬范围
#海岸线
map.drawcoastlines()
#国家分界线
map.drawcountries()
#填充陆地 湖泊颜色
map.fillcontinents(color='coral', lake_color='aqua')
#边界线颜色填充
map.drawmapboundary(fill_color='aqua')

#meridian 子午线 经线
map.drawmeridians(np.arange(0, 360, 30))
#parallel 平行线 纬线
map.drawparallels(np.arange(-90, 90, 30))

plt.show()

						'包含上部代码'

Basemap 是一个大的代码转化器，把 经度 纬度 转化到当前地图投影中，
	需要一个包含 long/lat 的数据集合，并把它传递给Basemap，用来投影，再用matplotlib在地图上绘制
	*从'cities.shp' 'cities.shx' 文件中加载美国城市的坐标

from mal_toolkits.basemap import Basemap
import matplotlib.pyplot as plt 
import numpy as np

map = Basemap(projection= 'merc', resolution= 'h', area_thresh = '100', 
		llcrnrlon = -126.619875, llcrnrlat=31.354158,  
		urcrnrlon = -59.647219, urcrnrlat =47.517613)

#shapefile 文件，储存地位位置信息，包含 name.shp name.shx name.dpf 等同名文件 
shapeinfo= map.readshapefile('cities', 'cities')

#zip()打包，与较短列表同长，获取多个一维列表，对应索引号元素组成的列表；；zip(*list) 解压，将高维数组的对应索引号元素组成的列表
x, y = zip(*map.cities)

#bulid a list of US cities
city_names= []
for each in map.cities_info:
	if each['COUNTRY'] != 'US':
		city_names.append("")		#add NULL
	else:
		city_names.append(each['NAME'])


map.drawcoastlines()
map.drawcountries()
map.fillcontinents(color='coral', lake_color='aqua')
map.drawmapboundary(fill_color='aqua')
map.drawmeridians(np.arange(0, 360, 30))
map.drawparallels(np.arange(-90, 90, 30))

#draw city markers
map.scatter(x, y, 25, marker='o', zorder=10)
#scatter(x,y, s=20(大小), c='b'（颜色）, marker='o', cmap=None, norm=None（亮度）, vmin=None, vmax=None,alpha=None, linewidths=None, verts=N)

#plot labels at City coords
for city_label, city_x, city_y in zip(city_name, x, y):
	plt.text(city_x, city_y, city_label)

plt.title('Cities in USA')

plt.show()

'''补充
----------------------------------------
'zip'函数
>>>a = [1,2,3]
>>> b = [4,5,6]
>>> c = [4,5,6,7,8]
>>> zipped = zip(a,b)     # 打包为元组的列表
[(1, 4), (2, 5), (3, 6)]
>>> zip(a,c)              # 元素个数与最短的列表一致
[(1, 4), (2, 5), (3, 6)]
>>> zip(*zipped)          # 与 zip 相反，*zipped 可理解为解压，返回二维矩阵式
[(1, 2, 3), (4, 5, 6)]

查看Basemap支持的投影
>>>import mpl_toolkits.basemap
>>>print(mpl_toolkits.basemap)
projections(投影)

在放大地图上的特定区域时，我们会指定要显示的区域的 左下角 右上角 的经度和纬度
llcrnrlon	左下角经度
llcinrlat	左下角纬度
urcrnrlon	右上角纬度
urcrnrlat	右上角纬度

官方文档中使用的数据格式 NetCDF格式
'''


6.6 使用google map api 在地图上绘制数据
	考虑将图表输出到Web页面
---------------------------------------------------------------------------
Web使用的主要语言 HTML CSS JavaScrit； 可以使用python 获取数据、处理数据、执行密集的运算，
	以及把数据渲染成适用于Web输出的格式，即 使用要求的 JavaScript 版本创建HTML页面来完成可视化工作

准备工作：
	1，需要安装 google-visuallization-python 模块
	2，使用 google数据可视化库 为前台界面准备数据
	3，使用 Google可视化API 在要求的可视化平台，也就是在地图和表格中渲染数据

import csv
import gviz_api

#创建模版生成器 template模版 样板
def get_page_template():
	page_template = """
	<html>
	  //加载Google的Javascript Api
	  <script src="https://wwww.google.com/jsapi" type="text/javascript"></script>
	  <script>
	    //加载Google数据可视化库 and 所需要的包 geochart table
	    google.load('visualization', '1', {packages:['geochart', 'table']});
	    
	    //设置一个函数，该函数在页面加载时会被调用，在Web世界中该事件被注册为onLoad，因此回调函数通过setonloadcallback函数进行设置
	    google.setOnLoadCallback(drawMap);
	    function drawMap()  {
	        //当页面加载时，Google实例将调用我们定义的自定义函数drawMap()，drawMap函数把一个JSON字符串加载到Datatable实例到JavaScript版本中
	    	var json_data = new google.visualization.Datatable(%s,0.6);
	    	
	    	var options = {colorAxis: {colors: ['#eee', 'green']}};
	    	//在ID为map_div的HTML元素中 创建一个geochart实例
	    	var mymap = new google.visualization.GeoChart(
	    						document.getElementById('map_div'));
	    	//用json_data 绘制地图，并且提供自定义的options
	    	mymap.draw(json_data, options);
	    	//在地图下面渲染出Google的JavaScript表
	    	var mytable = new google.visulization.Table(document.getElementById('table_div'));
	    	mytable.draw(json_data, {showRowNumber: true})
		}
	  </script>
	  <body>
	    <H1>Median Monthly Disposables Salary World Countries</H1>
	    
	    <div id= 'map_div'></div>
	    <hr />
	    <div id="table_div"></div>
	    
	    <div id="source">
	    <hr />
	    <small>
	    Source:
	    <a href="http://www.numbeo.com/cost-of-living/prices_by_country.jsp? dispalyCurrency=EUR&itemId=105">
	    href=http://www.numbeo.com/cost-of-living/prices_by_country.jsp? dispalyCurrency=EUR&itemId=105
	    </a>
	    </small>
	    </div>
	  </body>
	</html>
	"""
	return page_template

def main():
	#load data from CSV file,本地文件 从公共网站 www.numbeo.com获取数据，并将其储存为CSV格式
	afile = "median-dpi-countries.csv"
	datarows = []
	with open(afile, 'r') as f:
		reader = csv.reader(f)
		reader.next()		#skip header
		for row in reader:
			datarows.append(row)

	#Describe data，为了使用Google数据可视化库，指定ID 数据类型 可选标签
	#{"name": ("data_type", "Label")}
	description = { "country": ("string", "Country"),
					"dpi": ("number", "EUR")}		#eur 欧元

	#build list of dictionaries from loaded data,每条信息独立为字典形式，再构成列表
	data=[]
	for each in datarows:
		data.append({"country": each[0], "dpi": (float(each[1]), each[1])})		#两个each[1]??
	
	#instantizte（举例 示例） datatable with structure defined in 'description'
	#gviz_api.DataTable()依照description结构创建一个实例
	data_table = gviz_api.DataTable(description)
	
	#load i into gviz_api.DataTable 将数据加载到data_table中
	data_table.LoadData(data)
	
	#creating a JSon string 将数据输出为json格式
	#Tojson() 函数
	json = data_table.ToJSon(columns_order=("country", "dpi"),
							order_by="country",)
	
	#put json string into the template and save to output.heml 导出到文件html
	with open('output.html', 'w') as out:
		out.write(get_page_template() % (json,))

if __name__ == '__main__':
	main()

'补充'
''' 
HTML知识：




'''







6.7 生成captcha图像（验证码）
	利用python的图像库来生成图像 渲染点 线，渲染文本
---------------------------------------------------------------------------
from PIL import Image, ImageDraw, ImageFont
import random
import string

#定义类，容纳将来的异常类型
class AimpleCaptchaException(Exception):
	pass


class SimpleCaptcha(object):
	def __int__(self, length=5, size=(200, 100), fontsize=36, random_text=None, random_bgcolor=None):
		self.size= size
		#why not is random_text? 定义各个函数值的默认值
		self.text= "CAPTCHA"
		self.fontsize = fontsize
		#random_bgcolor 为什么不是这个名字
		self.bgcolor = 255
		self.length = length
		
		self.image = None # current captcha image
		
		#如果random_text为true，给self.text赋值
		if random_text:
			self.text = self._random_text()
		
		if not self.text:		#if not··· 如果为空（false）
			raise SimpleCaptchaException("Field text must not be empty.")
		
		if not self.size:
			raise SimpleCaptchaException("Size must not be empty.")
		
		if not self.fontsize:
			raise SimpleCaptchaException("Font size must not be defined.")
			
		if random_bgcolor:
			self.bgcolor = self._random_color()
		
	def _center_coords(self, draw):
		#？确认位置，size[0] 宽度，
		width, height = draw.textsize(self.text, font)		#随机文字的宽高
		xy = (self.size[0] - width) / 2 , (self.size[1] - height) / 2
		return xy
	
	#添加随机点
	def _add_noise_dots(self, draw):
		size = self.image.size
		for _ in range(int(size[0]*size[1]*0.1))：
			draw.point((random.randint(0, size[0]),
			random.randint(0, size[1])),
			fill = "white" )
		return draw
	
	def _add_noise_lines(self, draw):
		size= self.image.size
		for _ in range(8):
			width = random.randint(1, 2)
			#起点坐标（0，图片高度） 终点坐标（图片宽度，图片高度）
			start = (0, random.randint(0, size[1] - 1))
			end = (size[0], random.randint(0, siez[1] - 1))
			draw.line([start, end], fill= "white", width= width)
		for _ in range(8):
		    #画倾斜的曲线，定点 + 动点
			start = (-50, 50)
			#终点 （图片高的+10， ）
			end = (size[0] + 10, random.randint(0, size[1]+10))
			draw.arc(start+end, 0, 360, fill="white")
		return draw


	def get_captcha(self, size=None, text=None, bgcolor=None):
		if text is not None:
			self.text = text
		if size is not None:
			self.size = size
		if bgcolor is not None:
			self.bgcolor = bgcolor
			
		self.image = Image.new('RGB', self.size, self.bgcolor)
		#Note that the font file must present or point to your OS' syttem font
		#Ex, on Mac the path shoulde be '/Library/Fonts/Tahoma.ttf'
		font = ImageFont.truetype('fonts/Vera.ttf', self.fontsize)
		draw = ImageDraw.Draw(self.image)
		xy = self._center_coords(draw, font)
		draw.text(xy=xy, text=self.text, font=font)
		
		#add some dot noise
		draw = self._add_noise_dots(draw)
		
		#add some random lines
		draw = self._add_noise_lines(draw)
		
		self.image.show()
		return self.image, self.text
		
	def _random_text(self):
		letters = string.ascii_lowercase + string.ascii_uppercase
		random_text = ""
		for _ in range(self.length):
			random_text += random.choice(letters)
			return random_text
	def _random_color(self):
		r = random.randint(0, 255)
		g = random.randint(0, 255)
		b = random.randint(0, 255)
		return (r, g, b)

if __name__ == "__main__":
	sc = SimpleCaptcha(length= 7, fontsize=36, random_text=Ture, random_bgcolor=True)
	sc.get_captcha()






































-------------
