import os
import csv
import re
import boto3

###ALL the folder names here are taken in order for local testing in my laptop. You need to be careful of what you are putting in those places
list1 = os.listdir('.')
# print(list1)
# ['.idea', 'script.py', 'test.py']


# Sessions will change according to the study
list_session = ['BaseLine', 'PracticeDrive', 'NormalDrive', 'CognitiveDrive', 'MotaricDrive', 'FinalDrive']

# temporary list for collecting the names of the subject
temp_list = []
data_dir = 'Data'

# this is reading from the file that contains all the csv file only
# this is code where it is used when we have two seperate files for csv and there is a seperate file for videos
for dirName, subdirList, fileList in os.walk(data_dir):
    for fname in fileList:
        # print("\nfname: ")
        # print(fname)
        if (fname != "Order.csv" and fname != "order.csv" and fname != "config.csv"):
            if (fname.endswith(".csv")):
                ##Ques: why to split by '_' ?????
                name = fname.split('_')
                # print("\nName: ")
                # print(name)
                temp_list.append(name[0])

# set data structure will remove the duplicates
subfolder_list = list(set(temp_list))
# print(csv_list)


new_dir = "Testing_dir"
# we are making a new folder and creating the folder structure in that
if not os.path.isdir(new_dir):
    print('Testing_dir has been created')
    os.mkdir(new_dir)
    # os.system('mkdir Testing_dir')
else:
    print('Testing_dir is already created')

# making the folders for each subject and also the subfolders for each session
# we are even putting the order file as well
for subfolder in subfolder_list:
    subfolder_path = os.path.join(new_dir, subfolder)
    os.mkdir(subfolder_path)
    # print(subfolder_path)

    for session in list_session:
        os.mkdir(os.path.join(subfolder_path, session))
        with open(os.path.join(subfolder_path, 'Order.csv'), "a+", newline='') as subfolder:
            writer = csv.writer(subfolder, delimiter=',')
            writer.writerow([session])
            subfolder.close()

# config file:
# this is listing the files from the directory to get them in sorted order
for sub in os.listdir(new_dir):
    # print("\nX:")
    # print(sub)
    # path = new_dir
    with open(os.path.join(new_dir, 'config.csv'), "a+", newline='') as csv_file:
        # print("\ncsv_file:")
        # print(csv_file)
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow([sub])
    csv_file.close()



                ###The method walk() generates the file names in a directory tree by walking the tree either top-down or bottom-up.###
                # for root, dirs, files in os.walk(".", topdown=True):
                # print("\nRoot: ")
                # print(root)
                # print("\nDirs:")
                # print(dirs)
                # print("\nFiles:")
                # print(files)

                # for name in files:
                #     print(os.path.join(root, name))
                # for name in dirs:
                #     print(os.path.join(root, name))
