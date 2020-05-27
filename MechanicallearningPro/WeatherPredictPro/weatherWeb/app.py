import json
import pandas as pd
import warnings
from flask import Flask, jsonify, render_template, request
import math

from data.dealData import monthList, siteDict, getPicData, strToInt, DateEncoder, predictWeather, findLatestDay, \
    climate_type

warnings.filterwarnings('ignore')

app = Flask(__name__)

originData = './data/final.csv'
df = pd.read_csv(originData)

latest_month_path = './data/showData.csv'
latest_df = pd.read_csv(latest_month_path)


@app.route('/', methods=['GET', 'POST'])
def index():
    currentMonth = '2020-01'
    targetSite = request.args.get('site')
    targetMonth = request.args.get('month')
    print(targetSite, targetMonth)
    if not targetSite:
        targetSite = '济南'

    latest_day_date, date_num, max_temp, min_temp, latest_day_climate = findLatestDay(latest_df, targetSite)
    next_day_climate = predictWeather(targetSite, date_num, max_temp, min_temp)
    latest_day_info = {
        'date': latest_day_date,
        'max_temp': max_temp,
        'min_temp': min_temp,
        'climate': latest_day_climate
    }
    climate_index = int(math.ceil(next_day_climate[0]))
    if climate_index >= 12:
        climate_index = 11
    next_climate = climate_type[climate_index]

    print('预测天气状况', latest_day_climate, next_climate)

    if targetSite and not targetMonth:
        currentSite = targetSite
        resDf = df[(df['site'] == currentSite) & (df['date'] == currentMonth)]
        # print(resDf)
        monthJson = resDf.to_dict(orient='records')
        for month in monthJson:
            if month.get('date') == currentMonth:
                targetMonth = month.get('month_data')
                break
        # print(targetMonth)
        # 获取月平均数据
        month_mean_max_temp = resDf['month_mean_max_temp'].unique().tolist()[0]
        month_mean_min_temp = resDf['month_mean_min_temp'].unique().tolist()[0]

        # 获取每天的气温数据
        targetMonth = json.loads(targetMonth)
        picData = getPicData(targetMonth)
        picDataText = json.dumps(picData, ensure_ascii=False)
        site = siteDict.keys()
        return render_template('index.html', currentSite=currentSite, currentMonth=currentMonth, monthList=monthList,
                               site=site, targetMonth=targetMonth, picDataText=picDataText,
                               next_climate=next_climate, latest_day_info=latest_day_info,
                               month_mean_max_temp=month_mean_max_temp,
                               month_mean_min_temp=month_mean_min_temp)
    elif targetSite and targetMonth and targetMonth != '2020-05':
        currentSite = targetSite
        currentMonth = targetMonth
        # print(currentSite, currentMonth)
        resDf = df[(df['site'] == currentSite) & (df['date'] == currentMonth)]
        monthJson = resDf.to_dict(orient='records')
        for month in monthJson:
            if month.get('date') == currentMonth:
                targetMonth = month.get('month_data')
                break
        # print(targetMonth)
        # 获取月平均数据
        month_mean_max_temp = resDf['month_mean_max_temp'].unique().tolist()[0]
        month_mean_min_temp = resDf['month_mean_min_temp'].unique().tolist()[0]

        # 获取每天的气温数据
        targetMonth = json.loads(targetMonth)
        picData = getPicData(targetMonth)
        picDataText = json.dumps(picData, ensure_ascii=False)
        site = siteDict.keys()
        return render_template('index.html', currentSite=currentSite, currentMonth=currentMonth, monthList=monthList,
                               site=site, targetMonth=targetMonth, picDataText=picDataText,
                               next_climate=next_climate, latest_day_info=latest_day_info,
                               month_mean_max_temp=month_mean_max_temp,
                               month_mean_min_temp=month_mean_min_temp)

    else:
        currentSite = targetSite
        currentMonth = targetMonth
        current_month_df = latest_df.loc[
            (latest_df['date'].str.contains(currentMonth)) & (latest_df['site'] == currentSite)]
        # 添加星期几信息
        # 把时间列标准化时间格式
        current_month_df['date'] = pd.to_datetime(current_month_df['date'])
        # print(current_month_df)
        monthJson = current_month_df.to_dict(orient='records')
        # print(current_month_df.info)
        targetMonth = monthJson
        picData = getPicData(monthJson)
        picDataText = json.dumps(picData, ensure_ascii=False, cls=DateEncoder)
        # print('5 month', monthJson, type(monthJson))
        # 求每月最高气温
        # 先将字符串转化为数值
        current_month_df['max_temp'] = current_month_df.apply(lambda x: strToInt(x['max_temp']), axis=1)
        current_month_df['min_temp'] = current_month_df.apply(lambda x: strToInt(x['min_temp']), axis=1)

        month_mean_max_temp = '{}℃'.format(current_month_df['max_temp'].mean())
        month_mean_min_temp = '{}℃'.format(current_month_df['min_temp'].mean())

        site = siteDict.keys()
        return render_template('index.html', currentSite=currentSite, currentMonth=currentMonth, monthList=monthList,
                               site=site, targetMonth=targetMonth, picDataText=picDataText,
                               next_climate=next_climate, latest_day_info=latest_day_info,
                               month_mean_max_temp=month_mean_max_temp,
                               month_mean_min_temp=month_mean_min_temp)


if __name__ == '__main__':
    app.run(debug=1, port=5001)
