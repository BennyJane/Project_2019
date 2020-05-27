import datetime
import json

climate_type = ['暴雪', '大雪', '中雪', '小雪', '暴雨', '雷阵雨', '大雨', '中雨', '小雨', '阴', '多云', '晴']
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


def simpleClimate(x):
    # 晴, 多云,阴, 小雨,中雨, 大雨, 雷阵雨, 暴雨,小雪, 中雪, 大雪,暴雪
    climate_type = ['暴雪', '大雪', '中雪', '小雪', '暴雨', '雷阵雨', '大雨', '中雨', '小雨', '阴', '多云', '晴']
    for index, item in enumerate(climate_type):
        if item in x:
            return index
    return 11


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)


# dic = {'name': 'jack', 'create_time': datetime.datetime(2019, 3, 19, 10, 6, 6)}
#
# print(json.dumps(dic, cls=DateEncoder))

def predictWeather(site, date, max_temp, min_temp):
    import pickle

    path = f'./data/{site}.pkl'
    with open(path, "rb") as f:
        model = pickle.load(f)
    train_data = [[date, max_temp, min_temp]]
    res = model.predict(train_data)
    return res


def findLatestDay(df, site):
    only_site_df = df[df['site'] == site]
    only_site_df.set_index('date', inplace=True)
    only_site_df.reset_index(inplace=True)
    # print(only_site_df.tail)
    row_limit = only_site_df.shape[0] - 2
    print(row_limit)
    date = only_site_df.loc[row_limit, 'date']
    date_num = float(date.replace('-', ''))
    max_temp = only_site_df.loc[row_limit, 'max_temp']
    max_temp = max_temp.replace('℃', '')
    min_temp = only_site_df.loc[row_limit, 'min_temp']
    min_temp= min_temp.replace('℃', '')

    climate = only_site_df.loc[row_limit, 'climate']
    return date,date_num,  max_temp, min_temp, climate
