比较简单的主从模式，完全手工打造，不使用成熟的框架
	分布式进程
	进程间通信

控制节点(ControlNode)
	控制调度器
	URL管理器
	数据储存器

爬虫节点SpiderNode
	爬虫调度器
	HTML下载器
	HTML解析器


程序 URLManager.py
--------------------------------------------
	MD5处理

#coding:urf-8
class UrlManager(object):
	def __init__(self):
		self.new_urls =self.load_progress('new_urls.txt') 
		self.old_urls =self.load_progress('old_urls.txt')
	
	def has_new_url(self):
	''' 判断是否有未爬取的URL'''
		return self.new_urls_size() != 0
	
	def get_new_urls(self)：
	'''
	获取一个未爬取的URL
	'''
		new_url = self.new_urls.pop()
??
		m = hashlib.md5()
		m.update(new_url)
		self.olf_urls.add(m.hexdigest()[8:-8])
		return new_url
	
	def add_new_url(self, url):
	'''将新获得的URL，添加到未爬取的URL集合中 '''
		if url is None:
			return
??
		m = hashlib.md5()
		m.update(url)
		url_md5 = m.hexdigest()[8:-8]
??
		if url not in self.new_urls and url_md5 not in self.old_urls:		#判断URL不在已有两个集合中
			self.new_urls.add(url)

	def add_new_urls(self, urls):
	'''将多个新的URL添加到未爬取到URL集合中'''
		if urls is None or len(urls)==0:
			return
		for url in urls:
			self.add_new_url(url)	#调用 add_new_url()
	
	def new_url_size(slef):
	''' 获取未爬取URL集合的大小'''
		return len(self.new_urls)
	
	def old_url_size(self):
	''' 获取已爬取URL集合的大小'''
		return len(self.old_urls)
		
	def save_progress(self, path, data):
		with open(path, 'wb') as f:
			cPickle.dump(data, f)
	
	def load_progress(self, path):
		print('[+]从文件加载进度：%s' % path)
？？
		try:
			with open(path, 'rb') as f:
				tmp = cPickle.load(f)
				return tmp
		except:
			print('[!]无进度文件，创建： %s' % path)
		return set()	#返回set()集合？？




数据储存器
--------------------------------------------
DataOutput.py程序

# coding:utf-8
import codecs
import time

class DataOutput(object):
	
	def __init__(self):	
		self.filepath='baike_%s.html'%(time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime()))
		self.output_head(self.filepath)
		self.datas=[]
'''第一个方法：
store_data(self,data)将解析出来的数据储存到内存中
'''
	def store_data(self,data):
		if data is None:
			return
		self.datas.append(data)
		if len(self.datas)>10:
			self.output_html(self.filepath)

	def output_head(self, path):
	'''
	将HTML头写进去
	'''
		fout = codecs.open(path, 'w', encoding = 'utf-8')
		fout.write("<html>")
		fout.write("<body>")
		fout.write("<table>")
		fout.close()


'''第一个方法：
output_html(self) 将储存到数据输出为指定的文件格式，
本案例中，将数据输出为HTML格式
'''
	def output_html(self):
		fout = codecs.open(path, 'a', encoding='utf-8')
		for data in self.datas:
			fout.write("<tr>")
			fout.write("<td>%s</td>"%data['url'])
			fout.write("<td>%s</td>"%data['title'])
			fout.write("<td>%s</td>"%data['summary'])
			fout.write("<tr>")
			self.datas.remove(data)
		fout.close()

	def output_end(self, path):
		fout = codecs.open(path, 'a', encoding='utf-8')
		fout.write("</table>")
		fout.write("</body>")
		fout.write("/html")
		fout.close


控制调度器
---------------------------------------------
分布式管理器

	def start_Manager(self, url_q, result_q):
	'''
	把创建的两个队列注册在网络上，利用register方法，callable参数关联了Queue对象，将Queue对象在网络中暴露
	'''
		BaseManager.register('get_task_queue', callable=lambda:url_q)
	BaseManager.register('get_result_queue',callable=lambda:result_q)
	#绑定端口8001，设置验证口令"baike"，相当于对象的初始化
		manager=BaseManager(address=('', 8001), authkey='baike')
		return manager
	
	def url_manager_proc(self, url_q, conn_q, root_url):
		url_manager = UrlManager()
		url_manager.add_new_url(root_url)
		while True:
			while(url_manager.has_new_url()):
				new_url = url_manager.get_new_url()
				url_q.put(nuw_url)
				print('olf_url=', url_manager.old_url_size())
				if (url_manager.old_url_size()>2000):
					url_q.put('end')
					print("控制节点发起结束通知")
					url_manager.save_progress("new_urls.txt", url_manager.new_urls)
					url_manager.savr_progress('old_urls.txt', url_manager.old_urls)
					return
				try:
					if not conn_q.empty():
						urls = conn_q.get()
						url_manager.add_new_urls(urls)
				except:
					time.sleep(0.1)


	def result_solve_proc(self, result_q, conn_q, store_q):
		while(True):
			try:
				if not result_q.empty():
					content = result_q.get(True)
					if content['new_urls']=='end':
						print('结果分析进程接收通知然后结束')
						store_q.put('end')
						return
					conn_q.put(content['new_urls'])
					store_q.put(content['data'])
				else:
					time.sleep(0.1)
			except:
				tiem.sleep(0.1)

	def store_proc(self, store_q):
		output = DataOutput()
		while True:
			if not store_q.empty():
				data= store_q.get()
				if data == 'end':
					print('储存进度接受通知然后结束')
					output.output_end(output.filepath())
					
					return
				output.store_data(data)
			else:
				time.sleep(0.1)


