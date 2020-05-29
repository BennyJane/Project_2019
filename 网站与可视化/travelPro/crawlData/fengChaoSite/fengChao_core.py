import datetime

from crawlData.fengChaoSite.fengChao_parse import Crawl

start_time = datetime.datetime.now()
from loguru import logger


if __name__ == '__main__':

    wos = Crawl()
    for i in range(1164, 1221):
        logger.info(f"当前抓取的页面:  {i}")
        end_time = datetime.datetime.now()
        during_time = (end_time - start_time).seconds
        print(during_time)
        # if during_time > 3600:
        #     break
        wos.core(page_id=i)
