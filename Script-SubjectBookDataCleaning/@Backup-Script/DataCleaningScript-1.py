import pandas as pd
import math
import os
from os import listdir
from fnmatch import fnmatch

data_dir = "Data"
input_dir = "InputOutput"
input_data_path = os.path.join(data_dir, input_dir)
temp_file_dest = None

######################################################################################################
######################################################################################################

file_type_static = ['key_strokes', 'mouse', 'perinasal']
key_pressure_column_list = ["#PressureID", "Time", "Sensor1", "Sensor2", "Sensor3", "Sensor4"]
mouse_pressure_column_list = ["Time", "Sensor1", "Sensor2", "Sensor3", "Sensor4"]
perinasal_column_list = ["Frame#", "Time", "Perspiration"]
new_file_extension = "_cleaned.csv"


def getCleanFileName(file_name):
    return get_file_name_without_extension(file_name) + new_file_extension
    # if fnmatch(file_name, '*_pp.csv*'):
    #     return file_name
    # else:
    #     return get_file_name_without_extension(file_name) + new_file_extension


def cleanDataAndGetNewFile(file_path, file_name):
    df = pd.read_csv(file_path, error_bad_lines=False, index_col=False)

    if fnmatch(file_name, '*_ks.csv'):
        addRows(file_type_static[0], file_path, df)
    if fnmatch(file_name, '*_mt.csv'):
        addRows(file_type_static[1], file_path, df)
    if fnmatch(file_name, '*_kp.csv'):
        mergeRowsForOneSec(file_type_static[0], file_path, df)
    if fnmatch(file_name, '*_mp.csv'):
        mergeRowsForOneSec(file_type_static[1], file_path, df)
    if fnmatch(file_name, '*_pp.csv'):
        mergeRowsForOneSec(file_type_static[2], file_path, df)


def addRows(file_type, file_path, df, ind=0):
    # Assigning very first row time from the starting of the ind
    current_time = int(df.loc[0 + ind].Time)
    is_index_changed = False

    for row_index, row in df.iloc[ind:].iterrows():
        temp_time = int(row['Time'])
        # print("Index:" + str(row_index))
        # print("Temp Time:" + str(temp_time))
        # print("Current Time:" + str(current_time))

        time_diff = temp_time - current_time
        # row_index = index

        if ((time_diff) > 1):
            row_data = df.loc[row_index - 1]
            for time_in in range(1, time_diff):
                current_time = current_time + 1
                d = None
                if file_type == file_type_static[0]:
                    d = get_key_stroke_row_data(current_time)
                elif file_type == file_type_static[1]:
                    ####ADD MOUSE DATA###
                    d = get_mouse_row_data(row_data, current_time)
                line = pd.DataFrame(d, index=[row_index])
                df = pd.concat([df.ix[:row_index - 1], line, df.ix[row_index:]]).reset_index(drop=True)
                row_index = row_index + 1

            is_index_changed = True

        elif (time_diff) == 1:
            current_time = temp_time

        ##-- If the index is not changed, it means there might be some more dummy row to add --##
        if (is_index_changed):
            addRows(file_type, file_path, df, row_index)
            ##-- This break is IMPORTANT --##
            ##-- If we continue after changing the index, it will be a miscalculation of the index --##
            break

    ##-- If the index is not changed, it means there are no row to add more --##
    if not is_index_changed:
        convertToCsv(df, file_path, file_type)


def get_key_stroke_row_data(current_time):
    return {"#KeystrokeID": 0, "Time": current_time, "IsKeyDown": 0, "Key": 'NA'}


def get_mouse_row_data(prior_row, current_time):
    # print("Time: " + str(prior_row.Time))
    return {"Time": current_time, "X": prior_row.X, "Y": prior_row.Y, "Type": prior_row.Type}


def convertToCsv(df, file_path, file_type):
    file_dest = get_file_path_without_extension(file_path) + new_file_extension

    if file_type == file_type_static[0]:
        df = df[['#KeystrokeID', 'Time', 'IsKeyDown', 'Key']]
    elif file_type == file_type_static[1]:
        df = df[['Time', 'X', 'Y', 'Type']]
    df.to_csv(file_dest, index=False)


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
    elif file_type == file_type_static[2]:
        column_list = perinasal_column_list

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
    elif file_type == file_type_static[2]:
        return {
            "Frame#": i,
            "Time": i,
            "Perspiration": get_perspiration_value(one_sec_df_mean)
        }


def get_perspiration_value(one_sec_df_mean):
    if math.isnan(one_sec_df_mean['Perspiration']):
        return 0
    else:
        return one_sec_df_mean['Perspiration']


def convertToInt(number):
    # print(number)
    if math.isnan(number):
        return 0
    else:
        # print(number)
        return int(round(number))


def get_file_path_without_extension(file_path):
    return file_path[:file_path.rfind(".csv")]


def get_file_name_without_extension(file_path):
    return file_path[file_path.rfind("\\") + 1:file_path.rfind(".csv")]


def get_file_name_from_file_path(file_path):
    return file_path[file_path.rfind("\\") + 1:file_path.rfind(".csv") + 1]


def get_file_dir(file_path):
    return file_path[:file_path.rfind("\\") + 1]


######################################################################################################
######################################################################################################



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
        new_file = cleanDataAndGetNewFile(file_path, file_name)
        print(new_file)


####STARTING OF THE SCRIPT####
creatDirAndRunScript()
