import pandas as pd
import datetime
import re

path = './current.csv'
first_df = pd.read_csv(path)

second_path = './five.csv'
second_df = pd.read_csv(second_path)
df = pd.concat([first_df, second_df], axis=0)
df.dropna(inplace=True)
# print(df)
'''
数据处理:
1, 日期格式: 2012-01-15
2, 删除温度符号
3, climate:转化为数值类型
4, 每次只预测一个地区的数据
5, 风级处理,直接取风级的最大值

6, 天气类型划分:
晴, 多云,阴, 小雨,中雨, 大雨, 雷阵雨, 暴雨,小雪, 中雪, 大雪,暴雪
霾~雾
'''


def delSign(x):
    x = x.replace('℃', '')
    return x


def delTime(x):
    timeText = str(x)
    res = datetime.datetime.strptime(timeText, '%Y年%m月%d日')
    res = datetime.datetime.strftime(res, '%Y%m%d')
    return res


def standardTime(x):
    # timeText = str(x)
    # res = datetime.datetime.strptime(timeText, '%Y年%m月%d日')
    res = datetime.datetime.strftime(x, '%Y-%m-%d')
    return res


def standardWeek(x):
    index = int(x)
    week = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六','星期日',  ]
    res = week[index]
    return res


def findWind(x):
    wind = str(x)
    res = re.findall(r'\d{1,}', wind)
    if not res:
        return 0
    res = [int(item) for item in res]
    max_wind = max(res)
    return max_wind


def simpleClimate(x):
    # 晴, 多云,阴, 小雨,中雨, 大雨, 雷阵雨, 暴雨,小雪, 中雪, 大雪,暴雪
    climate_type = ['暴雪', '大雪', '中雪', '小雪', '暴雨', '雷阵雨', '大雨', '中雨', '小雨', '阴', '多云', '晴']
    for index, item in enumerate(climate_type):
        if item in x:
            return index
    return 11


def cleanFunc(isSaved=False):
    df['max_temp'] = df.apply(lambda x: delSign(x['max_temp']), axis=1)
    df['min_temp'] = df.apply(lambda x: delSign(x['min_temp']), axis=1)
    df['date'] = df.apply(lambda x: delTime(x['date']), axis=1)
    df['wind'] = df.apply(lambda x: findWind(x['wind']), axis=1)
    df['climate'] = df.apply(lambda x: simpleClimate(x['climate']), axis=1)
    df.sort_values(by='date', ascending=True, inplace=True)
    df.set_index('date', inplace=True)
    df.reset_index(inplace=True)
    print(df.head())
    if isSaved:
        df.to_csv('./cleanData.csv', index=None)
    return df


# cleanFunc(isSaved=True)


def showData(df):
    # df['max_temp'] = df.apply(lambda x: delSign(x['max_temp']), axis=1)
    # df['min_temp'] = df.apply(lambda x: delSign(x['min_temp']), axis=1)
    df['date'] = df.apply(lambda x: delTime(x['date']), axis=1)


    # 添加星期几信息: 从0开始计数，0代表礼拜一，6是礼拜天。
    # 把时间列标准化时间格式
    df['date'] = pd.to_datetime(df['date'])
    df['week'] = df['date'].dt.dayofweek
    df['week'] = df.apply(lambda x: standardWeek(x['week']), axis=1)

    df['date'] = df.apply(lambda x: standardTime(x['date']), axis=1)
    df.sort_values(by='date', ascending=True, inplace=True)
    df.set_index('date', inplace=True)
    df.reset_index(inplace=True)
    print(df.head())
    new_df = df[df['date'] > '2018-12-31']
    new_df.to_csv('./showData2.csv', index=None)
    print(new_df)
    return df


showData(df)
