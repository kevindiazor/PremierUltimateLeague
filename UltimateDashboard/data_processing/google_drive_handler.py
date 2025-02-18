from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import os
import io
import zipfile

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def authenticate_google_drive():
    """Authenticate with Google Drive using OAuth 2.0"""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return creds

def download_game_day_folder(folder_id: str, destination_path: str):
    """Download entire Game Day Info folder from Google Drive"""
    creds = authenticate_google_drive()
    service = build('drive', 'v3', credentials=creds)
    
    def download_folder(folder_id, current_path):
        # List all files in the folder
        results = service.files().list(
            q=f"'{folder_id}' in parents",
            fields="files(id, name, mimeType)"
        ).execute()
        
        items = results.get('files', [])
        
        for item in items:
            if item['mimeType'] == 'application/vnd.google-apps.folder':
                # Create subfolder
                new_path = os.path.join(current_path, item['name'])
                os.makedirs(new_path, exist_ok=True)
                download_folder(item['id'], new_path)
            else:
                # Download file
                request = service.files().get_media(fileId=item['id'])
                fh = io.BytesIO()
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while done is False:
                    _, done = downloader.next_chunk()
                
                fh.seek(0)
                with open(os.path.join(current_path, item['name']), 'wb') as f:
                    f.write(fh.read())
    
    # Create base directory
    os.makedirs(destination_path, exist_ok=True)
    download_folder(folder_id, destination_path)

def extract_game_files(zip_path: str, extract_path: str):
    """Extract downloaded zip file"""
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
