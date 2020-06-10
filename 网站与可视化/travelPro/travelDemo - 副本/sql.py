import pymysql

pymysql.install_as_MySQLdb()
import pymysql.connections

import json
from loguru import logger

logger.add('./log/sql.log', level='DEBUG')

'''
---------------------------------------
处理 list 中的空字符串
---------------------------------------
'''


def del_str_none(text_list: list) -> list:
    temp = []
    for item in text_list:
        item = item.replace('\r\n', '').strip()
        if item:
            temp.append(item)
    return temp


'''
---------------------------------------
封装sql语句:
参数host：连接的mysql主机，如果本机是'localhost'
参数port：连接的mysql主机的端口，默认是3306
参数db：数据库的名称
参数user：连接的用户名
参数password：连接的密码
参数charset：通信采用的编码方式，默认是'gb2312'，要求与数据库创建时指定的编码一致，否则中文会乱码
charset='utf8',
参数cursorclass： 返回的数据默认为元组， 可以设置为字典格式
cursorclass=pymysql.cursors.DictCursor
---------------------------------------
'''
# table_name = pymysql.escape_string('letPub_journal')
# mysql_conf: dict = dict(
#     host='192.168.1.124',
#     user='root',
#     password='123456',
#     # 需要指明数据库
#     database='bin_db',
#     port=3306,
#     chartset='utf-8'
# )

# home mysql
table_name = pymysql.escape_string('letpub')
mysql_conf: dict = dict(
    host='localhost',
    user='root',
    password='123456',
    db='base_test',
    port=3306,
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor,
    autocommit=True
)


# connect = pymysql.connect(host='localhost', user='root', password='123456', db='base_test',
#                                port=3306)
# connect = pymysql.connect(**mysql_conf)
# cursor = connect.cursor()

class sqlFunc(object):
    def __init__(self, table: str, **conf):
        self.connect = pymysql.connect(**conf)
        self.table_name = table
        self.cursor = self.connect.cursor()
        # print('done')

    def select_sql(self, target: list, sqlFilter: str = "") -> dict:
        target_test = ", ".join(target)
        sql = "select " + target_test + " from " + self.table_name + " " + sqlFilter
        # print(sql)
        result = ''
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            self.connect.commit()
            # logger.info("select is successful !")
        except Exception as e:
            logger.debug(e)
            logger.info(sql)

        return result

    def update_sql(self, targetFields: list, data: list, sqlFilter: str):
        target = ""
        for item in zip(targetFields, data):
            temp = "{}='{}'".format(item[0], item[1])
            if not target:
                target = temp
            else:
                target = target + ", " + temp
        sql = "update " + self.table_name + " set " + target + " " + sqlFilter
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            logger.info("update is successful !")
        except Exception as e:
            logger.debug(e)
            logger.info(sql)

    def insert_sql(self, targetField: list, data: list, sqlFilter: str = ""):
        targetFieldStr = ", ".join(targetField)
        dataStr = ""
        for item in data:
            temp = "'{}'".format(item)
            dataStr = dataStr + ", " + temp
        # 删除多余的一个 逗号
        dataStr = dataStr.lstrip(", ")
        sql = "insert into " + self.table_name + "(" + targetFieldStr + ") values ( " + dataStr + ") " + sqlFilter + ";"
        # print(sql)
        try:
            self.cursor.execute(sql)
            self.connect.commit()
            logger.info("insert is successful !")
        except Exception as e:
            logger.debug(e)
            logger.info(sql)

    def execute_sql(self, sql: str):
        if "select" in sql:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            # self.connect.commit()
            logger.info("sql is done!")
            return result
        else:
            self.cursor.execute(sql)
            # self.connect.commit()
            logger.info("sql is done!")


# 测试
# db = sqlFunc(table_name, **mysql_conf)
# fileds = ['id', 'journal_name']
# sqlCondition = 'where id >300 limit 20'
# res_select = db.select_sql(fileds, sqlCondition)
# print('res: ', res_select)


# TODO 字符串处理代码
# 字典 ==》 json， 单引号 ==》 双引号

'''
---------------------------------------
 使用simplejson把JSON转化为Python内置类型

JSON到字典转化：
ret_dict = simplejson.loads(json_str)
字典到JSON转化：
json_str = simplejson.dumps(dict)

存入mysql数据库: 报错处理
报错的原因: 引号 紊乱 问题
报错的位置: {'jcrYear': 2018, 'institutionName': "G D\\'ANNUNZIO UNIVERSITY OF CHIETI-PESCARA", 'occurrence': 1},
** 需要考虑 insert 语句 {} 外使用的是 双引号
---------------------------------------
'''


def dict_to_str_sql(result_dict: dict) -> str:
    result_json = json.dumps(result_dict)
    if isinstance(result_json, str):
        result_str = result_json.replace("'", '"').replace("\\", " ")
        result_str = pymysql.escape_string(result_str)
    else:
        # 将 数值 ==> 字符串
        result_str = str(result_json)
    return result_str


'''
---------------------------------------
insert 语句:
* 注意条件语句为空的情况
* 在数据库定义为int 类型的数据， 也可以转化为 str 输入， mysql会自动修改数据类型（猜测）
---------------------------------------
'''
