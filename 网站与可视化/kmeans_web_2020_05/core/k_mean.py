import pandas as pd
from sklearn.cluster import KMeans #导入K均值聚类算法
import matplotlib.pyplot as plt

inputfile = './data/exams.csv' #待聚类的数据文件
outputfile = './data/final.csv'
k = 3                       #需要进行的聚类类别数
iteration = 500             #聚类最大循环数

#读取数据并进行聚类分析
data = pd.read_csv(inputfile) #读取数据

data = data.loc[:, ['math score', 'reading score', 'writing score']]

#调用k-means算法，进行聚类分析
kmodel = KMeans(n_clusters = k, n_jobs = 4) #n_jobs是并行数，一般等于CPU数较好
kmodel.fit(data) #训练模型
print(kmodel, type(kmodel))

r1 = pd.Series(kmodel.labels_).value_counts()  #统计各个类别的数目
r2 = pd.DataFrame(kmodel.cluster_centers_)     #找出聚类中心
r = pd.concat([r2, r1], axis = 1) #横向连接（0是纵向），得到聚类中心对应的类别下的数目
r.columns = list(data.columns) + [u'类别数目'] #重命名表头

print(r)

r = pd.concat([data, pd.Series(kmodel.labels_, index = data.index)], axis = 1)  #详细输出每个样本对应的类别
r.columns = list(data.columns) + [u'聚类类别'] #重命名表头
r.to_csv(outputfile) #保存分类结果

def density_plot(data): #自定义作图函数
    p = data.plot(kind='kde', linewidth = 2, subplots = True, sharex = False)
    [p[i].set_ylabel('density') for i in range(k)]
    plt.legend()
    return plt

pic_output = './images' #概率密度图文件名前缀
for i in range(k):
    density_plot(data[r[u'聚类类别']==i]).savefig(u'%s%s.png' %(pic_output, i))