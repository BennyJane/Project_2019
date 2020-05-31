import re
import time
import json
import random
from sqlTable import comments_db, site_db, relationship_db, hotel_db
from utils import produce_id

from requestMathod import get_request, get_request_text


class Crawl:
    # first_url = 'https://m.mafengwo.cn/jd/10290/gonglve.html'
    first_url = 'https://m.mafengwo.cn/jd/10290/gonglve.html?page=@&is_ajax=1'
    second_url = 'https://m.mafengwo.cn/poi/{}.html'

    def __index__(self):
        self.root = ''
        self.firstHtml = ''

    # first 获取
    def first(self):
        for i in range(1, 10):
            site_url = self.first_url.replace('@', str(i))
            print(site_url)
            time.sleep(random.random() * 1.6 + 2)
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
                is_exist = site_db.select_sql(target=['id'], sqlFilter=f'where id = {site_id}')
                if not is_exist:
                    data = [site_id, site_name, description, num_comment, rank, site_img, site_imgs, num_ginfo]
                    target = ['id', 'site_name', 'brief', 'num_comment','rank','img', 'imgs', 'num_ginfo']
                    site_db.insert_sql(target, data)
        # break


new = Crawl()

new.first()
# new.second()
# print(allSite, '\n', len(allSite))
