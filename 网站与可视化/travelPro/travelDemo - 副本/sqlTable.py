from sql import sqlFunc
import pymysql

pymysql.install_as_MySQLdb()

'''
================================================================
数据库链接配置
================================================================
'''
bin_db_conf: dict = dict(
    host='127.0.0.1',
    user='root',
    password='123456',
    db='travel',
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
comments = pymysql.escape_string('comments')
comments_db = sqlFunc(comments, **bin_db_conf)

# 配置数据库
siteAndComment = pymysql.escape_string('siteandcomment')
relationship_db = sqlFunc(siteAndComment, **bin_db_conf)

# 配置数据库
site = pymysql.escape_string('site')
site_db = sqlFunc(site, **bin_db_conf)

# 配置数据库
hotel = pymysql.escape_string('hotel')
hotel_db = sqlFunc(hotel, **bin_db_conf)

# 配置数据库
user = pymysql.escape_string('user')
user_db = sqlFunc(user, **bin_db_conf)
