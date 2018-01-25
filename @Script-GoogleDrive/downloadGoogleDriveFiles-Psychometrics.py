
# from __future__ import print_function
import httplib2
import os
import time
import shutil
import urllib.request
import io
import apiclient
# import discovery

from googleapiclient import discovery
from googleapiclient.http import MediaIoBaseDownload
# from apiclient import discovery
# from apiclient.http import MediaIoBaseDownload
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
# CLIENT_SECRET_FILE = 'T:\@CPL\DataMigrationScript\@Script-GoogleDrive\client_secrets.json'
CLIENT_SECRET_FILE = 'T:\@CPL\DataMigrationScript\@Script-GoogleDrive\client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'

class DriveFile:
    def __init__(self, fileName, fileId):
        self.fileName = fileName
        self.fileId = fileId


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def createDirectoryIfNotExixts(path):
    if not os.path.isdir(path):
        print(str(path) + ' has been created')
        os.mkdir(path)
    # else:
    #     print(str(path) + ' is already created')

def downloadFileUsingGoogleDriveApi(drive_service, file_id, fileName):
    request = drive_service.files().get_media(fileId=file_id)
    # request = drive_service.files().export_media(fileId=file_id, mimeType='application/pdf')
    # request = drive_service.files().export_media(fileId=file_id, mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    # request = drive_service.files().export_media(fileId=file_id, mimeType='application/vnd.google-apps.spreadsheet')

    # fh = io.BytesIO()
    dest_folder = "DownloadedData-Psychometrics"
    # shutil.rmtree(dest_folder, ignore_errors=True)
    createDirectoryIfNotExixts(dest_folder)
    # os.mkdir(dest_folder)
    fh = open(os.path.join(dest_folder,fileName), 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download " + str(status.progress() * 100))

def getFileList(drive_service, query):
    listOfDriveFiles = []
    page_token = None
    while True:
        response = drive_service.files().list(q=query,
                                             spaces='drive',
                                             fields='nextPageToken, files(id, name)',
                                             pageToken=page_token).execute()
        for file in response.get('files', []):
            # Process change
            driveFile = DriveFile(file.get("name"), file.get("id"))
            listOfDriveFiles.append(driveFile)
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
    return listOfDriveFiles

def getSubjectFolderList(drive_service, folderId):
    subjectFolderList = []
    page_token = None
    query = "'" + folderId + "' in parents and trashed=false and mimeType = 'application/vnd.google-apps.folder'"
    # "name = 'Test Track 2' and mimeType = 'application/vnd.google-apps.folder'"
    while True:
        response = drive_service.files().list(q=query,
                                             spaces='drive',
                                             fields='nextPageToken, files(id, name)',
                                             pageToken=page_token).execute()
        for file in response.get('files', []):
            # Process change
            if "Subject" in file.get('name'):
                subjectFolderList.append(file.get('id'))
                print('Found folder: %s (%s)' % (file.get('name'), file.get('id')))
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
    return subjectFolderList

def findFolder(drive_service, name):
    page_token = None
    query = "name = '" + name + "' and mimeType = 'application/vnd.google-apps.folder'"
    # "name = 'Test Track 2' and mimeType = 'application/vnd.google-apps.folder'"
    while True:
        response = drive_service.files().list(q=query,
                                             spaces='drive',
                                             fields='nextPageToken, files(id, name)',
                                             pageToken=page_token).execute()
        for file in response.get('files', []):
            # Process change
            print('Found file: %s (%s)' % (file.get('name'), file.get('id')))
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break

def findFile(drive_service, text_to_match, folderId):
    query = "'" + folderId + "' in parents and trashed=false"
    listOfResFiles = []
    subjectList = getFileList(drive_service, query)
    for subject in subjectList:
        if "Subject" in subject.fileName:
            time.sleep(1)
            sessionQuery = "'" + subject.fileId + "' in parents and trashed=false"
            sessionList = getFileList(drive_service, sessionQuery)
            for session in sessionList:
                if "1Baseline" in session.fileName or "2PracticeDrive" in session.fileName \
                        or "3NormalDrive" in session.fileName or "4CognitiveDrive" in session.fileName \
                        or "5MotoricDrive" in session.fileName or "6FinalDrive" in session.fileName:
                    time.sleep(1)
                    fileQuery = "'" + session.fileId + "' in parents and name contains '" + text_to_match + "' and trashed=false"
                    files = getFileList(drive_service, fileQuery)
                    for f in files:
                        listOfResFiles.append(f)
                        print(f.fileName)
                        # with open("fileList.txt", 'a') as out:
                        #     out.write(f.fileName + ',' + f.fileId + '\n')
    return listOfResFiles

def findFiles(drive_service, text_to_match, folderId):
    query = "'" + folderId + "' in parents"
    listOfResFiles = []
    subjectList = getFileList(drive_service, query)
    # print(subjectList)
    for subject in subjectList:
        # print(subject.fileName)
        if "Subject" in subject.fileName:
            time.sleep(1)
            fileQuery = "'" + subject.fileId + "' in parents and name contains '" + text_to_match + "' and trashed=false"
            files = getFileList(drive_service, fileQuery)
            for f in files:
                listOfResFiles.append(f)
                print(f.fileName)

        #     sessionQuery = "'" + subject.fileId + "' in parents"
        #     sessionList = getFileList(drive_service, sessionQuery)
        #     for session in sessionList:
        #         print(session.fileName)
        #         if "Baseline" in session.fileName or "PracticeDrive" in session.fileName \
        #                 or "NormalDrive" in session.fileName or "CognitiveDrive" in session.fileName \
        #                 or "MotoricDrive" in session.fileName or "FinalDrive" in session.fileName:
        #             time.sleep(1)
        #             fileQuery = "'" + session.fileId + "' in parents and name contains '" + text_to_match + "' and trashed=false"
        #             files = getFileList(drive_service, fileQuery)
        #             for f in files:
        #                 listOfResFiles.append(f)
        #                 print(f.fileName)
        #                 # with open("fileList.txt", 'a') as out:
        #                 #     out.write(f.fileName + ',' + f.fileId + '\n')
    return listOfResFiles


def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    # findFolder(service, "Test Track 2")
    # TT2: 0B00ugPsj4f4RLTg2b2ExZTBfcEU
    # SIM2: 0B00ugPsj4f4RTjZsNUlFRzJfMzA
    drive_id = "0B00ugPsj4f4RTjZsNUlFRzJfMzA"
    file_extension = ".tp"
    # file_extension = ".bar"
    list = findFiles(service, file_extension, drive_id)
    print(list)

    for f in list:
        time.sleep(1)
        # url = "https://www.googleapis.com/drive/v3/files/" + f.fileId + "/export"
        url = "https://www.googleapis.com/drive/v3/files/" + f.fileId + "?key=1NjecUW1A5PJWv3l9k6FQ3Kd"
        # url = "https://www.googleapis.com/drive/v3/files/" + f.fileId + "?alt=media"
        resp, content = http.request(url, "DELETE")
        print(f.fileName + " (" + f.fileId + "), " + str(resp.status))
        print("Downloading: " + f.fileName + " (" + f.fileId + ")")
        downloadFileUsingGoogleDriveApi(service, f.fileId, f.fileName)
        

    # subjects = getSubjectFolderList(service, "0B00ugPsj4f4RLTg2b2ExZTBfcEU")
    # for s in subjects:
    #     print(s)

    # with open("fileList.txt") as f:
    #     content = f.readlines()
    #
    # for line in content:
    #     time.sleep(1)
    #     line = line.replace('\n', '')
    #     str = line.split(",")
    #     id = str[1]
    #     name = str[0]
    #     url = "https://www.googleapis.com/drive/v3/files/" + id + "?key=1NjecUW1A5PJWv3l9k6FQ3Kd"
    #     resp, content = http.request(url, "DELETE")
    #     print(name + " (" + id + "), ")


if __name__ == '__main__':
    main()
