import os
from os import listdir
import pandas as pd


data_dir = "Data"
new_file_extension = ".csv"


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

def find_filenames(path_to_dir, suffix):
    filenames = listdir(path_to_dir)
    return [filename for filename in filenames if filename.endswith(suffix)]

def get_file_path_without_extension(file_path):
    return file_path[:file_path.rfind(".xlsx")]

def get_file_name_without_extension(file_path):
    return file_path[file_path.rfind("\\") + 1:file_path.rfind(".xlsx")]


def getCsvFileName(file_name):
    return get_file_name_without_extension(file_name) + new_file_extension

def convertFile(file_path, file_name):
    xl = pd.ExcelFile(file_path)
    print(xl.sheet_names)
    csv_file = getCsvFileName(file_name)
    print(csv_file)

    df = pd.read_excel(file_path, sheet_name='Sheet1')



def convertExcelToCsv():
    createDirectoryIfNotExixts(data_dir)
    excel_file_names = find_filenames(data_dir, ".xlsx")
    print(excel_file_names)

    for file_name in excel_file_names:
        file_path = os.path.join(data_dir, file_name)
        convertFile(file_path, file_name)


####STARTING OF THE SCRIPT####
convertExcelToCsv()
