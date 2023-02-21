'''@author Carl Archemetre'''

from tkinter import *
from datetime import date, datetime
from calendar import day_name, month_abbr
import requests
from PIL import Image, ImageTk
import shutil
import os
from threading import Thread, Timer
from tkinter.messagebox import Message

DIRECTORY = 'icon' # name for icon directory
NIGHT = 'black' # image background color
DAY = '#91E0FF' # image background color
COLOR = {'n': NIGHT, 'd': DAY}
FONT = {'n': 'white', 'd': 'black'}


def set_interval(func, delay):
    def func_wrapper():
        set_interval(func, delay)
        func()

    thread = Timer(delay, func_wrapper)
    thread.daemon = True
    thread.start()
    return thread


class Weather:
    def __init__(self, city):
        self.city = city
        self.response = self.request(city)
        if isinstance(self.response, str):
            raise Exception(self.response)

    @property
    def time_of_day(self):
        '''returns n for night or d for day'''
        return self.response['weather'][0]['icon'][-1]

    def request(self, city):
        '''Interface for API provided by OpenWeatherMap'''
        key = 'a6b81c41a5f9a4218c0e5e1179786e81'
        url = 'http://api.openweathermap.org/data/2.5/weather?' + 'appid=' + key + '&q=' + city
        response = requests.get(url)
        response = response.json()
        if response['cod'] == 200:
            return response
        else:
            return response['cod']

    def update(self):
        '''gets the latest weather data'''
        self.response = self.request(self.city)

    @property
    def image(self):
        '''this property returns the path to the weather icon or it downloads an icon into the icon directory
        if it doesn't exist'''
        icon = self.response['weather'][0]['icon']
        image_url = 'https://openweathermap.org/img/wn/'+icon+'@4x.png'#url for icon hosted on the API server
        file = image_url.split('/')[-1]
        path = os.path.join(DIRECTORY, file)
        if file in os.listdir(DIRECTORY):
            return path
        else:
            response = requests.get(image_url, stream=True)
            response.raw.decode_content = True
            with open(path, 'wb') as file:
                shutil.copyfileobj(response.raw, file)#copies raw data into file
            return path

    @property
    def weather(self):
        '''returns a description of the weather'''
        return self.response['weather'][0]['main']

    @property
    def description(self):
        '''returns a detail description of the weather'''
        return self.response['weather'][0]['description']

    @property # not currently in use
    def timezone(self):
        return self.response['timezone']

    def temperature(self, scale='celsius'):
        '''return temperature, default is celsius'''
        kelvin = self.response['main']['temp']
        celsius = kelvin-273.15
        fahrenheit = celsius * (9/5) + 32
        return '%.0f%s' % (celsius, chr(176)) if scale == 'celsius' else '%.0f%s' % (fahrenheit, chr(176))


class App:
    def __init__(self, city='Port-au-Prince'):
        self.configure()
        self.weather = Weather(city)

        self.app = Tk()
        self.app.title('Wheatherly')
        self.app.geometry('250x250')
        self.app.resizable(False, False)
        self.app.columnconfigure(0, weight=1)
        self.app.columnconfigure(1, weight=1)

        self.search = Entry(self.app, width=15, textvariable=StringVar())
        self.search.grid(row=0, column=0, columnspan=2, sticky='', pady=10)
        self.search.insert(0, city)

        # lambda is handler for search box, to have Weather object point to a different city
        self.search.bind('<Return>', lambda event: self.update(city=event.widget.get()))

        self.temp = Label(self.app, height=-80, width=-80)
        self.temp.config(font=('Valera bold', -69))
        self.temp.grid(row=1, column=1, sticky='w')

        timestamp = Label(self.app)
        timestamp.config(text=self.timestamp(timestamp))
        timestamp.place(relx=1.0, rely=1.0, anchor='se')

        self.description = Label(self.app)
        self.description.grid(row=2, column=0, sticky='e')

        def click(btn):
            '''handler for button to change scale when clicked'''
            if btn.cget('text') == 'celsius':
                self.temp.configure(text=self.weather.temperature(scale='fahrenheit'))
                btn.config(text='fahrenheit')
            else:
                self.temp.configure(text=self.weather.temperature(scale='celsius'))
                btn.config(text='celsius')

        self.button = Button(self.app, text='celsius', width=10, command=lambda: click(self.button), bg='#DE7956')
        self.button.grid(row=2, column=1, sticky='w')

        self.refresh()

    def configure(self):
        '''creates a directory for the weather icons if one does not exist, should be created when app is first launch'''
        try:
            os.mkdir(DIRECTORY)
        except FileExistsError:
            pass

    def refresh(self):
        '''update weather with the latest data'''
        self.weather.update()

        time_of_day = self.weather.time_of_day
        color = COLOR[time_of_day]
        font = FONT[time_of_day]

        img = ImageTk.PhotoImage(Image.open(self.weather.image).resize((80, 80)))
        image = Label(self.app, image=img, bg=color, height=80, width=80)
        image.img = img
        image.grid(row=1, column=0, sticky='E')

        self.description.configure(text=self.weather.description)

        # sets scale to text on button
        scale = self.button.cget('text')
        self.temp.configure(text=self.weather.temperature(scale=scale))
        self.temp.configure(bg=color, fg=font)

    def update(self, city):
        '''Attempts to get data when city is changed, alerts user is city can't be updated'''
        try:
            self.weather = Weather(city)
            self.refresh()
        except Exception as exception:
            Message(master=self.app, title='Error %s' % exception, message='%s not found' % city).show()
            self.search.delete(0, END)#END is tkinter constant, this statement is change the search back to last request
            self.search.insert(0, self.weather.city)

    def timestamp(self, label):
        '''this method updates the date timestamp by running an infinite loop in a seperate thread'''
        def text():
            tz = datetime.now().astimezone().tzinfo
            date_time = datetime.now(tz)
            today = date.today()
            i = date.weekday(today)
            month = month_abbr[today.month]
            return day_name[i] + ', ' + month + ' ' + str(today.day) + ' ' + str(today.year) + ' ' + date_time.strftime('%H:%M')

        def loop():
            while True:
                label.configure(text=text())

        thread = Thread(target=loop)
        thread.daemon = True
        thread.start()
        return text()

    def run(self):
        '''runs the program, while updating the widgets every 1000 ms'''
        set_interval(self.refresh, 1000)
        self.app.mainloop()

