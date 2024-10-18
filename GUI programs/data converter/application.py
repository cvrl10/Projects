from eirich import Eirich

from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Separator
from tkcalendar import DateEntry

from datetime import date
import os
import re
import webbrowser
import logging

logfile = 'eirich.log'
logging.basicConfig(filename=logfile, filemode='w')
logger = logging.getLogger(logfile)


input_file = ''
output_file = ''
logfile = 'eirich.log'

ok_color = '#abf7b1'
ok_color = '#5ced73'

def enable(root, window):
    if input_file and window=='open':
        file = open(input_file, 'r')
        arr = file.readlines()

        try:
            frame = root.children['frame_1']
            begin = frame.children['!dateentry']
            end = frame.children['!dateentry2']
            begin.configure(state='active')
            end.configure(state='active')

            year, month, day = map(int, extract_date(arr[1]).split('-'))
            begin.set_date(date(year, month, day))

            year, month, day = map(int, extract_date(arr[-1]).split('-'))
            end.set_date(date(year, month, day))
        except Exception as e:
            logger.warning(f"Can't extract date from source file")
            print(f"can't extract date from source file or \n{e}")

    if input_file and output_file:
        button = root.children['frame_3'].children['button']
        button.configure(state='active')


def askopen(root):
    global input_file
    button = root.children['frame_0'].children['button']
    label = root.children['frame_0'].children['label']
    path = filedialog.askopenfilename()

    if path:
        input_file = os.path.abspath(path)
        button.configure(bg=ok_color)
        arr = input_file.split('\\')
        if len(arr) > 1:
            label.configure(text=arr[-1])
        else:
            label.configure(text=input_file.split('/')[-1])

    enable(root, window='open')


def asksave(root):
    global output_file
    button = root.children['frame_2'].children['button']
    label = root.children['frame_2'].children['label']
    path = filedialog.asksaveasfilename()

    if path:
        output_file = os.path.abspath(path)
        button.configure(bg=ok_color)
        arr = output_file.split('\\')
        if len(arr) > 1:
            label.configure(text=arr[-1])
        else:
            label.configure(text=output_file.split('/')[-1])

    enable(root, window='save')


def process(root):
    frame = root.children['frame_1']
    begin = frame.children['!dateentry']
    end = frame.children['!dateentry2']

    eirich = Eirich(input_file, output_file, from_date=str(begin.get_date()), to_date=str(end.get_date()))
    eirich.process()


def extract_date(row):
    match = re.search(r'[0-9]{2}.[0-9]{2}.[0-9]{4}', row)
    day, month, year = match.group().split('.')
    date = '-'.join([year, month, day])
    return date


class App:
    def __init__(self):
        self.root = Tk()
        self.root.iconbitmap(os.path.abspath('img/Clariant.ico'))
        self.root.geometry('250x350')
        self.root.title('Eirich v1.1')
        self.root.resizable(False, False)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=2)
        self.root.rowconfigure(1, weight=2)
        self.root.rowconfigure(2, weight=2)
        self.root.rowconfigure(3, weight=1)

        input_frame = Frame(self.root, name='frame_0')
        input_frame.grid(row=0, sticky='nsew')
        input_frame.columnconfigure(0, weight=1)
        input_frame.rowconfigure(0, weight=1)
        input_frame.rowconfigure(1, weight=1)

        self.input_button = Button(input_frame, name='button', text='Select input file', command= lambda: askopen(self.root))
        self.input_button.grid(row=0, sticky='s')
        self.input_label = Label(input_frame, name='label', text='No input file selected')
        self.input_label.grid(row=1, sticky='n')

        input_seperator = Separator(input_frame, orient='horizontal')
        input_seperator.grid(row=1, sticky='ews')

        date_range_frame = Frame(self.root, name='frame_1')
        date_range_frame.grid(row=1, sticky='nsew')
        date_range_frame.columnconfigure(0, weight=1)
        date_range_frame.rowconfigure(0, weight=1)
        date_range_frame.rowconfigure(1, weight=1)
        date_range_frame.rowconfigure(2, weight=1)

        date_range_label = Label(date_range_frame, text='Select input file before setting date range')
        date_range_label.grid(row=0, sticky='sew')

        begin = DateEntry(date_range_frame)
        begin.grid(row=1, sticky='s')
        begin.configure(state='disabled')

        end = DateEntry(date_range_frame)
        end.grid(row=2, sticky='n')
        end.configure(state='disabled')

        date_range_seperator = Separator(date_range_frame, orient='horizontal')
        date_range_seperator.grid(row=2, sticky='ews')

        output_frame = Frame(self.root, name='frame_2')
        output_frame.grid(row=2, sticky='nsew')
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        output_frame.rowconfigure(1, weight=1)

        self.output_button = Button(output_frame, name='button', text='Select output file', command=lambda: asksave(self.root))
        self.output_button.grid(row=0, sticky='s')
        self.output_label = Label(output_frame, name='label', text='No output file selected')
        self.output_label.grid(row=1, sticky='n')

        output_seperator = Separator(output_frame, orient='horizontal')
        output_seperator.grid(row=1, sticky='ews')

        process_frame = Frame(self.root, name='frame_3')
        process_frame.grid(row=3)

        self.process_button = Button(process_frame, name='button', text='Process', command=lambda: process(self.root))
        self.process_button.pack(pady=5)
        self.process_button.configure(state='disabled')

        self.root.bind('<Control-l>', lambda event: webbrowser.open(logfile))

    def run(self):
        self.root.mainloop()
