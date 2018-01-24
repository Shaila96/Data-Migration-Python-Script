import pandas as pd
import csv
import glob
import os

path = '.'
files_in_dir = [f for f in os.listdir(path) if f.endswith('csv')]
#
# for filenames in files_in_dir:
#     df = pd.read_csv(filenames)
#     df.to_csv('out.csv', mode='a')

# df_1 = pd.read_csv('main1.csv')
# df_2 = pd.read_csv('main2.csv')
# df_3 = pd.merge(df_1, df_2, on=['Time', 'Frame#'])
df_3 = pd.DataFrame()
#print(df_3.empty)

list_ = []
for filenames in files_in_dir:
    df = pd.read_csv(filenames)
    df_3 = df_3.join(df)
    #df_3 = pd.merge(df, on=['Time', 'Frame#'])
    #
    # list_.append(df)
    # df_3 = pd.merge(df_3, df, on=['Time', 'Frame#'])
    # df_3.to_csv('out.csv')


#print(list_[0])
print(df_3)