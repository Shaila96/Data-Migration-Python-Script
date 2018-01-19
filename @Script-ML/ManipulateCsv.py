import pandas as pd
import os
from os import listdir

data_dir = "DataTrainTest"
normal_window = "\\NormalWindow"
recursive_window = "\\RecursiveWindow"

normal_window_path = data_dir + normal_window
recursive_window_path = data_dir + recursive_window

def find_filenames(path_to_dir, suffix):
    filenames = listdir(path_to_dir)
    return [filename for filename in filenames if filename.endswith(suffix)]

def isNotPathExists(path):
    if not os.path.exists(path):
        print(str(path) + ' is not exists')
        return True
    else:
        print(str(path) + ' is already exists')
        return False

def createDirectoryIfNotExixts(path):
    if isNotPathExists(path):
        os.mkdir(path)

def covertToCsv(df, file_dest):
    df.to_csv(file_dest, header = None, index = False)


csv_file_names = find_filenames(data_dir, ".csv")

for file in csv_file_names:
    print(csv_file_names)
    print(file)
    file_path = data_dir + "\\" + file
    df = pd.read_csv(file_path)

    #####################################
    #####Delete column by row index######
    # df.drop(df.index[0], inplace = True)
    #####################################

    #####################################
    #####Delete column by column index#####
    #df.drop(df.columns[0], axis=1, inplace=True)
    #####################################

    #####################################
    #####Delete column by column name#####

    createDirectoryIfNotExixts(normal_window_path)
    createDirectoryIfNotExixts(recursive_window_path)

    normal_window_dest = normal_window_path + "\\" + file
    recursive_window_dest = recursive_window_path + "\\" + file

    df.drop('subject', axis = 1, inplace = True)
    covertToCsv(df, recursive_window_dest)

    df.drop('previous_stress', axis = 1, inplace = True)
    covertToCsv(df, normal_window_dest)
    #####################################

    #####################################
    #####Deleting the header#####
    # df.columns = range(df.shape[1])
    # df.to_csv('sample.csv', header=None, index=False)
    #####################################

    #normal_window_df.to_csv(normal_window_dest, header=None, index=False)
    #recursive_window_df.to_csv(recursive_window_dest, header=None, index=False)
    #print(df)



#####################################
# col1,col2,col3,col4
# 1,2,3,4
# 5,6,7,8
# 9,10,11,12
# 13,14,15,16
# 17,18,19,20
#####################################
