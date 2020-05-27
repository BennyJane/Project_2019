monthList = ['2020-01', '2020-02', '2020-03', '2020-04', '2020-05']
siteDict = {
    '济南': 'jinan',
    '青岛': 'qingdao',
    '淄博': 'zibo',
    '枣庄': 'zaozhuang',
    '东营': 'dongying',
    '烟台': 'yantai',
    '潍坊': 'weifang',
    '济宁': 'jining1',
    '泰安': 'taian1',
    '威海': 'weihai',
    '日照': 'rizhao',
    '滨州': 'binzhou',
    '德州': 'dezhou',
    '聊城': 'liaocheng',
    '菏泽': 'heze',
    '莱芜': 'laiwu',
    '临沂': 'linyi2'
}


def strToInt(wenDu):
    res = wenDu.replace('℃', '')
    res = int(res)
    return res


def getPicData(data: list):
    res = []
    for day in data:
        temp = {
            'name': day.get('date'),
            'value1': strToInt(day.get('max_temp')),
            'value2': strToInt(day.get('min_temp'))
        }
        res.append(temp)
    return res


import datetime
import json


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)


# dic = {'name': 'jack', 'create_time': datetime.datetime(2019, 3, 19, 10, 6, 6)}
#
# print(json.dumps(dic, cls=DateEncoder))