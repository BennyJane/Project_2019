#series 类型
end_num=Mean_df.shape[0]

#利用k值的奇偶性，来记录数值变化趋势
#上一个k为奇数代表降，下一个找升；上一个k偶数代表上升，下一个要找降
k=1

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
    #>=0.001
    #找到第一组最值
    #判断升降
        if last_price ==first_max_pirce:
            k=k+1
            #找出最小值所在的行，注意保存的顺序
            min_id=Mean_df.idxmin()
            max_id=Mean_df.idxmax()
            #选出时间和价格，分别保存到起、终点的dataframe中，最后再考虑合并
            ??
            
        else:
            #找出最小值所在的行，注意保存的顺序
            max_id=Mean_df.idxmax()
            min_id=Mean_df.idxmin()
            #选出时间和价格，分别保存到起、终点的dataframe中，最后再考虑合并
            
            pass
    #找出

    #找出对应行的数据
        break
    
