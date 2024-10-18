import os
import io
import re
import random
import csv
import pandas as pd
from collections import defaultdict

import logging

logfile = 'eirich.log'
logging.basicConfig(filename=logfile, filemode='w')
logger = logging.getLogger(logfile)

from pandas.io.formats import excel
excel.ExcelFormatter.header_style = None

pd.options.display.width = 0

NORMAL = 'NORMAL' #i = 2 and j = 1
KEY_MISSING = 'KEY_MISSING' #i = 1
RADIX = 'RADIX' #i = 3
RADIX_KEY_MISSING = 'RADIX_KEY_MISSING' #i = 2 and j = 3
SKIP = 'SKIP'
CHANGE_KEY = 'CHANGE_KEY'


def remove_commas(row):
    row = row.replace(',', ' ', 1)
    row = row.replace(',', '', 1)
    return row


def counting_to_seven(i):
    i += 1
    return i%7


def add_join_key(arr, key): #add join key last, order mather based on how I wrote this
    arr.append(key)


def add_radix(arr, ignore=''):
    arr[0] = f'{arr[0][:-1]}.'
    arr[0] += f'{arr.pop(1)}'
    arr[0] += '"' #needed


def add_both(arr, key):
    add_join_key(arr, key)
    add_radix(arr)


def get_key(arr):
    try:
        int(arr[-1])
        return arr[-1]
    except:
        return None


def create_key():
    key = ['0']
    for i in range(4):
        key.append(random.choice(['0','1','2','3','4','5','6','7','8','9']))
    return ''.join(key)


def parse(row):
    if re.search(r'\$RT_[A-Z]+\$', row):
        logger.warning(row)
        return SKIP, []

    arr = re.split(f'[{chr(32)}|\t]', row)

    arr[0] += f' {arr.pop(1)}'
    i = len(arr)

    if arr[-1]=='\n': #another special case from the ideal test file, where a tab is used to seperate the key leading to a false radix classification
        arr.pop(i-1)

    i = len(arr)

    if i==1:
        return KEY_MISSING, arr
    if i==3:
        return RADIX, arr

    j = len(arr[-1].split(';'))

    if j==3:
        return RADIX_KEY_MISSING, arr
    else:
        return NORMAL, arr


def do_nothing():
    def foo(arr, key):
        arr[1] = key
    return foo


def change_key(arr, key):
    do_nothing()(arr, key)


func = defaultdict(do_nothing)

func[KEY_MISSING] = add_join_key
func[RADIX] = add_radix
func[RADIX_KEY_MISSING] = add_both
func[CHANGE_KEY] = do_nothing()


class Eirich:
    def __init__(self, input_file, output_file=None, from_date='', to_date=''):
        self.input_file = input_file
        self.output_file = output_file
        self.from_date = from_date
        self.to_date = to_date

    def process(self):
        file = open(self.input_file, 'r')
        header = file.readline()

        if re.search(r',,$', header):
            no_commas = io.StringIO('')
            header = header.replace(',', '')
            no_commas.write(header)

            for row in file.readlines():
                row = remove_commas(row)
                no_commas.write(row)

            file.close()
            file = no_commas
            file.seek(0)
            header = file.readline()

        header = header.replace(';', ',')
        header = header.replace('"', '')
        header = header.replace('\n', '')
        header = f'{header},group_id'

        clean = open('clean.csv', 'w', newline='')
        output = csv.writer(clean)

        headers = header.split(',')
        output.writerow(headers)

        i = 0
        for DATA in file.readlines():
            ROW_TYPE, arr = parse(DATA)

            if ROW_TYPE==SKIP:
                continue

            key = get_key(arr)

            if i==0 and not key:
                key = create_key()
                use_previous_key = key
                func[ROW_TYPE](arr, key)
            elif i and (not key or key != use_previous_key):
                func[ROW_TYPE](arr, use_previous_key)
                func[CHANGE_KEY](arr, use_previous_key)
            else:
                use_previous_key = key
                func[ROW_TYPE](arr, key)

            arr[1] = f',{arr[1]}'
            arr[0] += f'{arr.pop(1)}'
            row = ''.join(arr)
            row = row.replace(';', ',')
            row = row.replace('"', '')
            row = row.replace('\n', '')
            row = row.split(',')
            output.writerow(row)

            i = counting_to_seven(i)

        file.close()
        clean.close()

        dfs = []

        file = open('clean.csv')
        file.readline()

        i = 0
        for line in file.readlines():
            column = headers.copy()
            line = line.replace('\n','').split(',')
            column[0] = line[0]
            data = {column[i]: [line[i]] for i in range(len(line))}
            data[f'{column[0]}'] = data['VarValue']
            data.pop('VarValue')
            data.pop('Validity')
            data.pop('Time_ms')

            if i==0:
                df = pd.DataFrame.from_dict(data)

            elif i==6:
                temp = pd.DataFrame.from_dict(data)
                df = pd.merge(df, temp, on=['group_id', 'TimeString'])
                dfs.append(df)

            else:
                temp = pd.DataFrame.from_dict(data)
                df = pd.merge(df, temp, on=['group_id', 'TimeString'])

            i = counting_to_seven(i)

        file.close()
        os.remove('clean.csv')
        df = pd.concat(dfs, ignore_index=True)

        dates = []
        times = []

        for timestring in df['TimeString']:
            date, time = timestring.split()
            dates.append(date)
            times.append(time)

        df = df.drop(columns='TimeString')
        df = df.drop(columns='group_id')

        df.insert(1, 'Date [yyyy-MM-dd]', dates)
        df.insert(2, 'Time [hh:mm:ss]', times)
        df['Date [yyyy-MM-dd]'] = pd.to_datetime(df['Date [yyyy-MM-dd]'], dayfirst=True)

        column = df.pop('HMI_Rotor_VFD_Speed_Setpoint1')
        df.insert(4, 'HMI_Rotor_VFD_Speed_Setpoint1', column)

        df = df.loc[df['Date [yyyy-MM-dd]'].between(self.from_date, self.to_date)]
        writer = pd.ExcelWriter(self.output_file, datetime_format='YYYY-MM-DD', engine='xlsxwriter',
                                engine_kwargs={'options': {'strings_to_numbers': True}})

        df.to_excel(writer, sheet_name='Eirich data', index=False)

        workbook = writer.book
        worksheet = writer.sheets['Eirich data']
        worksheet.autofit()
        worksheet.freeze_panes(1, 0)
        header_format = workbook.add_format()
        header_format.set_bold()
        worksheet.set_row(0, None, header_format)
        workbook.read_only_recommended()
        workbook.set_properties(
            {
                'author': 'Carl Archemetre',
                'company': 'Clariant',
                'comments': 'Created with Python, pandas.DataFrame and XlsxWriter'
            }
        )
        writer.close()
