import re
import time
import json
import random
from sqlTable import comments_db, site_db, relationship_db, hotel_db
from utils import produce_id

from requestMathod import get_request


class Crawl:
    first_url = 'https://m.mafengwo.cn/rest/hotel/hotels/?data_style=mobile&filter[mddid]=10290&filter[area_id]=-1&filter[poi_id]=&filter[distance]=10000&filter[check_in]=2020-07-09&filter[check_out]=2020-07-10&filter[price_min]=&filter[price_max]=&filter[tag_ids]=&filter[sort_type]=comment&filter[sort_flag]=DESC&filter[has_booking_rooms]=0&filter[has_faved]=0&filter[keyword]=&filter[boundary]=0&page[mode]=sequential&page[boundary]=@&page[num]=20&_ts=1590837534480&_sn=f38abb4436'

    def __index__(self):
        self.root = ''
        self.firstHtml = ''

    # first 获取
    def first(self):
        for i in range(10):
            i = i * 20
            hotel_url = self.first_url.replace('@', str(i))
            print(hotel_url)
            time.sleep(random.random() * 1.6 + 2)
            origin_result = get_request(hotel_url, isJson=True, isPrient=False)
            resList = origin_result.get('data').get('list')
            for item in resList:
                hotel_id = item.get('id')
                name = item.get('name')
                num_comment = item.get('num_comment')
                price = item.get('price')
                img = item.get('img_w100_h100')
                comment_keyword_list = item.get('comment_keyword_list')
                keywords = json.dumps(comment_keyword_list, ensure_ascii=False)
                try:
                    rank = item.get('comment_rank_detail').get('hotel_score').get('rank')
                    score = item.get('comment_rank_detail').get('hotel_score').get('score')
                except Exception as e:
                    rank = ''
                    score = ''
                is_exist = hotel_db.select_sql(target=['id'], sqlFilter=f'where id = {hotel_id}')
                if not is_exist:
                    data = [hotel_id, name, price, img, num_comment, keywords, rank, score]
                    target = ['id', 'hotel_name', 'price', 'img', 'comment_num', 'keywords', 'hotel_rank',
                              'hotel_score']
                    hotel_db.insert_sql(targetField=target, data=data)

new = Crawl()

new.first()
# new.second()
# print(allSite, '\n', len(allSite))
