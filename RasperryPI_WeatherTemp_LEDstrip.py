import requests
import json
import pigpio
from datetime import datetime, time

class TempColor:
    def __init__(self):
        self.pi = pigpio.pi()
        self.Rpin = 17
        self.Gpin = 22
        self.Bpin = 24
        self.bright_multiplier = 1
        self.url = "http://api.openweathermap.org/data/2.5/weather"
        self.key = "OpenWeatherMap_APIkey"
        self.city = "Denver"
        self.pinkish = ["pinkish",(20,0,20)]
        self.purple = ["purple",(10,0,30)]
        self.dkblue = ["dkblue",(5,0,35)]
        self.mdblue = ["mdblue",(0,0,30)]
        self.ltblue = ["ltblue",(0,10,20)]
        self.teal = ["teal",(0,25,15)]
        self.greenish = ["greenish",(0,30,10)]
        self.green = ["green",(0,30,0)]
        self.ltgreen = ["ltgreen",(15,20,0)]
        self.yellow = ["yellow",(20,10,0)]
        self.orange = ["orange",(30,10,0)]
        self.red = ["red",(30,0,0)]

    def setColor(self):
        red_scaled = self.color[1][0] * self.bright_multiplier
        green_scaled = self.color[1][1] * self.bright_multiplier
        blue_scaled = self.color[1][2] * self.bright_multiplier

        self.pi.set_PWM_dutycycle(self.Rpin,red_scaled)
        self.pi.set_PWM_dutycycle(self.Gpin,green_scaled)
        self.pi.set_PWM_dutycycle(self.Bpin,blue_scaled)
        print(self.color)
        print(self.bright_multiplier)
        self.pi.stop()

    def getWeatherData(self):
        try:
            self.response = requests.get(url=self.url, params=dict(q=self.city, APPID=self.key)).json()
        except:
            self.response = "ERROR"
        return self.response

    def getFTemp(self):
        if self.response != "ERROR":
            self.currentTemp = ((((self.response["main"]["temp"]-273.15)*9)/5)+32)
        #print(self.currentTemp)
        return self.currentTemp

    def assignColor(self):
        if self.currentTemp < 0:
            self.color = self.pinkish
            #print('0')
        elif self.currentTemp < 10:
            self.color = self.purple
            #print('10')
        elif self.currentTemp < 20:
            self.color = self.dkblue
            #print('20')
        elif self.currentTemp < 30:
            self.color = self.mdblue
            #print('30')
        elif self.currentTemp < 40:
            self.color = self.ltblue
            #print('40')
        elif self.currentTemp < 50:
            self.color = self.teal
            #print('50')
        elif self.currentTemp < 60:
            self.color = self.greenish
            #print('60')
        elif self.currentTemp < 70:
            self.color = self.green
            #print('70')
        elif self.currentTemp < 80:
            self.color = self.ltgreen
        elif self.currentTemp < 90:
            self.color = self.yellow
        elif self.currentTemp < 100:
            self.color = self.orange
        else:
            self.color = self.red

    def scaleBrightness(self):
        time_ranges = [
            ("Late Night AM", time(0, 0), time(4, 59)),
            ("Early Morning", time(5, 0), time(7, 59)),
            ("Late Morning", time(8, 0), time(11, 59)),
            ("Afternoon", time(12, 0), time(16, 59)),
            ("Evening", time(17, 0), time(20, 59)),
            ("Night", time(21, 0), time(21, 59)),
            ("Late Night PM", time(22, 0), time(23, 59)),
        ]
        current_time = datetime.now().time()
        for name, start, end in time_ranges:
            if start <= current_time <= end:
                current_name = name
        print(current_name)

        # scale brightness based on current time name
        if current_name in ("Late Night AM", "Late Night PM"):
            self.bright_multiplier = 0
        elif current_name in ("Early Morning", "Night"):
            self.bright_multiplier = 1
        elif current_name in ("Late Morning", "Evening"):
            self.bright_multiplier = 2
        elif current_name in ("Afternoon"):
            self.bright_multiplier = 3


# # #   MAIN   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
tc = TempColor()
tc.getWeatherData()
tc.getFTemp()
tc.assignColor()
tc.scaleBrightness()
tc.setColor()
