import pandas as pd
import os
from fnmatch import fnmatch
from os import listdir

data_dir = "Data"
input_dir = "Input"
output_dir = "Output"

input_data_path = os.path.join(data_dir, input_dir)
output_data_path = os.path.join(data_dir, output_dir)


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


def covertToCsv(df, file_dest):
    df = df[['KeystrokeID', 'Time', 'Key']]
    df.to_csv(file_dest, index=False)


def addRows(file_name, df, ind=0):
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

            for time_in in range(1, time_diff):
                current_time = current_time + 1

                d = {"KeystrokeID": 0, "Time": current_time, "Key": 'NA'}
                line = pd.DataFrame(d, index=[row_index])
                df = pd.concat([df.ix[:row_index - 1], line, df.ix[row_index:]]).reset_index(drop=True)
                row_index = row_index + 1

            is_index_changed = True

        elif (time_diff) == 1:
            current_time = temp_time

        if (is_index_changed):
            addRows(file_name, df, row_index)
            ##-- This break is IMPORTANT --##
            ##-- If we continue after changing the index, it will be a miscalculation of the index --##
            break

    ##-- If the index is not changed, it means there are no row to add more --##
    if not is_index_changed:
        output_file = os.path.join(output_data_path, file_name)
        covertToCsv(df, output_file)


def addDummyRowsKeystrokes(file_name):
    file_path = os.path.join(input_data_path, file_name)
    df = pd.read_csv(file_path)
    addRows(file_name, df)


def startMigration():
    createDirectoryIfNotExixts(data_dir)
    createDirectoryIfNotExixts(input_data_path)
    createDirectoryIfNotExixts(output_data_path)
    csv_file_names = find_filenames(input_data_path, ".csv")

    for file_name in csv_file_names:
        if fnmatch(file_name, '*ks*'):
            addDummyRowsKeystrokes(file_name)


            #####################################
            #####Delete column by row index######
            # df.drop(df.index[0], inplace = True)
            #####################################

            #####################################
            #####Delete column by column index#####
            # df.drop(df.columns[0], axis=1, inplace=True)
            #####################################

            #####################################
            #####Delete column by column name#####


startMigration()
