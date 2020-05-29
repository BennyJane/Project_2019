from crawlData.sql import sqlFunc
import pymysql

pymysql.install_as_MySQLdb()

'''
================================================================
数据库链接配置
================================================================
'''
bin_db_conf: dict = dict(
    host='192.168.1.124',
    user='root',
    password='123456',
    db='bin_db',
    port=3306,
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor,
    autocommit=True
)

'''
================================================================
数据表链接
================================================================
'''
# 配置数据库
wos_group = pymysql.escape_string('wos_group')
wos_group_db = sqlFunc(wos_group, **bin_db_conf)
