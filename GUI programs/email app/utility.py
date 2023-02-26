from threading import Thread
from datetime import date, datetime
from calendar import day_name, month_abbr

def timestamp(label=None):
    '''this function updates the date timestamp by running an infinite loop in a seperate thread'''

    def text():
        tz = datetime.now().astimezone().tzinfo
        date_time = datetime.now(tz)
        today = date.today()
        i = date.weekday(today)
        month = month_abbr[today.month]
        return day_name[i] + ', ' + month + ' ' + str(today.day) + ' ' + str(today.year) + ' ' + date_time.strftime('%H:%M')

    def loop():
      try:
        while label:
            label.configure(text=text())
      except:
        return

    thread = Thread(target=loop)
    thread.start()
    return text()


class Log:
    def __init__(self):
        self.file = open('log.txt', mode='a')

    def write(self, bytes):
        bytes += ' '+timestamp()+'\n'
        self.file.write(bytes)

    def close(self):
        self.file.flush()


