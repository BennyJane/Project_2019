#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import time

from peewee import (
    Model as BaseModel,
    DoesNotExist,
    PrimaryKeyField,
    CharField,
    TextField
)
from playhouse import pool

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tmt.v20180321 import tmt_client, models

"""
    学术会议数据翻译
"""
### 腾讯开发者配置
TENCENT_DEVELOPER_CONFIG = dict(
    secret_id='AKIDkHYgjWsWp9D3e4vAoIWZNO4ZonZeH4UQ',
    secret_key='oNfhtqXy4UfgRv97tU8WeHxiX9UH8LJE'
)
### Mysql数据库配置 ====> 字典数据格式
MYSQL_CONFIG = dict(
    host='192.168.1.124',
    port=3306,
    dbname='bin_db',
    user='root',
    password='123456'
)
### mysql连接池 ====> 调用字典内数据
database = pool.PooledMySQLDatabase(
    database=MYSQL_CONFIG['dbname'],
    host=MYSQL_CONFIG['host'],
    port=MYSQL_CONFIG['port'],
    user=MYSQL_CONFIG['user'],
    password=MYSQL_CONFIG['password'],
    max_connections=30
)

"""
    数据库模型
"""


class Model(BaseModel):
    class Meta:
        database = database

    @classmethod
    def findExists(cls, *query, **filters):
        try:
            cls.get(*query, **filters)
            return True  # 存在
        except DoesNotExist:
            return False  # 不存在

    @staticmethod
    def close():
        try:
            database.close()
        except Exception as e:
            print(f'数据库关闭失败. 详细信息 [ {str(e)} ]')


"""
    En_table
"""


class En_table(Model):
    id = PrimaryKeyField()
    event_d = CharField(null=True, max_length=30)
    page_title = CharField(null=True, max_length=300)
    city = CharField(null=True, max_length=255)
    country = CharField(null=True, max_length=255)
    con_topic = CharField(null=True, max_length=255)

    class Meta:
        db_table = 'en_table'


"""
    Zh_table
"""


class Zh_table(Model):
    id = PrimaryKeyField()

    event_d = CharField(null=True, max_length=30)

    page_title = CharField(null=True, max_length=300)
    city = CharField(null=True, max_length=255)
    country = CharField(null=True, max_length=255)

    con_topic = CharField(null=True, max_length=255)

    class Meta:
        db_table = 'zh_table'


"""
    不能开多线程
    请求频率限制 ==> 5次/秒
"""


# 调用腾讯翻译api，输入待翻译的文字 translate_string
def translateString(translate_string):
    result = credential.Credential(
        secretId=TENCENT_DEVELOPER_CONFIG['secret_id'],
        secretKey=TENCENT_DEVELOPER_CONFIG['secret_key']
    )
    httpProfile = HttpProfile()
    httpProfile.endpoint = "tmt.tencentcloudapi.com"

    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = tmt_client.TmtClient(result, 'ap-shanghai')

    request = models.TextTranslateRequest()

    request.SourceText = str(translate_string)
    request.Source = 'en'
    request.Target = 'zh'
    request.ProjectId = 200

    response = client.TextTranslate(request)
    response_dict = dict(json.loads(response.to_json_string()))

    # 需要弄清楚翻译返回的数据格式
    if 'TargetText' in response_dict.keys():
        # 输出 translate_string, TargetText ===> 翻译后输出的文档

        print(f'[翻译] {translate_string} ===> {response_dict["TargetText"]}')
        return response_dict['TargetText']


def transCore(major):
    # 输入的选出来的每行数据
    try:
        num_pk = major.event_d
        page_title_result = translateString(major.page_title)
        city_result = translateString(major.city)
        country_result = translateString(major.country)
        # print(num_pk)

        # 储存翻译结果
        zh_table = Zh_table(
            event_d=num_pk,
            page_title=page_title_result,
            city=city_result,
            country=country_result,
            # con_topic = None,
        )
        zh_table.save()

    except TencentCloudSDKException as e:
        print(str(e))  # api提供的错误

    time.sleep(0.5)  # 避免过高的请求频率


def start():
    print(f'- start - : {time.time()}')

    # # 创建表
    if not En_table.table_exists():
        En_table.create_table()
    if not Zh_table.table_exists():
        Zh_table.create_table()


    # 提取表中所有需要翻译的对象
    majors = [major for major in En_table.select()]
    print(len(majors))
    # En_table.close()       #取完数据后，关掉数据库的链接

    for major in majors:
        #判断已经存在的会议不再翻译
        if not Zh_table.findExists(Zh_table.event_d == major.event_d):
            print(major.id)
            transCore(major)

    Zh_table.close()
    print(f'- done - : {time.time()}')


if __name__ == '__main__':
    start()
