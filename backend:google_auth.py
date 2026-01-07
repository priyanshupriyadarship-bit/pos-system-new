{\rtf1\ansi\ansicpg1252\cocoartf2867
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 # backend/google_auth.py\
import json\
import os\
from google.oauth2.credentials import Credentials\
from googleapiclient.discovery import build\
\
def get_google_credentials():\
    """Load credentials from environment variable"""\
    token_json = os.getenv('GOOGLE_TOKEN')\
    \
    if not token_json:\
        raise ValueError("GOOGLE_TOKEN environment variable not set")\
    \
    token_data = json.loads(token_json)\
    \
    creds = Credentials(\
        token=token_data['token'],\
        refresh_token=token_data['refresh_token'],\
        token_uri=token_data['token_uri'],\
        client_id=token_data['client_id'],\
        client_secret=token_data['client_secret'],\
        scopes=token_data['scopes']\
    )\
    \
    return creds\
\
def get_gmail_service():\
    """Get Gmail API service"""\
    creds = get_google_credentials()\
    return build('gmail', 'v1', credentials=creds)\
\
def get_calendar_service():\
    """Get Calendar API service"""\
    creds = get_google_credentials()\
    return build('calendar', 'v3', credentials=creds)\
\
# Example: Send email\
def send_email(to, subject, body):\
    from email.mime.text import MIMEText\
    import base64\
    \
    service = get_gmail_service()\
    \
    message = MIMEText(body)\
    message['to'] = to\
    message['subject'] = subject\
    \
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()\
    \
    service.users().messages().send(\
        userId='me',\
        body=\{'raw': raw\}\
    ).execute()\
\
# Example: Create calendar event\
def create_calendar_event(summary, start_time, end_time):\
    service = get_calendar_service()\
    \
    event = \{\
        'summary': summary,\
        'start': \{'dateTime': start_time, 'timeZone': 'Asia/Kolkata'\},\
        'end': \{'dateTime': end_time, 'timeZone': 'Asia/Kolkata'\},\
    \}\
    \
    event = service.events().insert(\
        calendarId='primary',\
        body=event\
    ).execute()\
    \
    return event\
\
# backend/google_auth.py (add this)\
from google.auth.transport.requests import Request\
\
def get_refreshed_credentials():\
    """Get credentials and refresh if expired"""\
    creds = get_google_credentials()\
    \
    if creds.expired and creds.refresh_token:\
        creds.refresh(Request())\
        \
        # Save refreshed token back to environment\
        token_data = \{\
            'token': creds.token,\
            'refresh_token': creds.refresh_token,\
            'token_uri': creds.token_uri,\
            'client_id': creds.client_id,\
            'client_secret': creds.client_secret,\
            'scopes': creds.scopes\
        \}\
        \
        # Optional: Update environment variable\
        os.environ['GOOGLE_TOKEN'] = json.dumps(token_data)\
    \
    return crews\
}