#!/usr/bin/env python
from samplebase import SampleBase
from rgbmatrix import graphics
from datetime import datetime
import openmeteo_requests
import time

from utils import *


class TimeWeather(SampleBase):
    def __init__(self):
        super(TimeWeather, self).__init__()
        self.openmeteo = openmeteo_requests.Client()
    
    def run(self):
        '''Display time and weather on LED screen.'''

        time_text = self.get_formatted_time()
        time_font_path, time_x, time_y = draw_text(time_text, True, TextPlacement.TOP, 1)
        time_font = graphics.Font()
        time_font.LoadFont(time_font_path)

        date_text = self.get_formatted_time()
        date_font_path, date_x, date_y = draw_text(date_text, True, TextPlacement.BOTTOMRIGHT, 1)
        date_font = graphics.Font()
        date_font.LoadFont(date_font_path)

        weather_text = self.get_weather()
        weather_font_path, weather_x, weather_y = draw_text(weather_text, False, TextPlacement.BOTTOMLEFT, 3)
        weather_font = graphics.Font()
        weather_font.LoadFont(weather_font_path)

        canvas = self.matrix.CreateFrameCanvas()

        start = time.time()
        while True:
            if ((time.time() - start) / 60 >= 15):
                try:
                    weather_text = self.get_weather()
                    weather_font_path, weather_x, weather_y = draw_text(weather_text, False, TextPlacement.BOTTOMLEFT)
                    weather_font = graphics.Font()
                    weather_font.LoadFont(weather_font_path)
                except:
                    continue
                start = time.time()

            canvas.Clear()

            time_text = self.get_formatted_time()
            date_text = self.get_formatted_date()

            graphics.DrawText(canvas, time_font, time_x, time_y, graphics.Color(29, 78, 216), time_text)
            graphics.DrawText(canvas, weather_font, weather_x, weather_y, graphics.Color(255, 255, 255), weather_text)
            graphics.DrawText(canvas, date_font, date_x, date_y, graphics.Color(255, 255, 255), date_text)

            canvas = self.matrix.SwapOnVSync(canvas)

            time.sleep(0.2)


    def get_formatted_date(self):
        time_format = "%b %d"
        current_date = datetime.now()
        return current_date.strftime(time_format)

    def get_formatted_time(self):
        '''Get the current time as a string.'''
        time_format = "%I:%M:%S"
        now = datetime.now()
        return now.strftime(time_format)

    def get_weather(self):
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": 40.744678,
            "longitude": -73.758072,
            "current": "temperature_2m",
            "temperature_unit": "fahrenheit",
            "wind_speed_unit": "ms",
            "precipitation_unit": "inch",
            "timezone": "America/New_York",
            "forecast_days": 1
        }
        response = self.openmeteo.weather_api(url, params=params)[0]
        temperature = response.Current().Variables(0).Value()
        return f'{round(temperature)}°'



# Main function
if __name__ == "__main__":
    time_weather = TimeWeather()
    if (not time_weather.process()):
        time_weather.print_help()
