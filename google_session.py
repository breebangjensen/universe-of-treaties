# Initiate instance with GoogleDrive API
# you will need to enable your api and generate a key
# `GoogleAuth` will look for a "credentials.json" in the base directory
# see: https://developers.google.com/drive/api/v3/quickstart/python

import pickle
import os

from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request

def connect_google(client_secret_file, api_name, api_version, *scopes):
    CLIENT_SECRET_FILE = client_secret_file
    API_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]

    cred = None
    
    pickle_file = f'token_{API_NAME}_{API_VERSION}.pickle'

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.espired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)
        
    try:
        service = build(API_NAME, API_VERSION, credentials=cred)
        print(API_NAME, 'Success!')
        return service
    except Exception as er:
        print('Failure to connect.')
        print(er)
        return None
