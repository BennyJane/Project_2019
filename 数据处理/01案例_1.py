import pandas as pd
import os

#目标将所有带处理文件合并
#需要将待处理的CSV文件全部放到一个文件夹内
#用自己本地文件路径更换下列
all_csv_filepath="E:/编程接单/2019-4-14/raw0301"
filename=os.listdir(all_csv_filepath)
print(filename)

#新建一张表，将读取的文件合并到新的表中
alldf=pd.DataFrame()

#合并文件
for file in filename:
    #all_csv_filepath路径后加上‘/’,再跟上文件名称
    filepath='E:/编程接单/2019-4-14/raw0301/%s' %file
    df=pd.read_csv(filepath)
    alldf=pd.concat([alldf,df])

#设置选中的ID，并挑选出包含该id的所有行
Select_instrument_id='rb1905'
Simple_ID=alldf[alldf['instrument_id']==Select_instrument_id]

#求出每行的均值，mean()求出每列的均值，生成了新的表，只包含生成的均值
bid_ask_mean=Simple_ID[['bid_price','ask_price']].mean(1)
# print(bid_ask_mean)

#筛选出'instrument_id','exchange_time'两列
filter_01=Simple_ID[['instrument_id','exchange_time']]

#合并列，axis=1，必须设置；合并后发现均值列，没有列名，默认为数值 0
filter_02=pd.concat([filter_01,bid_ask_mean],axis=1)
# print(filter_02)

#筛选时间段，转换为data格式，[]号
filter_02['exchange_time'] = pd.to_datetime(filter_02['exchange_time'])
print(filter_02)


#小括号（），将时间设置为索引
filter_03 = filter_02.set_index("exchange_time")
# print(filter_02)

#选取9：00-10：15 、10：30-11:30、13：30-15:00段的数据
first_data = filter_03["2019-03-01 09:00:00":"2019-03-01 10:15:00"]
second_data = filter_03["2019-03-01 10:30:00":"2019-03-01 11:30:00"]
third_data = filter_03["2019-03-01 13:30:00":"2019-03-01 15:00:00"]
# print(first_data)
# print(second_data)
# print(third_data)

#合并三个时间段的数据
all_data=pd.concat([first_data,second_data,third_data])

#调整标题序号
all_data=all_data.reset_index()
order = ['instrument_id','exchange_time',0]
all_data_order = all_data[order]
print(all_data_order)

#修改表头，并输出
all_data_order.rename(columns={0:'bid/ask_price'},inplace=True)
all_data_order.to_csv("E:/编程接单/2019-4-14/实验.csv")
