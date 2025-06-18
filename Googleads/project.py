from google_auth_oauthlib.flow import InstalledAppFlow
import os
import pickle

# Define the scopes and client ID
CLIENT_ID = '766145919900-7k8e48035eq69ig7fnfhktc4bj01h7ej.apps.googleusercontent.com'
CLIENT_SECRET_FILE = 'client_secret.json'  # Download your client_secret.json from Google Developer Console
SCOPE = 'https://www.googleapis.com/auth/adwords'
REDIRECT_URI =  'http://127.0.0.1:8009/callback'  # For local testing

# The path to save the credentials
CREDENTIALS_PATH = 'google_ads_credentials.pkl'

# Perform OAuth authentication
def authorize():
    # Set up the flow using the client ID and secret
    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRET_FILE, scopes=[SCOPE])
    
    # Run the OAuth flow via the local server to get the authorization code
    credentials = flow.run_local_server(port=8009)  # Use port 8000 to match redirect URI


    # Save the credentials to a file for future use
    with open(CREDENTIALS_PATH, 'wb') as token:
        pickle.dump(credentials, token)

    return credentials

# Check if credentials already exist 
def load_credentials():
    if os.path.exists(CREDENTIALS_PATH):
        with open(CREDENTIALS_PATH, 'rb') as token:
            credentials = pickle.load(token)
        return credentials
    else:
        return None

# Run the authorization if no credentials are found
credentials = load_credentials()
if not credentials or not credentials.valid:
    credentials = authorize()
else:
    print("Credentials are already authorized and loaded.")

# Now you can use these credentials to access Google Ads API or Google Sheets API
