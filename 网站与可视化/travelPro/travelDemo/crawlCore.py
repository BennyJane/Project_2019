import re
import time
import json
import random
from requestMathod import get_request_text


class Crawl:
    first_url = 'https://m.mafengwo.cn/jd/10290/gonglve.html?page=@&is_ajax=1'
    crawledUrl = []

    def __init__(self):
        self.root = ''
        self.firstHtml = ''
        self.isCrawling = False

    # first 获取
    def first(self):
        print('启动爬虫 ==================================')
        self.isCrawling = True
        self.crawledUrl = []
        for i in range(1, 20):
            site_url = self.first_url.replace('@', str(i))
            print(site_url)
            if site_url not in self.crawledUrl:
                self.crawledUrl.append(site_url)
            time.sleep(random.random() * 1.2 + 0.5)
            root = get_request_text(site_url, isPrient=False)
            res = re.findall(r'mapponints = (\[\{.*\}\])', root)
            res = json.loads(res[0])
            for item in res:
                # print(item)
                site_id = item.get('id')
                site_name = item.get('name')
                site_img = item.get('img')
                num_comment = item.get('num_comment')
                rank = item.get('rank')
                description = item.get('description')
                site_imgs = item.get('imgs')
                site_imgs = json.dumps(site_imgs, ensure_ascii=False)
                num_ginfo = item.get('num_ginfo')

                data = [site_id, site_name, description, num_comment, rank, site_img, site_imgs, num_ginfo]
                # print(data)

                # fixme 数据存储
                # is_exist = site_db.select_sql(target=['id'], sqlFilter=f'where id = {site_id}')
                # if not is_exist:
                #     data = [site_id, site_name, description, num_comment, rank, site_img, site_imgs, num_ginfo]
                #     target = ['id', 'site_name', 'brief', 'num_comment','rank','img', 'imgs', 'num_ginfo']
                #     site_db.insert_sql(target, data)
        self.isCrawling = False

    def crawlUrls(self):
        return self.crawledUrl



crawlCore = Crawl()