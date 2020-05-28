import warnings

import pandas as pd
import numpy as np
import pickle
import time
warnings.filterwarnings('ignore')

# 是否保存处理好的数据
from cleanData import cleanFunc

isSaved = True
if isSaved:
    path = './cleanData.csv'
    df = pd.read_csv(path)
else:
    df = cleanFunc(isSaved)
print(df.head())

'''
只用最近一年的数据: 用前一天的气温，来预测明天的天气状况
'''


def tarinModel(df, site):
    df = df[(df['date'] > 20181231) & (df['site'] == site)]
    df.set_index('date', inplace=True)
    df.reset_index(inplace=True)
    next_climate_list = df['climate'].tolist()
    try:
        for index in range(df.shape[0] - 1):
            df.loc[index, 'climate'] = next_climate_list[index+1]
    except Exception as e:
        pass

    print(df.shape[0])
    # 删除wind列，干扰特征
    new_df = df[['date','climate','max_temp','min_temp','site']]
    # print(new_df.head())

    # labels 准确值
    labels = np.array(new_df['climate'])
    # 去掉特征中的标签
    feature_df = new_df.drop('climate', axis=1)
    feature_df = feature_df.drop('site', axis=1)
    # 转化成合适的格式
    features = np.array(feature_df)

    # 数据集划分
    from sklearn.model_selection import train_test_split

    x_tarin, x_test, y_tarin, y_test = train_test_split(
        features, labels, test_size=0.3, random_state=1120
    )
    print('训练集特征:', x_tarin.shape)
    print('训练集标签:', y_tarin.shape)
    print('测试集特征:', x_test.shape)
    print('测试集标签:', y_test.shape)

    # 导入算法
    from sklearn.ensemble import RandomForestRegressor

    rf = RandomForestRegressor(n_estimators=1000, random_state=1120)
    rf.fit(x_tarin, y_tarin)

    #  预测结果
    predictions = rf.predict(x_test)
    # print(type(x_test))
    # 计算误差
    errors = abs(predictions - y_test)
    # print(errors)
    # mean absolute percentage error (MAPE)
    mape = 100 * (errors / y_test)
    print(np.mean(mape))

    saved_model_name = f'{site}.pkl'
    with open(saved_model_name, "wb") as f:
        pickle.dump(rf, f)

siteDict = {
    # '济南': 'jinan',
    # '青岛': 'qingdao',
    # '淄博': 'zibo',
    # '枣庄': 'zaozhuang',
    # '东营': 'dongying',
    # '烟台': 'yantai',
    # '潍坊': 'weifang',
    # '济宁': 'jining1',
    # '泰安': 'taian1',
    # '威海': 'weihai',
    # '日照': 'rizhao',
    # '滨州': 'binzhou',

    '德州': 'dezhou',
    '聊城': 'liaocheng',
    '菏泽': 'heze',
    '莱芜': 'laiwu',
    '临沂': 'linyi2'
}

# tarinModel(df, '德州')

for key in siteDict.keys():
    try:
        tarinModel(df, key)
        # time.sleep(60*2)
    except Exception as e:
        print(f'===================================== {e}')