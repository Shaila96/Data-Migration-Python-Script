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

# REMOVE UNNECESSARY COLUMNS WHILE CLEANING FOR PP and KP

file_type_static = ['perinasal', 'key_stroke', 'key_pressure', 'mouse_pressure', 'mouse_trajectory']

perinasal_column_list = ['Frame#', 'Time', 'Perspiration']
key_stroke_new_column_list = ['Time', 'Key', 'Serial']
key_pressure_column_list = ['#PressureID', 'Time', 'Sensor1', 'Sensor2', 'Sensor3', 'Sensor4']
mouse_pressure_column_list = ['Time', 'Sensor1', 'Sensor2', 'Sensor3', 'Sensor4']
mouse_trajectory_column_list = ['Time', 'X', 'Y', 'Type']

new_file_extension = "_cleaned.csv"


def getCleanFileName(file_name):
    return get_file_name_without_extension(file_name) + new_file_extension


def cleanDataAndGetNewFile(file_path, file_name):
    df = pd.read_csv(file_path, error_bad_lines=False, index_col=False)

    if fnmatch(file_name, '*_pp.csv'):
        mergeRowsForOneSec(file_type_static[0], file_path, df)
    if fnmatch(file_name, '*_ks.csv'):
        addRowsAndSerialKeyStrokes(file_type_static[1], file_path, df)
    if fnmatch(file_name, '*_kp.csv'):
        mergeRowsForOneSec(file_type_static[2], file_path, df)
    if fnmatch(file_name, '*_mp.csv'):
        mergeRowsForOneSec(file_type_static[3], file_path, df)
    if fnmatch(file_name, '*_mt.csv'):
        addRowsMouseTrajectory(file_type_static[4], file_path, df)


def addRowsAndSerialKeyStrokes(file_type, file_path, df, ind=0):
    # Assigning very first row time from the starting of the ind
    current_time = int(df.loc[0 + ind].Time)
    new_key_stroke_df = pd.DataFrame(columns=getColumnList(file_type))
    back_key_stroke_list = []
    serial = 1

    for row_index, row in df.iloc[ind:].iterrows():
        temp_time = int(row['Time'])
        # print("Index:" + str(row_index))
        # print("Temp Time:" + str(temp_time))
        # print("Current Time:" + str(current_time))

        time_diff = temp_time - current_time

        if time_diff == 0:
            new_key_stroke_df, back_key_stroke_list, serial = appendNewRowExceptBackKeyRow(back_key_stroke_list,
                                                                                           new_key_stroke_df,
                                                                                           row,
                                                                                           serial)
        else:
            # NOW ADD THE BACK KEY ROW HERE WITH INCREASING THE SERIAL
            for back_key_stroke in back_key_stroke_list:
                new_key_stroke_df, serial = addKeyStrokeRowWithSerial(new_key_stroke_df, back_key_stroke, serial)

            # RE-INITIALIZE The back_key_stroke_list FOR THE NEXT SECOND
            back_key_stroke_list = []

            if (time_diff) == 1:
                current_time = temp_time
                serial = 1
                new_key_stroke_df, back_key_stroke_list, serial = appendNewRowExceptBackKeyRow(back_key_stroke_list,
                                                                                               new_key_stroke_df,
                                                                                               row,
                                                                                               serial)
            elif ((time_diff) > 1):
                for time_in in range(1, time_diff):
                    current_time = current_time + 1
                    new_row = {"Time": current_time, "Key": 'NA', "Serial": 0}
                    row_df = pd.DataFrame(new_row, index=[0])
                    new_key_stroke_df = pd.concat([new_key_stroke_df, row_df])

                # ADD THE ROW AFTER ADDING DUMMY ROWS IN BETWEEN THE time_diff
                current_time = temp_time
                serial = 1
                new_key_stroke_df, back_key_stroke_list, serial = appendNewRowExceptBackKeyRow(back_key_stroke_list,
                                                                                               new_key_stroke_df,
                                                                                               row,
                                                                                               serial)

    convertToCsv(new_key_stroke_df, file_path, file_type)



def appendNewRowExceptBackKeyRow(back_key_stroke_list, new_key_stroke_df, row, serial):
    if int(row['IsKeyDown']) == 0:
        if row['Key'] != "BACK":
            new_key_stroke_df, serial = addKeyStrokeRowWithSerial(new_key_stroke_df, row, serial)
        else:
            back_key_stroke_list.append(row)
    return new_key_stroke_df, back_key_stroke_list, serial


