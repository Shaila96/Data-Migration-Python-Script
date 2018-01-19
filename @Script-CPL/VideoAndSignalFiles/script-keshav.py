import os
import csv
import re
import boto3


###ALL the folder names here are taken in order for local testing in my laptop. You need to be careful of what you are putting in those places

list1 = os.listdir('Test_new')

#Sessions will change according to the study
list_session = ['BaseLine', 'PracticeDrive', 'NormalDrive', 'CognitiveDrive', 'MotaricDrive', 'FinalDrive']

#temporary list for collecting the names of the subject
list2 = []

#this is reading from the file that contains all the csv file only 
#this is code where it is used when we have two seperate files for csv and there is a seperate file for videos 
for dirName,subdirList,fileList in os.walk('upload_to_subjectbook'):
	for fname in fileList:
		if(fname != "Order.csv" and fname != "order.csv" and fname != "config.csv"):
			if(fname.endswith(".csv")):
				name = fname.split('_')
				list2.append(name[0])

#set data structure will remove the duplicates
list3 = list(set(list2))
print(list3)

#we are making a new folder and creating the folder structure in that
os.mkdir("Tesing_script")

#making the folders for each subject and also the subfolders for each session 
#we are even putting the order file as well
for x in list3:
	os.mkdir(os.path.join('Tesing_script', x))
	path = os.path.join('Tesing_script', x)
	for y in list_session:
		os.mkdir(os.path.join(path, y))
		with open(os.path.join(path, 'Order.csv'), "a+", newline='') as csv_file:
		        writer = csv.writer(csv_file, delimiter=',')
		        writer.writerow([y])
		csv_file.close()

#config file:
#this is listing the files from the directory to get them in sorted order
for x in os.listdir('Tesing_script'):
	path = 'Tesing_script'
	with open(os.path.join(path, 'config.csv'), "a+", newline='') as csv_file:
		        writer = csv.writer(csv_file, delimiter=',')
		        writer.writerow([x])
	csv_file.close()

"""
#renaming all the files:
for dirName,subdirList,fileList in os.walk('Tesing_script'):
	for fname in fileList:
		if(fname != "Order.csv" and fname != "order.csv" and fname != "config.csv"):
			splitname = re.split('(\d+)', fname)
			
			#inital = 'T'
			#number = splitname[1]
			#extention =  splitname[2]
			#wordlist = 'main' + extention
			#folder = inital + number
			
			inital = 'T'
			number = splitname[1]
			name = ""
			for _ in range(0, len(fname.split('.')) - 1):
				name = name + fname.split('.')[_]

			real_name = ""
			for _ in range(1, len(name.split('_'))):
				real_name = real_name + "_" + name.split('_')[_]

			new_name = inital + number + real_name

			extention = fname.split('.')[len(fname.split('.')) - 1]
			#print(new_name)

			#print(dirName)
			#print(fname)
			
			print(fname)
			#os.rename(os.path.join('Tesing_script', ))
			#print(splitname)
"""
"""
with the above code we have finished creating the folder structure that is needed to copy the legacy files

The following will be the code to copy the csv files and video files
"""

#this is for csv files:
#'upload_to_subjectbook' is just a test folder that I have taken for this example
for dirName,subdirList,fileList in os.walk('upload_to_subjectbook'):
	for fname in fileList:
		if(fname != "Order.csv" and fname != "order.csv" and fname != "config.csv"):
			if(fname.endswith(".csv")):
				index_session = int(fname.split('_')[2]) - 1
				name = fname.split('_')[0]
				os.rename(os.path.join('upload_to_subjectbook', fname), os.path.join('Tesing_script', name, list_session[index_session], fname))



#this is for video files:
#'upload_to_subjectbook' is just a test folder that I have taken for this example
for dirName,subdirList,fileList in os.walk('upload_to_subjectbook'):
	for fname in fileList:
		if(fname != "Order.csv" and fname != "order.csv" and fname != "config.csv"):
			if(fname.endswith(".mp4")):
				path = os.path.join(dirName, fname)
				new_path = path.split('\\')[2]

				##Legacy data has done randomization in a very different way so this to check for the name of the session removing the randomization 
				splitname = re.split('(\d+)', new_path)
				name_session = ""
				if(len(splitname) > 1):
					name_session = splitname[1]
				else:
					name_session = new_path

				splitname_filename - re.split('(\d+)', fname)
				name_subject = "T" + splitname_filename[1]

				os.rename(os.path.join('upload_to_subjectbook',dirName, fname), os.path.join('Tesing_script', name_subject, name_session, fname))




"""
##Warning dont do this until you are sure that your folder and file names are similar to the once that are found online or else this will create an
##extra file not override the existing file in the bucket
#uploading to aws
session = boto3.Session(
    aws_access_key_id="AKIAIA2HXCWM5LZM7XVQ",
    aws_secret_access_key="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"
)
s3 = session.resource('s3')
#name of the bucket you want to upload needs to be mentioned
bucket = s3.Bucket('study01')
#path of the folder needs to be mentioned
for subdir, dirs, files in os.walk(path):
    for file in files:
        full_path = os.path.join(subdir, file)
        with open(full_path, 'rb') as data:
            full_path = full_path.replace('\\','/')
            bucket.put_object(Key=full_path[len(path) + 1:], Body=data)
            print(full_path)
"""