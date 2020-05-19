import pandas as pd
from sklearn.cluster import KMeans  # 导入K均值聚类算法
import matplotlib.pyplot as plt

from core.dealData import deal


def SEEMethod(df):
    '利用SSE选择k'
    SSE = []  # 存放每次结果的误差平方和
    for k in range(1, 9):
        estimator = KMeans(n_clusters=k, max_iter=500, n_jobs='deprecated')  # 构造聚类器
        estimator.fit(df)
        SSE.append(estimator.inertia_)
    X = range(1, 9)
    plt.figure(figsize=(6, 3))
    plt.xlabel('k')
    plt.ylabel('SSE')
    plt.plot(X, SSE, 'o-')
    plt.savefig('../images/see_st.png')
    plt.show()


def kmeansCore(k, iteration, df):
    outputfile = '../data/final.csv'
    # 调用k-means算法，进行聚类分析
    kmodel = KMeans(n_clusters=k, n_jobs=4)  # n_jobs是并行数，一般等于CPU数较好
    kmodel.fit(df)  # 训练模型

    r1 = pd.Series(kmodel.labels_).value_counts()  # 统计各个类别的数目
    r2 = pd.DataFrame(kmodel.cluster_centers_)  # 找出聚类中心
    r = pd.concat([r2, r1], axis=1)  # 横向连接（0是纵向），得到聚类中心对应的类别下的数目
    r.columns = list(df.columns) + [u'类别数目']  # 重命名表头

    r = pd.concat([df, pd.Series(kmodel.labels_, index=df.index)], axis=1)  # 详细输出每个样本对应的类别
    r.columns = list(df.columns) + [u'聚类类别']  # 重命名表头
    r.to_csv(outputfile)  # 保存分类结果


df = deal()
SEEMethod(df)

# k = 3  # 需要进行的聚类类别数
# iteration = 500  # 聚类最大循环数
# kmeansCore(k, iteration, df)
