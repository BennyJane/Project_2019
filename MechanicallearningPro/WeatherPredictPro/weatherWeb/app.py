import json

from flask import Flask, jsonify, render_template, request
from data.dealData import monthList, siteDict, getPicData
import pandas as pd

app = Flask(__name__)

originData = './data/final.csv'
df = pd.read_csv(originData)


@app.route('/', methods=['GET', 'POST'])
def index():
    currentMonth = '2020-01'
    targetSite = request.args.get('site')
    targetMonth = request.args.get('month')
    print(targetSite, targetMonth)
    if not targetSite:
        currentSite = '济南'
        resDf = df[(df['site'] == currentSite) & (df['date'] == currentMonth)]
        print(resDf)
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
                               month_mean_max_temp=month_mean_max_temp,
                               month_mean_min_temp=month_mean_min_temp)
    elif targetSite and not targetMonth:
        currentSite = targetSite
        resDf = df[(df['site'] == currentSite) & (df['date'] == currentMonth)]
        print(resDf)
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
                               month_mean_max_temp=month_mean_max_temp,
                               month_mean_min_temp=month_mean_min_temp)
    elif targetSite and targetMonth:
        currentSite = targetSite
        currentMonth = targetMonth[:4] + '-' + targetMonth[4:]
        print(currentSite, currentMonth)
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
                               month_mean_max_temp=month_mean_max_temp,
                               month_mean_min_temp=month_mean_min_temp)


@app.route('/pic/data', methods=['POST', 'GET'])
def picData():
    if request.method == 'POST':
        site = request.form.get('site')
        month = request.form.get('month')

    return ''


if __name__ == '__main__':
    app.run(debug=1)
