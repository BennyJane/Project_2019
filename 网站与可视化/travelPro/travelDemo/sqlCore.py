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


class sqlBase:

    def topFirst(self):
        # 获取评论数量前十的景区
        ten_site = site_db.select_sql(['site_name', 'num_comment'], sqlFilter=f"order by num_comment desc limit 10")
        ten_site = sorted(ten_site, key=lambda x: int(x['num_comment']), reverse=True)
        # 获取评分最高的10个酒店
        ten_hotel = hotel_db.select_sql(['hotel_name', 'comment_num'], sqlFilter=f"order by comment_num desc limit 10")
        ten_hotel = sorted(ten_hotel, key=lambda x: int(x['comment_num']), reverse=True)
        # 获取游记数量最多的10个地区
        ten_site_info = site_db.select_sql(['site_name', 'num_ginfo'], sqlFilter=f"order by num_ginfo desc limit 10")
        ten_site_info = sorted(ten_site_info, key=lambda x: int(x['num_ginfo']), reverse=True)
        print(ten_site_info)
        return ten_site, ten_hotel, ten_site_info

    def picData(self):
        ten_site = site_db.select_sql(['site_name', 'num_comment', 'num_ginfo'],
                                      sqlFilter=f"order by num_comment desc limit 14")
        ten_site = sorted(ten_site, key=lambda x: int(x['num_comment']), reverse=True)
        res = []
        for item in ten_site:
            temp = {
                'name': item['site_name'],
                'value1': item['num_comment'],
                'value2': item['num_ginfo'],
            }
            res.append(temp)
        return res
