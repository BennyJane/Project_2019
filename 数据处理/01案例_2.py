from pprint import pprint
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

# 统计该爬虫的消耗时间
print('*' * 50)
t3 = time.time()

#目标将所有带处理文件合并
# 需要将待处理的CSV文件全部放到一个文件夹内
#用自己本地文件路径更换下列
FirstResult_filepath="E:/编程接单/2019-4-14/first_result.csv"
df=pd.read_csv(FirstResult_filepath)
# print(df)


#筛选出'exchange_time','bid_ask_mean'两列
filter_01=df[['exchange_time','bid/ask_price']]
# print(filter_01)
#<class 'pandas.core.series.Series'>
print(filter_01.iloc[0,0:])


filter_02=filter_01.set_index("exchange_time")

#设置横坐标的准确数值;放大图的显示
#9：00-10：15 、10：30-11:30、13：30-15:00
filter_02.plot()
plt.xticks(rotation=45)
plt.show()


Left_of_df=pd.DataFrame(columns=['exchange_time','bid/ask_price'])
Right_of_df=pd.DataFrame(columns=['exchange_time','bid/ask_price'])

Left_of_df.loc[Left_of_df.shape[0]] = filter_01.iloc[0,0:]

# Left_of_df.append(df.iloc[0,1:])
# Left_of_df = pd.concat(Left_of_df,df.iloc[0,1:])
print(Left_of_df)
end_num=filter_01.shape[0]-1
for i in range(0,end_num):
    price01=filter_01.iloc[i,1]
    price02 = filter_01.iloc[i+1,1]
    if price01>=price02:
        continue
    else:
        Right_of_df.loc[Right_of_df.shape[0]] = filter_01.iloc[i, 0:]
        Left_of_df.loc[Left_of_df.shape[0]] = filter_01.iloc[i+1, 0:]
        for j in range(i+1,end_num):
            price01 = filter_01.iloc[j, 1]
            price02 = filter_01.iloc[j + 1, 1]
            if price01 <= price02:
                continue
            else:
                Right_of_df.loc[Right_of_df.shape[0]] = filter_01.iloc[j, 0:]
                Left_of_df.loc[Left_of_df.shape[0]] = filter_01.iloc[j + 1, 0:]
                i=j+1
                break

# print(Left_of_df)
# print(Right_of_df)

Newdf=pd.concat([Left_of_df,Right_of_df],axis=1)
print(Newdf)

Newdf.rename(columns={'exchange_time':'extreme point', 'bid/ask_price':'Start_price', 'exchange_time':'confirm point','bid/ask_price':'End_price'}, inplace = True)
# order = ['Start_time','Start_time','End_time','End_point']
# Newdf_order = Newdf[order]
Newdf.to_csv("E:/编程接单/2019-4-14/Second_result02.csv")


mean_data=filter_01['bid/ask_price']
# mean_data02=filter_01.iloc[0:,1]
# print(mean_data02)
# print(mean_data)



t4 = time.time()
print('总共耗时：%s' % (t4 - t3))

