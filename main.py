from os.path import join, dirname, exists
from os import makedirs
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import AuthorizedSession
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json
from urllib.request import urlretrieve as download

AUTH_TOKEN_FILE = './secrets/auth_token_file.json'
CLIENT_ID = './client_id.json'
SCOPES = ['https://www.googleapis.com/auth/photoslibrary',
          'https://www.googleapis.com/auth/photoslibrary.sharing']
GOOGLE_PHOTOS_API = 'https://photoslibrary.googleapis.com/v1/albums'
ALBUM_ID = 'AIg7YU3hCbEq6aDSrMkL63fwHhfot1RvHTfAa6nAnFTH4iwjfuSIvs24Qrlpc0QsRNxLgGeBFEvO62JYvgD1Gqtal19AE2pREA'
PHOTOS_SAVE_DIRECTORY = 'photos'


# Saves the auth token after going through auth flow
def save_credentials(cred, auth_file):
    cred_dict = {
        'token': cred.token,
        'refresh_token': cred.refresh_token,
        'id_token': cred.id_token,
        'scopes': cred.scopes,
        'token_uri': cred.token_uri,
        'client_id': cred.client_id,
        'client_secret': cred.client_secret
    }

    with open(auth_file, 'w') as f:
        print(json.dumps(cred_dict), file=f)


def write_photos_to_disk(mediaItems):
    for media in mediaItems:
        if 'image' in media['mimeType']:
            download_url = f"{media['baseUrl']}=d"

            if not exists(PHOTOS_SAVE_DIRECTORY):
                makedirs(PHOTOS_SAVE_DIRECTORY)

            download(download_url,
                     f"{PHOTOS_SAVE_DIRECTORY}/{media['filename']}")


credentials = None

try:
    credentials = Credentials.from_authorized_user_file(
        AUTH_TOKEN_FILE, SCOPES)
except:
    # This fails when we
    # 1. Don't have a auth token file, that's fine, we'll generate one by authing with a client ID
    # 2. The auth token file we have is malformed, again we'll generate a new one
    pass

if not credentials:
    auth_flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_ID,
        scopes=SCOPES)

    credentials = auth_flow.run_local_server(host='localhost',
                                             port=8080,
                                             authorization_prompt_message="",
                                             success_message='The auth flow is complete; you may close this window.',
                                             open_browser=True)

    save_credentials(credentials, AUTH_TOKEN_FILE)

google_photos_service = build('photoslibrary', 'v1', credentials=credentials)

results = google_photos_service.mediaItems().search(
    body={'albumId': ALBUM_ID}).execute()
write_photos_to_disk(results['mediaItems'])
