import os
import csv
import re
import shutil

# Sessions will change according to the study
list_session = ['BaseLine', 'PracticeDrive', 'NormalDrive', 'CognitiveDrive', 'MotoricDrive', 'FinalDrive']

data_dir = "Data"
testing_dir = "Testing_dir"

vid_dir = "Video"
new_vid_dir = "Testing_video_dir"

##############################################
#####key.split('.')[n_key - 1] == 'mp4'#######
##############################################

def createDirectoryIfNotExixts(path):
    if not os.path.isdir(path):
        print(str(path) + ' has been created')
        os.mkdir(path)
    else:
        print(str(path) + ' is already created')


def createSubjectsAndSessions():
    for dirName, subdirList, fileList in os.walk(vid_dir):
        for fname in fileList:
            if (fname != "Order.csv" and fname != "order.csv" and fname != "config.csv"):
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

                    subfolder_path = os.path.join(new_vid_dir, name_subject)
                    createDirectoryIfNotExixts(subfolder_path)
                    for session in list_session:
                        createDirectoryIfNotExixts(os.path.join(subfolder_path, session))

                    path1 = os.path.join(dirName, fname)
                    path2 = os.path.join(new_vid_dir, name_subject, name_session, fname)

                    # os.rename(os.path.join(dirName, fname),
                    #           os.path.join(new_vid_dir, name_subject, name_session, fname))

                    ##################################
                    ##########COPYING VIDEO###########
                    ##################################
                    # shutil.copy2(path1, path2)


def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


##Create order file inside every subject consisting the session name
def createOrderFile():
    subject_list = get_immediate_subdirectories(new_vid_dir)
    for subject in subject_list:
        subject_path = os.path.join(new_vid_dir, subject)

        with open(os.path.join(subject_path, 'order.csv'), "a+", newline='') as subj:
            for session in list_session:
                writer = csv.writer(subj, delimiter=',')
                writer.writerow([session])
            subj.close()


##Create config file with the subject list
def createConfigFile():
    for sub in os.listdir(new_vid_dir):
        with open(os.path.join(new_vid_dir, 'config.csv'), "a+", newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow([sub])
            csv_file.close()


shutil.rmtree(new_vid_dir, ignore_errors=True)
createDirectoryIfNotExixts(new_vid_dir)
createSubjectsAndSessions()
createOrderFile()
createConfigFile()
