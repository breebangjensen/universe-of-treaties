# dowload google drive dataset
# function to work with the google api 
import os 
import io
from google_session import connect_google
from googleapiclient.http import MediaIoBaseDownload
import pandas as pd 

# Create a client to interact with the Google Drive API
CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

connection = connect_google(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

# list drives
connection.drives().list().execute()

# Shared Drive info and data directory 
drive_name = 'eScience Winter Incubator- Treaties'
drive_id = '0AE5H_6otegXCUk9PVA'
folder_id = '1_e6frSQQ50qy-mtZFYO53Ub4ERrkdTd4'

query = f"parents = '{folder_id}'"

response = connection.files().list(driveId=drive_id, includeItemsFromAllDrives=True, corpora = 'drive', supportsAllDrives = True, q=query).execute()
files = response.get('files')
nextPageToken = response.get('nextPageToken')

while nextPageToken:
    response = connection.files().list(driveId=drive_id, includeItemsFromAllDrives=True, corpora = 'drive', supportsAllDrives = True, q=query, pageToken=nextPageToken).execute()
    files.extend(response.get('files'))
    nextPageToken = response.get('nextPageToken')

# Create df of files in drive
# I'm thinking this will be useful to get a list of all files we need 
files_dir_view = pd.DataFrame(files)

# downloads from the api require individual file IDs or we can specify file types 
# etc. It's robust but we can streamline on Thursday.
# test example
file_ids = ['1oE2Ic7JffusJMZfuXDQu1UDATEQqUxBT']
file_name = ['some.pdf']

for file_id, file_name in zip(file_ids, file_name):
    request = connection.files().get_media(fileId=file_id)

    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fd=fh, request=request)
    done = False

    while not done:
        status, done = downloader.next_chunk()
        print('Download Progress {0}'.format(status.progress()*100))

    fh.seek(0)

    with open(file_name, 'wb') as f: # we can specify directory here
        f.write(fh.read())
        f.close()
