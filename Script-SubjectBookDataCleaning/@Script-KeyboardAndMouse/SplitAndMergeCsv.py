import pandas as pd
import os
from os import listdir
from fnmatch import fnmatch


data_dir = "Data"
input_dir = "InputOutput"
input_data_path = os.path.join(data_dir, input_dir)

file_type_static = ['key_strokes', 'mouse']

def cleanData(file_path, file_name):
    df = pd.read_csv(file_path)
    if fnmatch(file_name, '*_ks*'):
        print("Inside Keystroke Cleaing....")
        addRows(file_type_static[0], file_path, df)
    if fnmatch(file_name, '*_mt*'):
        print("Inside Mouse Trajectory Cleaing....")
        addRows(file_type_static[1], file_path, df)

def addRows(file_type, file_path, df, ind=0):
    # Assigning very first row time from the starting of the ind
    current_time = int(df.loc[0 + ind].Time)
    is_index_changed = False

    for row_index, row in df.iloc[ind:].iterrows():
        temp_time = int(row['Time'])
        print("Index:" + str(row_index))
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
        if file_type == file_type_static[0]:
            covertToKeystrokesCsv(df, file_path)
        elif file_type == file_type_static[1]:
            covertToMouseCsv(df, file_path)


def get_key_stroke_row_data(current_time):
    return {"#KeystrokeID": 0, "Time": current_time, "IsKeyDown": 0, "Key": 'NA'}


def get_mouse_row_data(prior_row, current_time):
    # print(row)
    print("Time: " + str(prior_row.Time))
    return {"Time": current_time, "X": prior_row.X, "Y": prior_row.Y, "Type": prior_row.Type}


def covertToKeystrokesCsv(df, file_dest):
    df = df[['#KeystrokeID', 'Time', 'IsKeyDown', 'Key']]
    df.to_csv(file_dest, index=False)


def covertToMouseCsv(df, file_dest):
    df = df[['Time', 'X', 'Y', 'Type']]
    df.to_csv(file_dest, index=False)


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

















# def cleanData(file_path, file_name):
#     if fnmatch(file_name, '*ks*'):
#         addDummyRows(file_type_static[0], file_name, file_path)
#     if fnmatch(file_name, '*mt*'):
#         addDummyRows(file_type_static[1], file_name, file_path)
#
#
# def addDummyRows(file_type, file_name, file_path):
#     df = pd.read_csv(file_path)
#     addRowsMouseTrajectory(file_type, file_name, file_path, df)
