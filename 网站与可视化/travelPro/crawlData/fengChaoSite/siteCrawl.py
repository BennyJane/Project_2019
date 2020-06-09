import re
import time
import json
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from lxml import etree
# 1.引入 ActionChains 类
from selenium.webdriver.common.action_chains import ActionChains
from sqlTable import comments_db, site_db, relationship_db
from utils import produce_id

options = webdriver.FirefoxOptions()
options.add_argument('-headless')
driver = webdriver.Firefox(firefox_options=options)  # Firefox浏览器

# driver = webdriver.Firefox()  # Firefox浏览器
# allSite = []
allSite = [
    # '/poi/29173.html',
    # '/poi/30296.html',
    # '/poi/6630786.html',
    # '/poi/7690103.html',
    # '/poi/6630768.html',
    # '/poi/30295.html',

    # '/poi/29173.html',
    # '/poi/30295.html',
    # '/poi/6496992.html',
    # '/poi/71730088.html',
    # '/poi/6496369.html',
    # '/poi/5435069.html',
    # '/poi/66489924.html',
    # '/poi/71730088.html'
    # '/poi/30331.html'
    #
    '/poi/1062707.html'
]


class newCrawl:
    first_url = 'https://www.mafengwo.cn/jd/10290/gonglve.html'
    origin_url = 'https://www.mafengwo.cn/poi/29173.html'
    detail_info_url = 'https://www.mafengwo.cn'

    def __index__(self):
        self.root = ''
        self.firstHtml = ''

    def request(self, url):
        wait = WebDriverWait(driver, 10)  # 超时时长为10s
        driver.get(url)  # 这次返回的是 521 相关的防爬js代码
        driver.get(url)  # 调用2次 browser.get 解决 521 问题
        Html = driver.page_source
        root = etree.HTML(Html)
        return root

    # first 获取
    def first(self):
        url = self.first_url
        wait = WebDriverWait(driver, 10)  # 超时时长为10s
        driver.get(url)  # 这次返回的是 521 相关的防爬js代码
        driver.get(url)  # 调用2次 browser.get 解决 521 问题
        self.firstHtml = driver.page_source
        root = etree.HTML(self.firstHtml)

        self.firstUrl(root)
        time.sleep(3)
        n = 0
        while n < 9:
            print(n)
            try:
                pre_handle = driver.current_window_handle
                print('handle now', pre_handle)
                nextPagebuttomElement = driver.find_element_by_xpath(r'/html/body/div[2]/div[4]/div/div[2]/div/a[6]')
                # print(nextPagebuttomElement.text)
                driver.execute_script("arguments[0].click();", nextPagebuttomElement)

                wait = WebDriverWait(driver, 10)  # 超时时长为10s
                time.sleep(4)
                html = driver.page_source
                root = etree.HTML(html)
                self.firstUrl(root)
                n += 1
            except Exception as e:
                print(e)
                print(f'当前抓取的页面{n}存在问题')

    def firstUrl(self, root):
        '''
        ['/poi/29173.html', '/poi/30296.html', '/poi/29175.html', '/poi/6630786.html', '/poi/7690103.html', '/poi/6630768.html', '/poi/30295.html', '/poi/29178.html', '/poi/30333.html', '/poi/6496992.html', '/poi/29180.html', '/poi/29187.html', '/poi/6496369.html', '/poi/29179.html', '/poi/71730088.html']
        '''
        site_urls = root.xpath(r'//*[@id="container"]/div[4]/div/div[1]/ul//@href')
        print('site_url: ', site_urls)
        if site_urls:
            for url in site_urls:
                allSite.append(url)
        return site_urls

    def second(self):
        # 获取详情页面内容
        for url in allSite:
            targetUrl = self.detail_info_url + url
            print('second', targetUrl)
            detailRoot = self.request(targetUrl)
            imgs = self.secondImg(detailRoot)
            img = json.dumps(imgs, ensure_ascii=False)
            name = self.secondTitle(detailRoot)
            brief = self.secondBrief(detailRoot)
            site = self.secondSite(detailRoot)
            site_id = produce_id()
            # 获取评论信息
            comment_num = self.commentNum(detailRoot)
            comment_category = self.commentCategory(detailRoot)

            other = {
                'comment_num': comment_num,
                'comment_category': comment_category
            }
            other = json.dumps(other, ensure_ascii=False)

            # fixme 数据存储
            is_exist = site_db.select_sql(target=['id'], sqlFilter=f"where site_name = '{name}'")[0]
            print('is_exist =============== ', is_exist)
            # if not is_exist and brief:
            #     data = [site_id, name, site, brief, img, other]
            #     target = ['id', 'site_name', 'site', 'brief', 'imgs', 'other']
            #     site_db.insert_sql(target, data)
            #
            #     for index in range(1, 16):
            #         comment_id = self.commentContent(detailRoot, index)
            #         data = [site_id, comment_id]
            #         target = ['site_id', 'comment_id']
            #         relationship_db.insert_sql(target, data)
            if is_exist:
                for index in range(1, 16):
                    comment_id = self.commentContent(detailRoot, index)
                    site_id = is_exist.get('id')
                    data = [site_id, comment_id]
                    target = ['site_id', 'comment_id']
                    relationship_db.insert_sql(target, data)
            driver.close()

    def secondImg(self, root):
        img = root.xpath(r'/html/body/div[2]/div[3]/div[1]/div/a/div//div/img/@src')
        # print(img)
        return img

    def secondTitle(self, root):
        res = root.xpath(r'/html/body/div[2]/div[2]/div/div[3]/h1/text()')
        if res:
            res = res[0].strip()
            # print(res)
            return res
        return ''

    def secondBrief(self, root):
        res = root.xpath(r'/html/body/div[2]/div[3]/div[2]/div//text()')
        if res:
            rres = [item.strip() for item in res]
            result = ' '.join(rres)
            # print(result)
            return result
        return ''

    def secondSite(self, root):
        res = root.xpath(r'/html/body/div[2]/div[3]/div[3]/div[1]//text()')
        if res:
            result = res[1].strip()
            # print(result)
            return result
        return ''

    def commentNum(self, root):
        res = root.xpath(r'/html/body/div[2]/div[4]/div/div/div[1]/span/em/text()')
        if res:
            res = res[0].strip()
            # print(res)
            return res
        return ''

    def commentCategory(self, root):
        res = root.xpath(r'/html/body/div[2]/div[4]/div/div/div[2]/ul//text()')
        if res:
            result = []
            for item in res:
                item = item.strip()
                if item and item != '全部':
                    result.append(item)
            # print(result)
            return result
        return ''

    def commentContent(self, root, index):

        user_name = root.xpath(r'/html/body/div[2]/div[4]/div/div/div[4]/div[1]/ul/li[{}]/a/text()'.format(index))
        if user_name:
            user_name = user_name[0]
        else:
            user_name = ''
        print('user_name', user_name)

        user_start = root.xpath(r'/html/body/div[2]/div[4]/div/div/div[4]/div[1]/ul/li[{}]/span/@class'.format(index))
        if user_start:
            user_start = user_start[0]
            user_start = re.findall(r'\d', user_start)[0]
        else:
            user_start = ''
        print('user_start', user_start)

        # /html/body/div[2]/div[4]/div/div/div[4]/div[1]/ul/li[1]/p
        user_comment = root.xpath(r'//p[@class="rev-txt"]/text()')
        print(user_comment)
        if user_comment:
            try:
                user_comment = user_comment[index].strip()
            except Exception as e:
                user_comment = ''
        else:
            user_comment = ''
        print('user_comment', user_comment)

        #
        xpath = '//*[@id="pagelet-block-183d2e4c3babbc689fa3368e9c17e4f8"]/div/div[4]/div[1]/ul/li[1]/div[3]/span[{}]/text()'.format(index)
        user_date = root.xpath(xpath)
        if user_date:
            user_date = user_date[index].strip()
        else:
            user_date = ''
        print('user_date', user_date)

        id = produce_id()

        # fixme 数据存储
        data = [id, user_name, user_start, user_date, user_comment]
        target = ['id', 'userName', 'goal', 'publishDate', 'message']
        comments_db.insert_sql(target, data)

        return id


new = newCrawl()

# new.first()
new.second()
# print(allSite, '\n', len(allSite))
