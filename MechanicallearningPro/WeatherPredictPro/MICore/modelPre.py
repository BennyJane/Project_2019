import pickle

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

target = [[20190103, 5, -3]]
res = model.predict(target)

res = int(round(res[0]))
print(res)
climate_type = ['暴雪', '大雪', '中雪', '小雪', '暴雨', '雷阵雨', '大雨', '中雨', '小雨', '阴', '多云', '晴']
print(climate_type[res])