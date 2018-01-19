import os
import csv
import re
import boto3
import shutil

# Sessions will change according to the study
list_session = ['BaseLine', 'PracticeDrive', 'NormalDrive', 'CognitiveDrive', 'MotoricDrive', 'FinalDrive']

# temporary list for collecting the names of the subject
temp_list = []


data_dir = 'Data'

# vid_dir = "Video"
vid_dir = "T:\@CPL\TestingData"

# new_dir = "Testing_csv_dir"
new_dir = "T:\@CPL\Testing_dir"

order_file_name = "order.csv"
config_file_name = "config.csv"




def lowerCase(str):
    return str.lower()

def createDirectoryIfNotExixts(path):
    if not os.path.isdir(path):
        print(str(path) + ' has been created')
        os.mkdir(path)
    else:
        print(str(path) + ' is already created')

def isDirectoryExists(path):
    if not os.path.isdir(path):
        print(str(path) + ' is not there!')
        return False
    else:
        return True

def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

def getSubjectListFromCsv():
    for dirName, subdirList, fileList in os.walk(data_dir):
        for fname in fileList:
            if (lowerCase(fname) != lowerCase(order_file_name) and lowerCase(fname) != lowerCase(config_file_name)):
                if (fname.endswith(".csv")):
                    name = fname.split('_')
                    temp_list.append(name[0])

def createSubjectAndSessionFolders(subj_list):
    for subfolder in subj_list:
        subfolder_path = os.path.join(new_dir, subfolder)
        os.mkdir(subfolder_path)

        for session in list_session:
            os.mkdir(os.path.join(subfolder_path, session))
            with open(os.path.join(subfolder_path, order_file_name), "a+", newline='') as subfolder:
                writer = csv.writer(subfolder, delimiter=',')
                writer.writerow([session])
                subfolder.close()

# config file:
# this is listing the files from the directory to get them in sorted order
def createConfigFile():
    for sub in os.listdir(new_dir):
        with open(os.path.join(new_dir, config_file_name), "a+", newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow([sub])
        csv_file.close()

def copyCsvFiles():
    for directoryName, subdirectoryList, fileList in os.walk(data_dir):
        for fname in fileList:
            if (lowerCase(fname) != lowerCase(order_file_name) and lowerCase(fname) != lowerCase(config_file_name)):
                if (fname.endswith(".csv")):
                    index_session = int(fname.split('_')[2]) - 1
                    name = fname.split('_')[0]

                    path1 = os.path.join(data_dir, fname)
                    path2 = os.path.join(new_dir, name, list_session[index_session], fname)

                    # os.rename(os.path.join('upload_to_subjectbook', fname),
                    #           os.path.join('Tesing_script', name, list_session[index_session], fname))

                    shutil.copy2(path1, path2)


def copyVideoFiles():
    for dirName, subList, fileList in os.walk(vid_dir):
        for fname in fileList:
            # print(fileList)
            if (fname.endswith(".mp4")):
                path = os.path.join(dirName, fname)
                session_name = path.split('\\')[2]

                ##Legacy data has done randomization in a very different way so this to
                ##check for the name of the session removing the randomization
                split_name = re.split('(\d+)', session_name)
                name_session = ""

                if (len(split_name) > 1):
                    name_session = split_name[2]
                else:
                    name_session = session_name

                split_name = re.split('(\d+)', fname)
                name_subject = "T0" + split_name[1]

                subject_path = os.path.join(new_dir, name_subject)

                if isDirectoryExists(subject_path):
                    path1 = os.path.join(dirName, fname)
                    path2 = os.path.join(new_dir, name_subject, name_session, fname)

                    # os.rename(os.path.join(dirName, fname),
                    #           os.path.join(new_vid_dir, name_subject, name_session, fname))

                    # shutil.copy2(path1, path2)
                else:
                    continue


def makeFolderStructure():
    shutil.rmtree(new_dir, ignore_errors=True)
    getSubjectListFromCsv()
    createDirectoryIfNotExixts(new_dir)

    # set data structure will remove the duplicates
    subject_list = list(set(temp_list))

    createSubjectAndSessionFolders(subject_list)
    createConfigFile()






# makeFolderStructure()
# copyCsvFiles()


copyVideoFiles()

