import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from utils.logger import logger

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def connect_gmail():
  """Shows basic usage of the Gmail API.
  Lists the user's Gmail labels.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    logger.info("Started with the Gmail Authentication")
    # Call the Gmail API
    service = build("gmail", "v1", credentials=creds)
    print("Service:", service)
    results = service.users().labels().list(userId="me").execute()
    labels = results.get("labels", [])
    profile = service.users().getProfile(userId="me").execute()
    connected_user_email = profile["emailAddress"]

    if not labels:
      print("No labels found.")
      return
    print("Labels:")
    for label in labels:
      print(label["name"])

    logger.info("Authenticaion completed")
    logger.info("Connected to Gmail API successfully")

    return service, connected_user_email

  except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    print(f"An error occurred: {error}")
    logger.error(f"Cant connect to the Gmail API due to {error}")



# def get_gmail_service():

#     creds = None

#     if os.path.exists("token.json"):
#         creds = Credentials.from_authorized_user_file(
#             "token.json",
#             SCOPES
#         )

#     if not creds or not creds.valid:

#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())

#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 "credentials.json",
#                 SCOPES
#             )

#             creds = flow.run_local_server(port=0)

#         with open("token.json", "w") as token:
#             token.write(creds.to_json())

#     service = build(
#         "gmail",
#         "v1",
#         credentials=creds
#     )

#     logger.info("Connected to Gmail API successfully")

#     return service

if __name__ == "__main__":
  connect_gmail()