2.1 从CSV文件导入数据
----------------------------------------------------------

import csv

filename = 'ch02-data.csv'

data= []

try:
	with open(filename) as f: 			#将文件绑定到对象f
		reader = csv.reader(f)		#所有内容读取到reader，具体内容是什么样的？
	header = reader.next()		#py3 header=next(readre)
	data = [row for row in reader]	#?是否包含第一行？
except csv.Error as e:
	print("Error reading CSV file at line %s: %s" (reader.line_num, e))
	sys.exit(-1)				#？？

if header:
	print(header)
	print ('=================')
for datarow in data:
	print(datarow)

'注释'
	1 csv模块所有信息，查看PEP文档中的《CSV文件API》
	2 加载大数据文件，明智做法，使用其他库，例如NumPy的 loadtxt()方法：
		import numpy
		data=numpy.loadtxt('che02-data.csv',dtype='string', delimiter=',')
		#为了正确分割数据，需要定义分隔符。
	3 numpy.loadtxt() 要比类似的 numpy.genformtxt() 速度更快，但后者能 更好的处理缺失数据，在处理已加载文件的某些列时，可以使用一些方法来做额外的事情。


2.3 从Microsoft Excel 文件中导入数据
----------------------------------------------------------
思路：
	1 通常做法，把数据从Excle中导出到CSV格式的文件中，再将CSV导入Python ——————少量文件
	2 想自动化地对大量文件进行'数据管道处理' （做为数据连续处理流程中的一部分）—————— python包 'xlrd',仅能用于读取excle文件

import xlrd

file = 'ch02-xlsxdata.xlsx'
wb = xlrd.open_workbook(filename=file)
ws = wb.sheet_by_name(Sheet1)
dataset = []

for r in xrange(ws.nrows)
	col = []
	for c in range(ws.ncols)
		col.append(ws.cell(r , c).value)	#cell()方法，单元格
		dataset.append(col)
	
	form pprint import pprint
	ppritn(dataset)

Excle中 日期 的读取
日期是以浮点数，而不是以某个日期类型储存的。但，xlrd模块有能力检查数据的值，并推断出数据实际上是否是一个日期。
如果数字字符串像日期，xlrd模块将返回 'xlrd.XLCELL_DATE' 做为单元格类型。
——————这样，可以通过检查 单元格类型，得到 python date对象。

from datetime import datetime
from xlrd import open_workbook, xldate_as_tuple
...
cell = sheet.cell(1,0)
print(cell)
print(cell.value)
print(cell.ctype)
if cell.ctype == xlrd.XL_CELL_DATE:
	date_value = xldate_as_tuple(cell.value, book.datemode)		#
	print(datetiem(*date_value)) # * ？

源码查看

# @param xldate The Excel number
# @param datemode 0: 1900-based, 1: 1904-based.
xldate_as_tuple(xldate, datemode)  
输入一个日期类型的单元格会返回一个时间结构组成的元组，可以根据这个元组组成时间类型
datemode 有2个选项基本我们都会使用1900为基础的时间戳


# Convert an Excel date/time number into a datetime.datetime object.
#
# @param xldate The Excel number
# @param datemode 0: 1900-based, 1: 1904-based.
#
# @return a datetime.datetime() object.
#
def xldate_as_datetime(xldate, datemode)

'注释'
	1 ？？思考相反操作，将python数据转化为excle数据
	2 xlrd，非常好的特性： 按照需要仅加载文件的部分内容到内容中，open_workbook() 方法中有一个 'on_demand' 参数，调用时设置为 True，工作表就能按需要加载了。
	book = open_workbook('large.xls', on_demand=True)
	#?? 怎么设置特定的需要
	3 xlwt Excle的写的操作

----------------------------------------------------------

