import pickle
from google.oauth2.credentials import Credentials

# Path to the credentials file
CREDENTIALS_PATH = 'google_ads_credentials.pkl'

# Load the credentials from the pickle file
with open(CREDENTIALS_PATH, 'rb') as token:
    credentials = pickle.load(token)

# Check if the refresh token is available and print it
if credentials.refresh_token:
    print(f"Refresh Token: {credentials.refresh_token}")
else:
    print("No refresh token found in the credentials.")


    