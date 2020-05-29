# import json
# import random
# import re
# import time
# from pprint import pprint
import re

from crawlData.requestMathod import get_request


# import pandas as pd
# from crawlData.utils import produce_id
# from crawlData.sqlTable import wos_group_db


class Crawl:
    origin_url = 'https://www.mafengwo.cn/ajax/router.php?sAct=KMdd_StructWebAjax%7CGetPoisByTag&iMddid=10290&iTagId=0&iPage=1&_ts=1590709009765&_sn=a8e7453f50'
    detail_info_url = 'https://www.mafengwo.cn/poi/{}.html'

    def __init__(self):
        self.root = ''
        self.pageDict = {}
        self.detailPageId = []

    def core(self):
        self.getPageList()
        self.detailInfo()

    def getPageList(self):
        # for i in range(1,7):
        #     url = self.origin_url.replace('@', str(i))
        #     print(url)
        #     self.pageDict = get_request(url, isJson=True, isPrient=True)
        #     self.getUrlId()

        self.pageDict = get_request(self.origin_url, isJson=True, isPrient=False)
        self.getUrlId()
        # site = self.site(isPrint=True)

    def getUrlId(self):
        label_str = self.pageDict.get('data').get('list')
        ids = re.findall(r'/poi/([\d]*).html', label_str)
        self.detailPageId.extend(ids)

    def detailInfo(self):
        for id in self.detailPageId:
            url = self.detail_info_url.format(id)
            print(url)
            token = {
                'Cookie':'__jsluid_s=06dda8107212fae3e918cd3df4fc4865; mfw_uuid=5ecefe2c-00c6-fd0f-ab0d-1acc30ef94e1; oad_n=a%3A3%3A%7Bs%3A3%3A%22oid%22%3Bi%3A1029%3Bs%3A2%3A%22dm%22%3Bs%3A15%3A%22www.mafengwo.cn%22%3Bs%3A2%3A%22ft%22%3Bs%3A19%3A%222020-05-28+07%3A56%3A28%22%3B%7D; __mfwc=direct; uva=s%3A92%3A%22a%3A3%3A%7Bs%3A2%3A%22lt%22%3Bi%3A1590623788%3Bs%3A10%3A%22last_refer%22%3Bs%3A24%3A%22https%3A%2F%2Fwww.mafengwo.cn%2F%22%3Bs%3A5%3A%22rhost%22%3BN%3B%7D%22%3B; __mfwurd=a%3A3%3A%7Bs%3A6%3A%22f_time%22%3Bi%3A1590623788%3Bs%3A9%3A%22f_rdomain%22%3Bs%3A15%3A%22www.mafengwo.cn%22%3Bs%3A6%3A%22f_host%22%3Bs%3A3%3A%22www%22%3B%7D; __mfwuuid=5ecefe2c-00c6-fd0f-ab0d-1acc30ef94e1; UM_distinctid=1725890e08b340-0c5960dbeacf3d-d373666-1fa400-1725890e08c52b; __jsluid_h=aa82e9b115a9ecf973262c2e38284085; __omc_chl=; __omc_r=; PHPSESSID=c9rehpdtphbilgjpj78e7fkoo0; Hm_lvt_8288b2ed37e5bc9b4c9f7008798d2de0=1590623789,1590665348; __jsl_clearance=1590707539.269|0|%2BFog9zbcbYGonLUIUzQH68WHn98%3D; __mfwa=1590623788462.84316.4.1590678100854.1590707541444; __mfwlv=1590707541; __mfwvn=4; CNZZDATA30065558=cnzz_eid%3D1220731470-1590623168-https%253A%252F%252Fwww.mafengwo.cn%252F%26ntime%3D1590704576; bottom_ad_status=0; __mfwb=0e512400ce29.8.direct; __mfwlt=1590709431; Hm_lpvt_8288b2ed37e5bc9b4c9f7008798d2de0=1590709432'
            }
            self.root = get_request(url, isJson=False, isPrient=True, token=token)
            self.sietImg()
            break


        pass

    def site(self, isPrint=False):
        # /html/body/div[1]/div[1]/div/div[1]/div[3]/div[2]/div[1]/div[2]/div[1]/div[5]/span
        res = self.root.xpath(
            r'/html/body/div[1]/div[1]/div/div[1]/div[3]/div[2]/div[1]/div[2]/div[1]/div[5]/span//text()')[1]
        if res:
            if isPrint:
                print(res)
            return res
        return ''

    def detailUrl(self):
        res = self.root.xpath(r'//*[@id="_j_search_result_left"]/div[2]/div[2]/a[1]/@href')
        if res:
            res = res[0]
            print('url', res)
        return ''

    def sietImg(self):
        # /html/body/div[2]/div[3]/div[1]/div/a/div
        res = self.root.xpath(r'/html/body/div[2]/div[3]/div[1]/div/a/div//img/@src')
        if res:
            print('img_url', res)
        return ''


wos = Crawl()
wos.core()

import execjs
