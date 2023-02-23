from smtplib import SMTP_SSL
from ssl import create_default_context
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

email = 'cvrlix@gmail.com'
password = 'widfvyygdblbvsyp'
context = create_default_context()

with SMTP_SSL('smtp.gmail.com', port=465, context=context) as smtp:
    smtp.login(email, password)
    smtp.sendmail('cvrlix@gmail.com', 'carlarch10@gmail.com', 'Hello Carl from Python')


class Email:
    def __init__(self, recipient, subject=''):
        self.message = MIMEMultipart()
        self.message['To'] = recipient
        self.message['Subject'] = subject

    def body(self, text='', html=''):
        if text:
            self.message.attach(MIMEText(text, 'plain'))
        if html:
            self.message.attach(MIMEText(html, 'html'))

    @property
    def address(self):
        return self.message['To']

    @property
    def attachment(self, path):
        with open(path, 'rb') as file:
            attachment = MIMEBase('application', 'octet-stream')
            attachment.set_payload(file.read())
            encoders.encode_base64(attachment)
            attachment.add_header('Content-Disposition', f"attachment: filename= {path.split('/')[-1]}")
            self.message.attach(attachment)

    @property
    def message(self):
        return self.message.as_string()