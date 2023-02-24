from smtplib import SMTP, SMTP_SSL
from ssl import create_default_context

email = 'cvrlix@gmail.com'
password = ''
context = create_default_context()
'''
with SMTP_SSL('smtp.gmail.com', port=465, context=context) as smtp:
    smtp.login(email, password)
    smtp.sendmail('cvrlix@gmail.com', 'carlarch10@gmail.com', 'Hello Carl from Python')
'''

from application import App

app = App()
app.run()

