from os.path import join, dirname
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import AuthorizedSession
from google.oauth2.credentials import Credentials
import json

AUTH_TOKEN_FILE = './secrets/auth_token_file.json'
CLIENT_ID = './client_id.json'
SCOPES = ['https://www.googleapis.com/auth/photoslibrary',
          'https://www.googleapis.com/auth/photoslibrary.sharing']
GOOGLE_PHOTOS_API = 'https://photoslibrary.googleapis.com/v1/albums'


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


credentials = None
session = None

try:
    credentials = Credentials.from_authorized_user_file(
        AUTH_TOKEN_FILE, SCOPES)
except OSError as err:
    print("Error opening auth token file - {0}".format(err))

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

session = AuthorizedSession(credentials)
albums = session.get(
    GOOGLE_PHOTOS_API).json()

print(albums)
