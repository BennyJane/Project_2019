import pandas as pd
import random
import numpy as np

soh = []
for i in range(10):
    b = np.random.rand()
    print('%.6f' % b)
    soh.append('%.6f' % b)
print(soh)
month = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
temp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
charged = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
df = pd.DataFrame(data={
'SOH':soh, 'month': month, 'Temp':temp, 'Charged':charged
})


print(df)
df.to_csv('./soh.csv', index=None, encoding='utf-8')