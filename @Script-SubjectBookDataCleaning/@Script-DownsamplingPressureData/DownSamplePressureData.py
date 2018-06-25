import pandas as pd
import os
import math
from fnmatch import fnmatch
from os import listdir

data_dir = "Data"
input_dir = "InputOutput"
input_data_path = os.path.join(data_dir, input_dir)

file_type_static = ['keyboard', 'mouse']
key_pressure_column_list = ["#PressureID", "Time", "Sensor1", "Sensor2", "Sensor3", "Sensor4"]
mouse_pressure_column_list = ["Time", "Sensor1", "Sensor2", "Sensor3", "Sensor4"]
new_file_extension = "_downsampled.csv"


def cleanData(file_path, file_name):
    df = pd.read_csv(file_path, error_bad_lines=False, index_col=False)
    if fnmatch(file_name, '*_kp.csv'):
        mergeRowsForOneSec(file_type_static[0], file_path, df)
    if fnmatch(file_name, '*_mp.csv'):
        mergeRowsForOneSec(file_type_static[1], file_path, df)


def mergeRowsForOneSec(file_type, file_path, df):
    max_time = int(math.ceil(df['Time'].max()))
    min_time = int(math.floor(df['Time'].min()))
    downsampled_df = pd.DataFrame(columns=getColumnList(file_type))

    for i in range(min_time, max_time):
        # for i in range(0, 3):
        row_data = get_one_sec_row(file_type, df, i)
        row_df = pd.DataFrame(row_data, index=[i])
        downsampled_df = pd.concat([downsampled_df, row_df])

    covertToKeyPressureCsv(downsampled_df, file_path, file_type)


def getColumnList(file_type):
    column_list = None
    if file_type == file_type_static[0]:
        column_list = key_pressure_column_list
    elif file_type == file_type_static[1]:
        column_list = mouse_pressure_column_list

    return column_list


def covertToKeyPressureCsv(df, file_path, file_type):
    file_dest = get_file_path_without_extension(file_path) + new_file_extension
    df = df[getColumnList(file_type)]
    df.to_csv(file_dest, index=False)


def get_one_sec_row(file_type, df, i):
    one_sec_df = df[(i <= df['Time']) & (df['Time'] < i + 1)]
    one_sec_df_mean = one_sec_df.mean()

    if file_type == file_type_static[0]:
        return {
            "#PressureID": i,
            "Time": i,
            "Sensor1": convertToInt(one_sec_df_mean['Sensor1']),
            "Sensor2": convertToInt(one_sec_df_mean['Sensor2']),
            "Sensor3": convertToInt(one_sec_df_mean['Sensor3']),
            "Sensor4": convertToInt(one_sec_df_mean['Sensor4'])
        }
    elif file_type == file_type_static[1]:
        return {
            "Time": i,
            "Sensor1": convertToInt(one_sec_df_mean['Sensor1']),
            "Sensor2": convertToInt(one_sec_df_mean['Sensor2']),
            "Sensor3": convertToInt(one_sec_df_mean['Sensor3']),
            "Sensor4": convertToInt(one_sec_df_mean['Sensor4'])
        }


def convertToInt(number):
    print(number)
    return int(round(number))


def get_file_path_without_extension(file_path):
    return file_path[:file_path.rfind(".csv")]


def get_file_name_without_extension(file_path):
    return file_path[file_path.rfind("\\") + 1:file_path.rfind(".csv")]


def get_file_dir(file_path):
    return file_path[:file_path.rfind("\\") + 1]


def find_filenames(path_to_dir, suffix):
    filenames = listdir(path_to_dir)
    return [filename for filename in filenames if filename.endswith(suffix)]


def isNotPathExists(path):
    if not os.path.exists(path):
        print(str(path) + ' is created')
        return True
    else:
        # print(str(path) + ' is already exists')
        return False


def createDirectoryIfNotExixts(path):
    if isNotPathExists(path):
        os.mkdir(path)


def creatDirAndRunScript():
    createDirectoryIfNotExixts(data_dir)
    createDirectoryIfNotExixts(input_data_path)
    csv_file_names = find_filenames(input_data_path, ".csv")

    for file_name in csv_file_names:
        file_path = os.path.join(input_data_path, file_name)
        cleanData(file_path, file_name)


####STARTING OF THE SCRIPT####
creatDirAndRunScript()
