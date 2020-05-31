import json

from sqlTable import comments_db, site_db, relationship_db, hotel_db, user_db


# 登录检验（用户名、密码验证）
def valid_login(username, password):
    is_exist = user_db.select_sql(target=['id'], sqlFilter=f'where username="{username}" and password ="{password}"')
    if is_exist:
        return True
    else:
        return False


# 注册检验（用户名、邮箱验证）
def valid_regist(username):
    is_exist = user_db.select_sql(target=['id'], sqlFilter=f'where username="{username}"')
    if is_exist:
        return False
    else:
        return True


def addUser(username, password):
    user_db.insert_sql(targetField=['username', 'password'], data=[username, password])


def getSite():
    allSite = site_db.select_sql(["*"], sqlFilter=f'order by num_comment desc limit 12')
    return allSite

def getManySite():
    allSite = site_db.select_sql(["*"], sqlFilter=f'where img != "" limit 16')
    return allSite

def getHotel():
    allHotel = hotel_db.select_sql(["*"], sqlFilter=f'order by price desc limit 16')
    return allHotel


def getContent(id):
    site = site_db.select_sql(["*"], sqlFilter=f'where id = "{id}"')
    return site