import pandas as pd
import random
import numpy as np

soh = []
for i in range(87):
    b = np.random.rand()
    # print('%.6f' % b)
    soh.append('%.6f' % b)

month = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9,0, 1, 2, 3, 4, 5, 6, 7, 8, 9,0, 1, 2, 3, 4, 5, 6, 7, 8, 9,0, 1, 2, 3, 4, 5, 6, 7, 8, 9,0, 1, 2, 3, 4, 5, 6, 7, 8, 9,0, 1, 2, 3, 4, 5, 6, 7, 8, 9,0, 1, 2, 3, 4, 5, 6, 7, 8, 9,0, 1, 2, 3, 4, 5, 6, 7, 8, 9,9,9,9,9,9,9,9,]
temp = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1,0, 0, 0, 0, 0, 1, 1, 1, 1, 1,0, 0, 0, 0, 0, 1, 1, 1, 1, 1,0, 0, 0, 0, 0, 1, 1, 1, 1, 1,0, 0, 0, 0, 0, 1, 1, 1, 1, 1,0, 0, 0, 0, 0, 1, 1, 1, 1, 1,0, 0, 0, 0, 0, 1, 1, 1, 1, 1,0, 0, 0, 0, 0, 1, 1, 1, 1, 1,0,0,0,0,1,1,1]
charged = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1,0, 0, 0, 0, 0, 1, 1, 1, 1, 1,0, 0, 0, 0, 0, 1, 1, 1, 1, 1,0, 0, 0, 0, 0, 1, 1, 1, 1, 1,0, 0, 0, 0, 0, 1, 1, 1, 1, 1,0, 0, 0, 0, 0, 1, 1, 1, 1, 1,0, 0, 0, 0, 0, 1, 1, 1, 1, 1,0, 0, 0, 0, 0, 1, 1, 1, 1, 1,0,0,0,0,1,1,1]


# print(len(soh), len(month), len(temp), len(charged))
df = pd.DataFrame(data={
'SOH':soh, 'month': month, 'Temp':temp, 'Charged':charged
})


# print(df)
# df.to_csv('./soh.csv', index=None, encoding='utf-8')


import pickle
with open('MLP_SOH_model.pkl', 'rb') as fp:
    df = pickle.load(fp)

print(df)