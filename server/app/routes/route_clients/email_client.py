# Clients
import os, smtplib

# Email utils
from email.message import EmailMessage
from email.headerregistry import Address


class EmailClient():
    ''' Client to send emails via SMTP '''

    DEFAULT_EMAIL_SERVER = "smtp.gmail.com"
    DEFAULT_EMAIL_SERVER_PORT = 587
    TEMPLATE_PATH = "/app/templates/email"

    def __init__(self, email_server:str=None, email_port:int=None, template_path:str=None,
                    sender_email_address:str=None, sender_email_password:str=None) -> None:

        # Allow user specified email server to override the default
        if email_server:
            self.DEFAULT_EMAIL_SERVER = email_server

        # Allow user specified email server port to override the default
        if email_port:
            self.DEFAULT_EMAIL_SERVER_PORT = email_port

        # Allow user specified email template path to override the default
        if template_path:
            self.TEMPLATE_PATH = template_path

        # The default outgoing email address info
        self.sender_email_address = sender_email_address or os.environ.get('SENDER_EMAIL_ADDRESS')
        self.sender_email_password = sender_email_password or os.environ.get('SENDER_EMAIL_PASSWORD')


    def _templatize_text(self, text, template_name, template_values) -> str:
        ''' Validate arguments and apply template values to template if passed '''

        # Handle errors
        if not text and not template_name:
            raise ValueError('send_email() must be passed email body text or the name of an HTML template')

        if text and template_name:
            raise ValueError('send_email() cannot be passed both email body text and the name of an HTML template')

        if template_name:
            text = self._generate_email_body_from_template(template_name, template_values)

        return text


    def _send_email(self, email:EmailMessage, recipient_email_address:str):
        ''' Internal method that invokes the actual client to send the message '''

        # Open client and connect
        client = smtplib.SMTP(self.DEFAULT_EMAIL_SERVER, self.DEFAULT_EMAIL_SERVER_PORT)
        client.ehlo()
        client.starttls()

        # Login and send email
        client.login(self.sender_email_address, self.sender_email_password)
        client.sendmail(self.sender_email_address, recipient_email_address, email.as_string())
        
        client.quit()


    def send_email(self, recipient_email_address:str, subject:str, text:str=None, template_name:str=None, template_values:dict=None):
        ''' Send an email to a recipient with plain text or using an HTML template 
            
            Templates should be specified by their name in the TODO - FOLDER folder
            
            A map of template values should be passed if a template is used to populate the template
        '''

        # Generate email from template and values if passed
        text = self._templatize_text(text, template_name, template_values)
            
        # Create the email object
        email = self._generate_email_object(recipient_email_address, subject, text, 'plain' if not template_name else 'html')

        # Use the client to send the email object
        self._send_email(email, recipient_email_address)


    def _generate_email_object(self, recipient_email_address:str, subject:str, text, type="plain") -> EmailMessage:
        ''' Create the email object to send '''

        email = EmailMessage()

        email['From'] = Address(domain=self.sender_email_address)
        email['To'] = Address(domain=recipient_email_address)
        email['Subject'] = subject

        # Add body content
        email.add_alternative(text, type)

        return email


    def _generate_email_body_from_template(self, template_name:str, template_values:dict) -> str:
        ''' Generate an email body using the name of an HTML template and the keys/values to populate '''

        # Load the specified template and populate with passed values
        with open(f"{self.TEMPLATE_PATH}/{template_name}.html") as template_file:
            template = template_file.read()
            formatted_template = self._format_template(template, template_values)

        return formatted_template


    def _format_template(self, template:str, template_values:dict):
        ''' Format the template '''

        for key, value in template_values.items():
            template = template.replace("{" + key + "}", value)

        return template