def addKeyStrokeRowWithSerial(new_key_stroke_df, row, serial):
    row_data = get_key_stroke_new_row_data(row, serial)
    row_df = pd.DataFrame(row_data, index=[0])
    new_key_stroke_df = pd.concat([new_key_stroke_df, row_df])
    serial = serial + 1
    return new_key_stroke_df, serial


def addRowsMouseTrajectory(file_type, file_path, df, ind=0):
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
                d = get_mouse_row_data(row_data, current_time)
                line = pd.DataFrame(d, index=[row_index])
                df = pd.concat([df.ix[:row_index - 1], line, df.ix[row_index:]]).reset_index(drop=True)
                row_index = row_index + 1

            is_index_changed = True

        elif (time_diff) == 1:
            current_time = temp_time

        ##-- If the index is not changed, it means there might be some more dummy row to add --##
        if (is_index_changed):
            addRowsMouseTrajectory(file_type, file_path, df, row_index)
            ##-- This break is IMPORTANT --##
            ##-- If we continue after changing the index, it will be a miscalculation of the index --##
            break

    ##-- If the index is not changed, it means there are no row to add more --##
    if not is_index_changed:
        convertToCsv(df, file_path, file_type)


def get_key_stroke_new_row_data(row, serial):
    return {"Time": row['Time'], "Key": row['Key'], "Serial": serial}


def get_key_stroke_row_data(current_time):
    return {"#KeystrokeID": 0, "Time": current_time, "IsKeyDown": 0, "Key": 'NA'}


def get_mouse_row_data(prior_row, current_time):
    # print("Time: " + str(prior_row.Time))
    return {"Time": current_time, "X": prior_row.X, "Y": prior_row.Y, "Type": prior_row.Type}


def convertToCsv(df, file_path, file_type):
    file_dest = get_file_path_without_extension(file_path) + new_file_extension
    df = df[getColumnList(file_type)]
    df.to_csv(file_dest, index=False)


def getColumnList(file_type):
    column_list = None
    if file_type == file_type_static[0]:
        column_list = perinasal_column_list
    elif file_type == file_type_static[1]:
        column_list = key_stroke_new_column_list
    elif file_type == file_type_static[2]:
        column_list = key_pressure_column_list
    elif file_type == file_type_static[3]:
        column_list = mouse_pressure_column_list
    elif file_type == file_type_static[4]:
        column_list = mouse_trajectory_column_list

    return column_list


def mergeRowsForOneSec(file_type, file_path, df):
    max_time = int(math.ceil(df['Time'].max()))
    min_time = int(math.floor(df['Time'].min()))
    downsampled_df = pd.DataFrame(columns=getColumnList(file_type))

    for i in range(min_time, max_time):
        # for i in range(min_time, min_time+3):
        row_data = get_one_sec_row(file_type, df, i)
        row_df = pd.DataFrame(row_data, index=[i])
        downsampled_df = pd.concat([downsampled_df, row_df])

    convertToCsv(downsampled_df, file_path, file_type)


def get_one_sec_row(file_type, df, i):
    one_sec_df = df[(i <= df['Time']) & (df['Time'] < i + 1)]
    one_sec_df_mean = one_sec_df.mean()

    if file_type == file_type_static[0]:
        return {
            "Frame#": i,
            "Time": i,
            "Perspiration": get_perspiration_value(one_sec_df_mean)
        }
    elif file_type == file_type_static[2]:
        return {
            "#PressureID": i,
            "Time": i,
            "Sensor1": convertToInt(one_sec_df_mean['Sensor1']),
            "Sensor2": convertToInt(one_sec_df_mean['Sensor2']),
            "Sensor3": convertToInt(one_sec_df_mean['Sensor3']),
            "Sensor4": convertToInt(one_sec_df_mean['Sensor4'])
        }
    elif file_type == file_type_static[3]:
        return {
            "Time": i,
            "Sensor1": convertToInt(one_sec_df_mean['Sensor1']),
            "Sensor2": convertToInt(one_sec_df_mean['Sensor2']),
            "Sensor3": convertToInt(one_sec_df_mean['Sensor3']),
            "Sensor4": convertToInt(one_sec_df_mean['Sensor4'])
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
        new_file = getCleanFileName(file_name)
        print(new_file)
        cleanDataAndGetNewFile(file_path, file_name)


####STARTING OF THE SCRIPT####
creatDirAndRunScript()
