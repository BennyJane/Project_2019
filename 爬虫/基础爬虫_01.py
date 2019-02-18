#01


程序 URLManager.py
--------------------------------------------
#coding:urf-8

class UrlManager(object):
	def __init__(self):
		self.new_urls = set()
		self.old_urls = set()
	
	def has_new_url(self):
	''' 判断是否有未爬取的URL'''
		return self.new_urls_size() != 0
	
	def get_new_urls(self)：
		new_url = self.new_urls.pop()
		self.olf_urls.add(new_url)
		return new_url
	
	def add_new_url(self, url):
	'''将新获得的URL，添加到未爬取的URL集合中 '''
		if url is None:
			return
		if url not in self.new_urls and url not in self.old_urls:		#判断URL不在已有两个集合中
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


数据储存器
--------------------------------------------


DataOutput.py程序

# coding:utf-8
import codecs

class DataOutput(object):
	
	def __init__(self):	
		self.datas=[]
'''第一个方法：
store_data(self,data)将解析出来的数据储存到内存中
'''
	def store_data(self,data):
		if data is None:
			return
		self.datas.append(data)
'''第一个方法：
output_html(self) 将储存到数据输出为指定的文件格式，
本案例中，将数据输出为HTML格式
'''
	def output_html(self):
		fout = codecs.open('baike.html', 'w', encoding='utf-8')
		fout.write("<html>")
		fout.write("<body>")
		fout.write("<table>")
		for data in self.datas:
			fout.write("<tr>")
			fout.write("<td>%s</td>"%data['url'])
			fout.write("<td>%s</td>"%data['title'])
			fout.write("<td>%s</td>"%data['summary'])
			fout.write("<tr>")
			self.datas.remove(data)
		fout.write("</table>")
		fout.write("</body>")
		fout.write("/html")
		fout.close

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
		self.manager = UrlManager()
		self.downloader = HtmlDownloader()
		self.parser = HtmlParser()
		self.output = DataOutput()
		
	def crawl(self, root_url):
		#调用函数
		self.manager.add_new_url(root_url)
		while(self.manager.has_new_url() and self.manager.old_url_size()<100):
			try:
				new_url = self.manager.get_new_url()
				html = self.downloader.download(new_url)
				new_urls, data = self.parser.parser(new_url, html)
				self.manager.add_new_urls(new_urls)
				self.output.store_data(data)
				print("已经抓取%s个链接"%self.manager.old_url_size())
			except:
				print("crawl failed")
		self.output.ouput_html()

if __name__ == "__main__":
	spider_man = SpiderMan()
	spider_man.crwal("http://baike.baidu.com/view/284853.htm")





































# end
