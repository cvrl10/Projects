from timestamp import timestamp
from tkinter import *
from tkinter import filedialog
from smtplib import SMTP_SSL
from ssl import create_default_context
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

email = 'cvrlix@gmail.com'
password = 'widfvyygdblbvsyp'

'''
with SMTP_SSL('smtp.gmail.com', port=465, context=context) as smtp:
    smtp.login(email, password)
    smtp.sendmail('cvrlix@gmail.com', 'carlarch10@gmail.com', 'Hello Carl from Python')'''


class Email:
    def __init__(self, smtp, receiver, recipient=(), subject=''):

        self.message = MIMEMultipart()
        self.message['To'] = receiver
        self.message['Subject'] = subject

        smtp.send_message(self.message)

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



class Application:
    def __init__(self, SMTP):
        self.SMTP = SMTP
        self.window = Tk()
        self.window.title('New Message')
        self.window.geometry('600x600')

        self.files = []

        self.recipients = Label(self.window, text='Recipients')
        self.recipients.pack(side=LEFT, anchor='n', padx=(15,0))

        self.recipients = Entry(self.window, textvariable=StringVar())
        self.recipients.pack(side=TOP, fill='x', expand=False, padx=(0,15))

        self.subject = Label(self.window, text='Subject')
        self.subject.pack(side=LEFT, anchor='n')

        self.subject = Entry(self.window, textvariable=StringVar())
        self.subject.pack(side=TOP, fill='x', expand=False, padx=(0,15))

        self.body = Label(self.window, text='Body')
        self.body.pack(side=LEFT, anchor='n')

        self.body = Text(self.window)
        self.body.pack(side=TOP, fill='x', expand=False, padx=(0,15))

        self.send = Button(self.window, text='Send', bg='blue', fg='white', command=self.send)
        self.send.pack(side=LEFT, anchor='n', padx=(0,5), pady=5)

        time = Label(self.window)
        _, text = timestamp(time)
        time.config(text=text)
        time.place(relx=1.0, rely=1.0, anchor='se')

        def getfiles():
            file = filedialog.askopenfilename()
            if file:
                self.files.append(file)


        self.attachment = Button(self.window, text='Attachment', command=lambda: getfiles())
        self.attachment.pack(side=LEFT, anchor='n', pady=5)

        self.delete = Button(self.window, text='Delete', bg='red', command=lambda: self.body.delete('1.0','end'))
        self.delete.pack(side=RIGHT, anchor='n', pady=5, padx=(0,15))

    def run(self):
        self.window.mainloop()

    def send(self):
        receiver, subject, text = '', self.recipients.get(), self.subject.get()
        mail = Email(self.SMTP, receiver=receiver, subject='test')
        text = self.body.get('1.0', END)
        mail.body(text=text)
        for file in self.files:
            mail.attachment = file

        with self.smtp:
            self.smtp.sendmail('cvrlix@gmail.com', mail.address, mail.message)



class Login:
    def __init__(self):
        app = Tk()
        app.title('emale')
        app.geometry('450x450')
        app.resizable('False', 'False')

        app.columnconfigure(0, weight=1)
        app.columnconfigure(1, weight=1)
        app.columnconfigure(2, weight=1)
        app.rowconfigure(0, weight=1)
        app.rowconfigure(1, weight=1)
        app.rowconfigure(2, weight=1)

        def rmvplchldr(event):
            if event.widget.get() == 'email':
                event.widget.delete(0, 'end')
            elif event.widget.get() == 'password':
                event.widget.delete(0, 'end')

        def onleave(event):
            widget = event.widget
            if widget.get() == '' and widget.name == 'email':
                widget.insert(0, 'email')
            elif widget.get() == '' and widget.name == 'password':
                widget.insert(0, 'password')
                if button.cget('text') == 'HIDE':
                    button.invoke()

            app.focus()

        def close():
            smtpd = self.connect()#
            self.thread.alive = False
            app.destroy()
            Application(smtpd).run()

        email = Entry(app, textvariable=StringVar())
        email.insert(0, 'email')
        email.name = 'email'
        email.grid(row=0, column=0, columnspan=3, sticky='sew', padx=50)
        email.bind('<Button-1>', rmvplchldr)
        email.bind('<Leave>', onleave)

        passwrd = Entry(app, textvariable=StringVar(), show='*')
        passwrd.insert(0, 'password')
        passwrd.name = 'password'
        passwrd.grid(row=1, column=0, columnspan=2, sticky='new', padx=(50, 0))
        passwrd.bind('<Button-1>', rmvplchldr)
        passwrd.bind('<Leave>', onleave)
        passwrd.bind('<Return>', lambda event: close())

        def onclick():
            if button.cget('text') == 'SHOW':
                passwrd.config(show='')
                button.config(text='HIDE', fg='red')
            else:
                passwrd.config(show='*')
                button.config(text='SHOW', fg='green')

        button = Button(app, text='SHOW', fg='green', command=onclick)
        button.grid(row=1, column=2, sticky='new', padx=(0, 50))

        login = Button(app, text='login', bg='red', command=lambda: close())
        login.grid(row=2, column=0, columnspan=3, sticky='new', padx=50)

        time = Label(app)
        self.thread, text = timestamp(time)
        time.config(text=text)
        time.place(relx=1.0, rely=1.0, anchor='se')
        self.connect()
        app.mainloop()

    def connect(self, email=email, password=password):
        context = create_default_context()
        with SMTP_SSL('smtp.gmail.com', port=465, context=context) as smtp:
            try:
                smtp.login(email, password)
                return smtp
            except Exception as exception:
                print(exception)



class App:
    def __init__(self):
        pass
    def run(self):
        Login()
