from threading import Thread
from datetime import date, datetime
from calendar import day_name, month_abbr


def timestamp(label):
    '''this function updates the date timestamp by running an infinite loop in a seperate thread'''

    def text():
        tz = datetime.now().astimezone().tzinfo
        date_time = datetime.now(tz)
        today = date.today()
        i = date.weekday(today)
        month = month_abbr[today.month]
        return day_name[i] + ', ' + month + ' ' + str(today.day) + ' ' + str(today.year) + ' ' + date_time.strftime('%H:%M')



    def loop():
        while thread.alive:
            label.configure(text=text())

    thread = Thread(target=loop)
    thread.daemon = True
    thread.alive = True
    thread.start()
    return thread, text()