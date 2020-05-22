import os
import pandas as pd
from sklearn.cluster import KMeans  # 导入K均值聚类算法
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


#打印本地中的所有字体
# for font in fm.fontManager.ttflist:
#     print(font.name)
# 预先设置图表使用的字体，防止中文乱码问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
# zhfont = fm.FontProperties(fname='C:\Windows\Fonts\楷体 常规.ttf')
def SEEMethod(df, start=1, limit=9):
    '利用SSE选择k'
    SSE = []  # 存放每次结果的误差平方和
    for k in range(start, limit):
        estimator = KMeans(n_clusters=k, max_iter=500, n_jobs='deprecated')  # 构造聚类器
        estimator.fit(df)
        SSE.append(estimator.inertia_)
    X = range(start, limit)
    fig = plt.figure(figsize=(6, 3))
    fig.tight_layout()
    plt.xlabel('k', size=8)
    # plt.ylabel('SSE', size=8)
    plt.plot(X, SSE, 'o-')
    if os.access('./static/images/see.png', os.F_OK):
        os.remove('./static/images/see.png')
    plt.savefig('./static/images/see.png', dpi=200, bbox_inches='tight')
    # plt.show()


def kmeansCore(k, iteration, df):
    outputfile = './data/final.csv'
    # 调用k-means算法，进行聚类分析
    kmodel = KMeans(n_clusters=k, max_iter=iteration, n_jobs='deprecated')  # n_jobs是并行数，一般等于CPU数较好
    kmodel.fit(df)  # 训练模型

    r1 = pd.Series(kmodel.labels_).value_counts()  # 统计各个类别的数目
    r2 = pd.DataFrame(kmodel.cluster_centers_)  # 找出聚类中心
    r = pd.concat([r2, r1], axis=1)  # 横向连接（0是纵向），得到聚类中心对应的类别下的数目
    r.columns = list(df.columns) + [u'category']  # 重命名表头

    r = pd.concat([df, pd.Series(kmodel.labels_, index=df.index)], axis=1)  # 详细输出每个样本对应的类别
    r.columns = list(df.columns) + [u'category']  # 重命名表头
    r.to_csv(outputfile)  # 保存分类结果
    return r


def density_plot(data):  # 自定义作图函数
    plt.figure(figsize=(4, 2))
    p = data.plot(kind='kde', linewidth=2, subplots=True, sharex=False)
    # 特征数量
    featureNum = 8
    [p[i].set_ylabel('') for i in range(featureNum)]
    plt.legend(fontsize=10)
    return plt


def drawCategoryPic(originData, k, resDf):
    pic_output = './static/images/category/'  # 概率密度图文件名前缀
    categoryPicPath = {}
    for i in range(k):
        imagePath = u'%scategory%s.png' % (pic_output, i)
        density_plot(originData[resDf[u'category'] == i]).savefig(imagePath)
        categoryPicPath[i] = '.'+imagePath
    return categoryPicPath
