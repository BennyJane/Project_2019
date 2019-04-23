#!/user/bin/env Python
#coding=utf-8

import pandas as pd

#求变化率
#下降
def compute01(num1,num2):
    result=(num1-num2)/num1
    return result
#上升
def compute02(num1,num2):
    result=(num1-num2)/num2
    return result

def Get_ExtremeValues(data):
    # 储存起始点
    Left_df = pd.DataFrame()
    Right_df = pd.DataFrame()

    # 储存最值索引号为列表，用于画图
    MAX_MIN_List = []

    # 输入第一段代码处理的数据结果
    k = 1
    first_break_point = 0

    endnum = data.shape[0]

    # 从第二个数据开始读取
    for i in range(1, endnum):
        Current_Process = data.loc[0:i, "means"]  # 带有索引号
        # print(Current_Process)
        # print(Current_Process)
        first_max_price = Current_Process.max()
        max_id = Current_Process.idxmax()
        first_min_price = Current_Process.min()  # 只有最值，没有索引号
        min_id = Current_Process.idxmin()
        last_price = Current_Process.iloc[i]
        # print(first_max_price,first_min_price, "\t",last_price,"\t",)
        if min_id < i:
            # up
            result = compute02(last_price, first_min_price)
            # print(result)
            if result >= The_Limition:
                first_break_point = i
                k = k + 1
                # print(last_price, first_max_price)
                # 找出最值所在行的索引，注意保存的先后顺序
                MAX_MIN_List.append(min_id)
                MAX_MIN_List.append(max_id)
                # print(MAX_MIN_List)
                # 选出整行数据储存，保留索引，输出的时候再考虑删除多余数据，考虑合并
                Left_df = Left_df.append(data.iloc[min_id])
                Right_df = Right_df.append(data.iloc[max_id])
                # 先完成一段数据的查找
                print("该数据以UP趋势开头")
                break

        elif max_id < i:
            # down
            result = compute01(first_max_price, last_price)
            # print(result)
            if result >= The_Limition:
                first_break_point = i
                # print(first_break_point)
                k = k + 1
                # print(last_price, first_min_price)
                # 找出最小值所在的行，注意保存的顺序
                max_id = Current_Process.idxmax()
                min_id = i
                MAX_MIN_List.append(max_id)
                MAX_MIN_List.append(min_id)
                # print(MAX_MIN_List)
                # 选出时间和价格，分别保存到起、终点的dataframe中，最后再考虑合并
                Left_df = Left_df.append(data.iloc[max_id])  # 只取出时间和价格
                Right_df = Right_df.append(data.iloc[min_id])  # 只取出时间和价格
                print("该数据以DOWN趋势开头")
                # 先完成一段数据的查找
                break
        else:
            continue

    n = first_break_point
    j = first_break_point
    while True:
        j = j + 1
        if j < endnum:
            if (k % 2) == 0:
                # 上一个K为偶数，下一个找下降,Down
                # 保证可以取到2个数以上
                N_Process = df.loc[n:j, "means"]
                # print(N_Process)
                N_max_price = N_Process.max()
                max_id = N_Process.idxmax()
                last_price = N_Process.loc[j]
                # 最后一个极值必须是最小值
                if max_id < j:
                    result = compute01(N_max_price, last_price)
                    # print(result)
                    if result >= The_Limition:
                        # print(j)
                        k = k + 1
                        n = j
                        # 找出最大值所在的行，注意保存的顺序
                        max_id = N_Process.idxmax()
                        min_id = j
                        MAX_MIN_List.append(max_id)
                        MAX_MIN_List.append(min_id)
                        # print(MAX_MIN_List)
                        # 选出时间和价格，分别保存到起、终点的dataframe中，最后再考虑合并到一张表中
                        Left_df = Left_df.append(df.iloc[max_id])
                        Right_df = Right_df.append(df.iloc[min_id])
                        # 完成一段数据的查找
                        print('完成了一对极值的查找：%s' % k)

            else:
                # 上一个K为奇数，下一个要找升
                # 保证可以取到2个数以上
                N_Process = df.loc[n:j, "means"]
                # print(N_Process)
                N_min_price = N_Process.min()
                min_id = N_Process.idxmin()
                last_price = N_Process.loc[j]
                if min_id < j:
                    result = compute02(last_price, N_min_price)
                    if result >= The_Limition:
                        k = k + 1
                        n = j
                        # print(last_price, N_min_price, N_max_price)
                        # 找出最小值所在的行，注意保存的顺序
                        max_id = j
                        min_id = N_Process.idxmin()
                        MAX_MIN_List.append(min_id)
                        MAX_MIN_List.append(max_id)
                        # print(MAX_MIN_List)
                        # 选出时间和价格，分别保存到起、终点的dataframe中，最后再考虑合并到一张表中
                        Left_df = Left_df.append(df.iloc[min_id])
                        Right_df = Right_df.append(df.iloc[max_id])
                        # 先完成一段数据的查找
                        print('完成了一对极值的查找：%s' % k)

        else:
            break

    return MAX_MIN_List,Left_df,Right_df

def Get_FinalData(extreme_list,data1,data2):
    Extremes_df = df.iloc[extreme_list, [1, 2]]
    print(Extremes_df)
    # Extremes_df.to_csv(SimpleCoul_filename)

    # 将两张表合并,需要先去掉原来的索引号，这样“1”号的索引与另一个“1”号索引合并。
    data1 = data1.reset_index()
    data1 = data1.iloc[:, [1, 3]]

    data2 = data2.reset_index()
    data2 = data2.iloc[:, [1, 3]]

    Newdf = pd.concat([data1, data2], axis=1)
    return Extremes_df , Newdf


if __name__=="__main__":
    # 变量调整
    # 将第一段代码生成的文件路径拷贝到下方
    FirstResult_filepath = "E:/编程接单/2019-4-14/结项整理/代码重构/First_data_01-04.csv"
    # 变化的比率调整
    The_Limition = 0.001
    # 最值文件保存的位置及文件名，4列，每列两个点
    Final_filename = "E:/编程接单/2019-4-14/结项整理/代码重构/Second_four_data18_01-04.csv"
    SimpleCoul_filename = "E:/编程接单/2019-4-14/结项整理/代码重构/Simple_Col18_01-04.csv"

    df = pd.read_csv(FirstResult_filepath)
    MAX_MIN_List, Left_df, Right_df=Get_ExtremeValues(df)
    Extremes_1cols, Extremes_4cols =Get_FinalData(MAX_MIN_List, Left_df, Right_df)
    print(Extremes_1cols)
