import pandas as pd


def deal():
    inputfile = './data/all_grade.xlsx'  # 待聚类的数据文件
    df = pd.read_excel(inputfile)  # 读取数据

    df.to_csv('.finalDat.csv', index=None)
    return df


orderDict = {
    0: "一",
    1: "二",
    2: "三",
    3: "四",
    4: "五",
    5: "六",
    6: "七",
    7: "八",
    8: "九",
    9: "十",
    10: "十一",
    11: "十二",
    12: "十三"
}
