from utility import *
from tkinter import *
from tkinter import filedialog
from smtplib import SMTP_SSL
from ssl import create_default_context
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from threading import Timer


TIMEOUT = 6


class Email:
    def __init__(self, receiver, recipient=(), subject=''):
        self.msg = MIMEMultipart()
        self.msg['To'] = receiver
        self.msg['Subject'] = subject


    def body(self, text='', html=''):
        if text:
            self.msg.attach(MIMEText(text, 'plain'))
        if html:
            self.msg.attach(MIMEText(html, 'html'))

    @property
    def address(self):
        return self.msg['To']

    def attach(self, path):
        with open(path, 'rb') as file:
            attachment = MIMEBase('application', 'octet-stream')
            attachment.set_payload(file.read())
            encoders.encode_base64(attachment)
            attachment.add_header('Content-Disposition', f"attachment; filename={path.split('/')[-1]}")
            self.msg.attach(attachment)

    @property
    def message(self):
        return self.msg.as_string()


class Application:
    def __init__(self, user=(), login=None):
        self.user, self.password = user
        self.window = Tk()
        self.window.title('New Message')
        self.window.geometry('600x600')

        self.files = []

        self.menubar = Menu(self.window)
        self.file = Menu(self.menubar, tearoff=0)

        def getfiles():
            file = filedialog.askopenfilename()
            if file:
                self.files.append(file)

        def close():
            if login:
                self.window.destroy()
                login(*user)
            else:
                self.window.destroy()

        self.file.add_command(label='New', command=lambda: Application(user, None).run())
        self.file.add_command(label='Open', command=getfiles)
        self.file.add_command(label='Send', command=self.send)
        self.file.add_command(label='Close', command=close)
        self.file.add_separator()
        self.file.add_command(label='Exit', command=lambda: self.window.destroy())

        self.menubar.add_cascade(label='File', menu=self.file)

        self.window.config(menu=self.menubar)

        self.recipients = Label(self.window, text='Recipients')
        self.recipients.pack(side=LEFT, anchor='n', padx=(15, 0))

        self.recipients = Entry(self.window, textvariable=StringVar())
        self.recipients.pack(side=TOP, fill='x', expand=False, padx=(0, 15))

        self.subject = Label(self.window, text='Subject')
        self.subject.pack(side=LEFT, anchor='n')

        self.subject = Entry(self.window, textvariable=StringVar())
        self.subject.pack(side=TOP, fill='x', expand=False, padx=(0, 15))

        self.body = Label(self.window, text='Body')
        self.body.pack(side=LEFT, anchor='n')

        self.body = Text(self.window)
        self.body.pack(side=TOP, fill='x', expand=False, padx=(0, 15))

        self.send = Button(self.window, text='Send', bg='blue', fg='white', command=self.send)
        self.send.pack(side=LEFT, anchor='n', padx=(0, 5), pady=5)

        time = Label(self.window)
        text = timestamp(time)
        time.config(text=text)
        time.place(relx=1.0, rely=1.0, anchor='se')

        self.attachment = Button(self.window, text='Attachment', command=lambda: getfiles())
        self.attachment.pack(side=LEFT, anchor='n', pady=5)

        self.delete = Button(self.window, text='Delete', bg='red', command=lambda: self.body.delete('1.0', 'end'))
        self.delete.pack(side=RIGHT, anchor='n', pady=5, padx=(0, 15))

    def run(self):
        self.window.mainloop()

    def send(self):
        for recipient in self.recipients.get().split(','):
            subject, text = self.subject.get(), self.body.get('1.0', END)
            mail = Email(receiver=recipient, subject=subject)
            mail.body(text=text)
            for file in self.files:
                mail.attach(file)

            context = create_default_context()
            with SMTP_SSL('smtp.gmail.com', port=465, context=context) as smtp:
                smtp.login(self.user, self.password)
                smtp.sendmail('cvrlix@gmail.com', mail.address, mail.message)


class Login:
    def __init__(self, user=None, password=None):
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
            if email.get() == 'email':
                frame.grid(row=0, column=0, columnspan=3, sticky='nsew', padx=20, pady=20)
                frame.columnconfigure(0, weight=1)
                frame.rowconfigure(0, weight=1)
                frame.rowconfigure(1, weight=1)
                message.grid(row=0, sticky='nsew', padx=30, pady=(30, 0))
                var.set('Please specify email/password')
                Log().write(var.get())
                ok.grid(row=1, sticky='e', padx=30)

                def okclick():
                    try:
                        ok.invoke()
                    except:
                        pass

                thread = Timer(TIMEOUT, function=okclick)
                thread.start()
                return

            user = (email.get(), passwrd.get())
            print(*user)
            if self.connect(*user):
                #ok.invoke()
                app.destroy()
                Application(user, login=Login).run()

        frame = Frame(app, bg='#F8F3D6')
        var = StringVar()
        message = Message(frame, bg='#F8F3D6', textvariable=var, justify=LEFT, anchor='nw', aspect=700)
        ok = Button(frame, text='OK', bg='blue', fg='white', command=frame.grid_forget)

        email = Entry(app, textvariable=StringVar())
        email.insert(0, user if user else 'email')
        email.name = 'email'
        email.grid(row=0, column=0, columnspan=3, sticky='sew', padx=50, pady=(20, 0))
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
                button.config(text='HIDE', fg='red', highlightbackground='red')
            else:
                passwrd.config(show='*')
                button.config(text='SHOW', fg='green', highlightbackground='green')

        button = Button(app, text='SHOW', fg='green', highlightbackground='green', command=onclick)
        button.grid(row=1, column=2, sticky='new', padx=(0, 50))

        login = Button(app, text='Login', bg='red', command=lambda: close())
        login.grid(row=2, column=0, columnspan=3, sticky='new', padx=50)

        time = Label(app)
        text = timestamp(time)
        time.config(text=text)
        time.place(relx=1.0, rely=1.0, anchor='se')
        app.mainloop()

    def connect(self, email, password):
          context = create_default_context()
          with SMTP_SSL('smtp.gmail.com', port=465, context=context) as smtp:
              try:
                  return smtp.login(email, password)
              except Exception as exception:
                  Log().write(str(exception))


class App:
    def __init__(self):
        pass

    def run(self):
        Login()