#启动
if __name__ =='__main__':
	url_q = Queue()
	result_q = Queue()
	store_q = Queue()
	conn_q = Queue()
	
	node = NodeManager()
	manager = node.start_Manager(url_q, result_q)
	
	url_manager_proc = Process(target = node.url_manager_proc, args=(url_q, conn_q, 'http://baike.baidu.com/view/284853.html'))
	result_solve_proc = Process(target=node.result_solve_proc, args=(result_q, conn_q, store_q,))
	store_proc = Process(target=node.store_proc, args=(store_q,))
	
	url_manager_proc.start()
	result_solve_proc.start()
	store_proc.start()
	manager.get_server().serve_forever()



						"爬虫节点"

程序 HtmlDownloader.py
--------------------------------------------
	注意网页的编码，以保证下载的网页没有乱码

这里只需要实现一个借口： download(url)


#coding: utf-8
import requests
class HtmlDownloader(object):
	
	def download(self, url):
		if url is None:
			return None
		user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
		headers = {'User-Agent':user_agent}
		#设置 请求头
		r = request.get(url, headers= headers)
		if r.status_code == 200:#查看请求状态，200为正常
			r.encoding='utf-8'
			return r.text
		return None




HTML解析器
----------------------
	<a></a> 标记中的href属性值只是一个相对网址，可以使用urlparse.urljoin()函数将 当前网址 相对网址 拼接成完整的URL路径
	HTML解析器，主要是提供一个Parser对外借口，输入参数为 当前页面的URL和HTML下载器返回的网页内容

#coding: utf-8

import rs
import urlparse
from bs4 import BeautifulSoup

class HtmlParser(object):

	def parser(self, page_url, html_cont):
	'''
	用于解析网页内容，抽取URL和数据
	：param page_url 下载网页的URL
	:param html_cont 下载的网页内容 ？
	:return 返回URL 数据
	'''
	if page_url is None or html_cont is None:
	#为空，不执行
		return 
	soup = BeautifulSoup(html_cont, 'hrml.parser', form_coding='utf-8')
	#设置解析方式，解码方式
	new_urls = self._get_new_urls(page_url,soup)
	#_get_new_urls() 定义的函数
	new_data = self._get_new_data(page_url,soup)
	return new_urls, new_data

	def _get_new_urls(self, page_url, soup):
	
		new_urls = set()
		links = soup.find_all('a', href=re.complie(r'/view/\d+\.htm'))
#links 是列表，links=find(title,p)
'''[<title>Page title</title>, 
<p id="firstpara" align="center">This is paragraph <b>one</b>.</p>, 
<p id="secondpara" align="blah">This is paragraph <b>two</b>.</p>]'''
		for link in links:
			#获取href的属性
			new_url = link['href']
??link['href'] 是什么意思
			new_full_url = urlparse.urljoin(page_url,new_url)
			new_urls.add(new_full_url)
		return new_urls
	
	def _get_new_data(self, page_url, soup):
		
		data = {}
		data['url'] = page_url
		title =soup.find('dd', class_='lemmaWgr-lemmaTitle-title').find('h1')
?		
		data['title'] = title.get_text()
		summary = soup.find('div', class_='lemma-summary')
		data['summary']= summary.get_text()
		
		return data



⚠️ '注意'
储存文件更好的做法：
	'将数据分批储存到文件中'；
	而'将所有文件都储存在内存中'，一次性写入文件容易使系统出现异常，造成数据丢失。

爬虫调度器
--------------------------------------------

#coding:utf-8
from firstSpider.DataOutput import DataOutput
from firstSpider.HtmlDownlodaer import HtmlDownloader
from firstSpider.HtmelParser import HtmlParser
from firstSpider.UrlManager import UrlManager

class SpiderMan(object):
	def __init__(self):
		BaseManager.register('get_task_queue')
		BaseManager.register('get_result_queue')
		
		server_addr = '127.0.0.1'
		print('Connect to server %s...' $ server_addr)
		
		self.m = BaseManager(address=(server_addr, 8001), authkey='baike')
		
		self.m.connect()
		
		self.task = self.m.get_task_queue()
		self.result = self.m.get_result_queue()
		
		self.downloader = HtmlDownloader()
		self.parser = HtmlParser()
		print('init finish')




	def crawl(self, root_url):
		while True:
			try:
				if not self.task.empty():
					url = self.task.get()
					
					if url == 'end':
						print('控制节点通知爬虫节点停止工作···')
						self.result.put({'new_urls':'end', 'data':'end'})
						return
					print('爬虫节点正在解析：%s'%url.encode(utf-8))
					content=self.downloader.download(url)
					new_urls, data = self.parser.parser(url, content)
					self.result.put({"new_urls":new_urls, "data":data})
			except:
				print("连接节点失败")
				return
			except Exception, e：
				print(e)
				print('Crawl fail')

if __name__ == "__main__":
	spider = SpiderMan()
	spider.crwal()


