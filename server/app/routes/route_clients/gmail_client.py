# Clients
from google.oauth2.service_account import Credentials
from .email_client import EmailClient
from email.message import EmailMessage

# Utils
from googleapiclient.discovery import build as build_creds
import os, base64


class GmailClient(EmailClient):
    ''' Client to send emails via the GMail API 
    
        Requires the following environmental variables or arguments:
        - SENDER_EMAIL_ADDRESS
        - GMAIL_OAUTH_PROJECT_ID
        - GMAIL_OAUTH_PRIVATE_KEY
        - GMAIL_OAUTH_PRIVATE_KEY_ID
        - GMAIL_OAUTH_CLIENT_EMAIL
        - GMAIL_OAUTH_CLIENT_ID
        - GMAIL_OAUTH_CLIENT_X509_CERT_URL
    '''

    def __init__(self, template_path:str=None, sender_email_address:str=None,
                    project_id:str=None, private_key_id:str=None, private_key:str=None,
                    client_email:str=None, client_id:str=None, client_x509_cert_url:str=None) -> None:
        
        super().__init__(template_path=template_path, sender_email_address=sender_email_address)

        # Store credentials if passed or read from env
        self.project_id = project_id or os.environ.get('GMAIL_OAUTH_PROJECT_ID')
        self.private_key_id = private_key_id or os.environ.get('GMAIL_OAUTH_PRIVATE_KEY_ID')
        self.private_key = private_key or base64.b64decode(bytes(os.environ.get('GMAIL_OAUTH_PRIVATE_KEY', ''), 'utf-8')).decode('utf-8')
        self.client_email = client_email or os.environ.get('GMAIL_OAUTH_CLIENT_EMAIL')
        self.client_id = client_id or os.environ.get('GMAIL_OAUTH_CLIENT_ID')
        self.client_x509_cert_url = client_x509_cert_url or os.environ.get('GMAIL_OAUTH_CLIENT_X509_CERT_URL')

        # Login to GMail
        self.service = self._login()


    def _login(self):
        credentials = Credentials.from_service_account_info({
            "type": "service_account",
            "project_id": self.project_id,
            "private_key_id": self.private_key_id,
            "private_key": self.private_key,
            "client_email": self.client_email,
            "client_id": self.client_id,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": self.client_x509_cert_url
        }, scopes=['https://www.googleapis.com/auth/gmail.send'])

        credentials = credentials.with_subject(self.sender_email_address)

        service = build_creds('gmail', 'v1', credentials=credentials)

        return service


    def _generate_email_object(self, recipient_email_address:str, subject:str, text, type="plain") -> EmailMessage:
        ''' Create the email object to send '''

        email = EmailMessage()

        email['From'] = self.sender_email_address
        email['To'] = recipient_email_address
        email['Subject'] = subject

        # Add body content
        email.add_alternative(text, type)

        return email


    def _send_email(self, email:EmailMessage, _):
        ''' Internal method that invokes the actual client to send the message '''

        self.service.users().messages().send(userId='me', body={'raw': base64.urlsafe_b64encode(email.as_bytes()).decode()}).execute()
