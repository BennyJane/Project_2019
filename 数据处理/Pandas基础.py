#构造储存的表
Left_df=pd.DataFrame(columns=['exchange_time','bid/ask_price'])
Right_df=pd.DataFrame(columns=['exchange_time','bid/ask_price'])

#利用k值的奇偶性，来记录数值变化趋势
#上一个k为奇数代表降，下一个找升；上一个k偶数代表上升，下一个要找降
k=1
first_break_point=0
#series 类型
end_num=Mean_df.shape[0]
for i in range(1, end_num):
    Current_Process=Mean_df.iloc[:i]
    #Current_Process=Mean_df[:i]
    first_max_price=Current_Process.max()
    first_min_price=Current_Process.min()
    last_price=Current_Process.iloc[i]
    result=compute(first_max_price,first_min_price)
    if result < 0.001:
        continue
    else:
         first_break_point=i
    #>=0.001
    #找到第一组最值
    #判断升降
        if last_price ==first_max_pirce:
            k=k+1
            #找出最小值所在的行，注意保存的先后顺序
            min_id=Mean_df.idxmin()
            max_id=Mean_df.idxmax()
            #选出时间和价格，分别保存到起、终点的dataframe中，最后再考虑合并
            Left_df.loc[Left_df.shape[0]] = df.iloc[min_id, 1:]#只取出时间和价格
            Right_df.loc[Right_df.shape[0]] = df.iloc[max_id, 1:]#只取出时间和价格\
            
            #先完成一段数据的查找
            break
            
        else:
            #找出最小值所在的行，注意保存的顺序
            max_id=Mean_df.idxmax()
            min_id=Mean_df.idxmin()
            #选出时间和价格，分别保存到起、终点的dataframe中，最后再考虑合并
            Left_df.loc[Left_df.shape[0]] = df.iloc[max_id, 1:]#只取出时间和价格
            Right_df.loc[Right_df.shape[0]] = df.iloc[min_id, 1:]#只取出时间和价格
            
            #先完成一段数据的查找
            break
#从第一段数据结尾，继续第二段数据，起始位向后+1
n=first_break_point+1
for j in range(n,end_num):
    j = j+1
    #先判断第一段是升 or 降
    if (k % 2)==0:
        #上一个K为偶数，下一个找下降
        #保证可以取到2个数以上
        N_Process=Mean_df.iloc[n:j]
        #？？需要检测N_Process的索引号，如果从0开始了，下方的Max_id就需要加上 （breakpoint + 1）
        #可以通过判断last_price 与 找出来的最值的索引号是否相等来判断
        N_max_price=N_Process.max()
        N_min_price=N_Process.min()
        last_price=N_Process.iloc[j]
        result=compute(first_max_price,first_min_price)
        if result < 0.001:
            continue
        else:
            #最后一个极值必须是最小值
            if last_price ==N_max_pirce:
                pass
            else:
                k=k+1
                n = j + 1
                #找出最大值所在的行，注意保存的顺序
                max_id=N_Process.idxmax()
                min_id=N_Process.idxmin()
                #选出时间和价格，分别保存到起、终点的dataframe中，最后再考虑合并到一张表中
                Left_df.loc[Left_df.shape[0]] = df.iloc[max_id, 1:]#只取出时间和价格
                Right_df.loc[Right_df.shape[0]] = df.iloc[min_id, 1:]#只取出时间和价格
                #完成一段数据的查找
                print('完成了一对极值的查找：%s' %k)
                #continue
    else:
        #上一个K为奇数，下一个要找升
        #保证可以取到2个数以上
        N_Process=Mean_df.iloc[n:j]
        #？？需要检测N_Process的索引号，如果从0开始了，下方的Max_id就需要加上 （breakpoint + 1）
        N_max_price=N_Process.max()
        N_min_price=N_Process.min()
        last_price=N_Process.iloc[j]
        result=compute(first_max_price,first_min_price)
        if result < 0.001:
            continue
        else:
            #最后一个极值必须是最大值
            if last_price ==N_max_pirce:
                k=k+1
                n = j + 1
                #找出最小值所在的行，注意保存的顺序
                max_id=N_Process.idxmax()
                min_id=N_Process.idxmin()
                #选出时间和价格，分别保存到起、终点的dataframe中，最后再考虑合并到一张表中
                Left_df.loc[Left_df.shape[0]] = df.iloc[min_id, 1:]#只取出时间和价格
                Right_df.loc[Right_df.shape[0]] = df.iloc[max_id, 1:]#只取出时间和价格
                #先完成一段数据的查找
                continue
            else:
                continue

#将两张表合并
Newdf=pd.concat([Left_df,Right_df],axis=1)
#print(Newdf)

#重新命名表的列名称
Newdf.rename(columns={'exchange_time':'extreme point', 'bid/ask_price':'Start_price', 'exchange_time':'confirm point','bid/ask_price':'End_price'}, inplace = True)
Newdf.to_csv("E:/编程接单/2019-4-14/Second_data.csv")

#end
