import requests
from loguru import logger
import pymysql
import json
import re
from pprint import pprint
import chardet
from lxml import etree

oprea_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36 OPR/63.0.3368.107'
huohu_user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0'
CHROME_USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'


def get_request_text(url, isPrient=False, token=''):
    headers = {'User-Agent': CHROME_USER_AGENT,
               "Accept":"application/json, text/javascript, */*; q=0.01",
               'enc': 'UTF-8'
               }
    if token:
        headers.update(token)
    try:
        r = requests.get(url,
                         headers=headers,
                         timeout=50,
                         )
        if r.status_code != 200:
            print('status_code', r.status_code)
            logger.debug("请求失败")
        # print(r.apparent_encoding)
        # print(r.encoding)
        #
        # # 转码
        # r.encoding = 'UTF-8'
        # root = r.text.encode(r.encoding).decode(r.apparent_encoding)
        # res = re.findall(r'mapponints = (\[\{.*\}\])', root)
        # print(res)
        if isPrient:
            print(r.text)
        root = r.text
    except Exception as e:
        root = ''
        logger.debug('get_requests: ', e)
    return root


def get_request(url, isJson=False, isPrient=False, token=''):
    headers = {'User-Agent': CHROME_USER_AGENT,
               }
    if token:
        headers.update(token)
    try:
        r = requests.get(url,
                         headers=headers,
                         timeout=50,
                         )
        if r.status_code != 200:
            print('status_code', r.status_code)
            logger.debug("请求失败")
        # r.encoding = 'utf-8'
        if isPrient:
            print(r.text)
        if isJson:
            root = json.loads(r.text)
        else:
            root = etree.HTML(r.text)
    except Exception as e:
        root = ''
        logger.debug('get_requests: ', e)
    return root


def get_json_text(url, isPrient=False):
    headers = {'User-Agent': CHROME_USER_AGENT,
               }
    try:
        r = requests.get(url,
                         headers=headers,
                         timeout=50,
                         )
        if r.status_code != 200:
            # print('status_code', r.status_code)
            logger.debug("请求失败")
        r.encoding = 'utf-8'
        if isPrient:
            print(r.text)
        root = r.text
    except Exception as e:
        root = ''
        logger.debug('get_requests: ', e)
    return root


def postRequest(url, params='', isJson=False, isPrint=False, authorization=''):
    headers = {'User-Agent': CHROME_USER_AGENT,
               'Content-Type': 'application/json',
               }
    if authorization:
        headers.update(authorization)
    try:
        r = requests.post(url,
                          headers=headers,
                          timeout=10,
                          data=params
                          )
        if r.status_code != 200:
            print('status_code', r.status_code)
            logger.debug("请求失败")
        if isPrint:
            print(r.text)
            print(r.get('authorization'))
        if isJson:
            root = json.loads(r.text)
        else:
            root = etree.HTML(r.text)
    except Exception as e:
        root = ''
        logger.debug('get_requests: ', e)
    return root


def get_request_root(url, isShow=False):
    headers = {'User-Agent': CHROME_USER_AGENT,
               }
    try:
        r = requests.get(url,
                         headers=headers,
                         timeout=50,
                         )
        if r.status_code != 200:
            # print('status_code', r.status_code)
            logger.debug("请求失败")
        if isShow:
            print(r.text)
        root = etree.HTML(r.text)
    except Exception as e:
        root = ''
        logger.debug('get_requests: ', e)
    return root
