monthList = ['202001', '202002', '202003', '202004', '202005']
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
