# dowload google drive dataset
# function to work with the google api 
from google_session import connect_google
import pandas as pd 

this_file_path = os.path.abspath(__file__)

project_root = os.path.split(this_file_path)[0]

path_data = os.path.join(project_root, "data") + '/'

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

files_dir_view = pd.DataFrame(files)