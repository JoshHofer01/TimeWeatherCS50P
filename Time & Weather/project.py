import pytz
from datetime import datetime
import requests
import os
from dotenv import load_dotenv
from colorama import Fore, Style

class User_commands():
    def __init__(self, timestyle=None, temptype=None, details=False):
        self.timestyle = timestyle
        self.temptype = temptype
        self.details = details
        self.locations = pytz.common_timezones
        self.city = None
        self.city2 = None
        self.continent = None
        self.get_user_commands()


    def get_user_commands(self):
        while True:
            timestyle = input("'24' or '12' hour time format: ").strip()
            if timestyle == '24' or timestyle == '12':
                self.timestyle = timestyle
                break
            else:
                print("Invalid input, please enter '24' or '12'.")
        
        while True:
            details = input("Would you like detailed weather info: (Y/N) ").strip().upper()
            if details == 'N':
                return
            #Getting details
            elif details == 'Y':
                #Get temptype
                while True:
                    temptype = input("Celsius(C) or Fahrenheit(F) temperature format: ").strip().upper()
                    if temptype == 'C' or temptype == 'F':
                        self.temptype = temptype
                        self.details = True
                        break
                    else:
                        print("Invalid input, please enter 'C' or 'F'.")
                break


    def get_location(self):
        continent_options = ['Africa','America','Asia','Antarctica','Australia','Europe']
        cities = []
        cities2 = []
        
        print("Type the number corresponding with your choice: ")
        for index, continent in enumerate(continent_options, start=1):
            print(f"{index}. {continent}")

        while True:
            continent_choice = input("Continent: ")
            try:
                continent_choice = continent_options[int(continent_choice) - 1]
            except:
                print(f"Invalid input, please enter a number between 1-{len(continent_options)}.")
            if continent_choice in continent_options:
                # Adds all supported cities in chosen continent to list
                for location in self.locations:
                    if '/' in location and location.startswith(continent_choice):
                        continent, city = location.split('/', 1)
                        if '/' not in city:
                            if city not in cities:
                                cities.append(city)
                        elif '/' in city:
                            if city.split('/')[0]not in cities:
                                cities.append(city.split('/')[0])
                break

        # Prints all supported cities
        print(f"Cities in {continent_choice}, select a number corresponding with your choice:")
        for index, city in enumerate(cities, start=1):
            print(f"{index}. {city}")

        while True:             
            city = input("City: ")
            try:
                city = cities[int(city) - 1]
                break
            except:
                print(f"Invalid input, please enter a number between 1-{len(cities)}.")

        self.city = city
        self.continent = continent_choice
        if city in ['Argentina', 'North_Dakota', 'Kentucky', 'Indiana']:
            for location in self.locations:
                if location.startswith(f"{continent_choice}/{city}") and location not in cities2:
                    cities2.append(location.split('/')[2])
            for index, city in (enumerate(cities2, start=1)):
                print(f"{index}. {city}")
                
            # returns inputs to class methods
            while True:
                city2 = input("City: ")
                try:
                    city2 = cities2[int(city2) - 1]
                    break
                except:
                    print(f"Invalid input, please enter a number between 1-{len(cities2)}.")
            self.city2 = city2
            self.continent = continent_choice


            
print(Fore.GREEN + """Time & Weather information. 
CS50P Project by Josh Hofer - England""", Style.RESET_ALL)
user_commands = User_commands()

def main():
    location = user_commands.get_location()
    continent = user_commands.continent
    city = user_commands.city
    city2 = user_commands.city2
    if city2 == None:
        location = f"{continent}/{city}"
    else:
        location = f"{continent}/{city}/{city2}"

    openweather_raw = get_openweather_info(city)
    if city2 != None:
            city = city2
    if user_commands.details == True:
        print(f"You chose {continent}, {city.replace('_', ' ')}!")
        print(f"The time in {city.replace('_', ' ')} is {get_time(location)}")
        try:
            print(f"The temperature is currently {get_temp(openweather_raw)}, with {openweather_raw['weather'][0]['description']}.")
            print(f"Wind speed is {get_weather(openweather_raw)[1]}m/ph, with a humidity of {get_weather(openweather_raw)[0]}%.")
            print(f"Finally, it feels like {feelslike_statement(openweather_raw)}")
        except:
            print(f"Unfortunately, the weather for '{city.replace('_', ' ')}' is not supported in this version...")
    else:
        print(f"You chose {continent}, {city.replace('_', ' ')}!")
        print(f"The local time in {city.replace('_', ' ')} is {get_time(location)}")
        try:
            print(f"The current weather there is: {openweather_raw['weather'][0]['description'].capitalize()}")
        except:
            print(f"Unfortunately, the weather for '{city.replace('_', ' ')}' is not supported in this version...")


def get_weather(openweather_raw):
    humidity = (openweather_raw['main']['humidity'])
    wind_speed = (openweather_raw['wind']['speed'])
    return humidity, wind_speed,

def get_temp(openweather_raw):
    temp_kelvin = openweather_raw['main']['temp']
    if user_commands.temptype == 'C':
        temp_celsius = temp_kelvin - 273.15
        return f"{temp_celsius:.2f}°C"
    elif user_commands.temptype == 'F':
        temp_fahrenheit = 1.8 * (temp_kelvin - 273) + 32
        return f"{temp_fahrenheit:.2f}°F"
    
def feelslike_statement(openweather_raw):
    temp_kelvin = openweather_raw['main']['feels_like']
    if user_commands.temptype == 'C':
        temp = temp_kelvin - 273.15
        temp = f"{temp:.2f}°C"
    elif user_commands.temptype == 'F':
        temp = 1.8 * (temp_kelvin - 273) + 32
        temp = f"{temp:.2f}°F"

    if temp_kelvin >= 303.15:
        return f"{temp}, drink some water! It's a hot day"
    elif temp_kelvin >= 293.15 and temp_kelvin < 303.15:
        return f"{temp}, it's a great day to get outside!"
    elif temp_kelvin > 283.15 and temp_kelvin < 293.15:
        return f"{temp}. Yeh you might want a hoodie, its not warm."
    elif temp_kelvin <= 283.15:
        return f"{temp}, bring a jacket... It's a cold day"


def get_time(location):
    try:
        timezone = pytz.timezone(location)
        time_at_city = datetime.now(timezone)
        if user_commands.timestyle == '12':
            formatted_time = time_at_city.strftime('%I:%M:%S %p')
        else:
            formatted_time = time_at_city.strftime('%H:%M:%S')
        return formatted_time
    except pytz.UnknownTimeZoneError:
        return "This city is not supported in this version of the Timezone Converter"


def get_openweather_info(city):
    load_dotenv()
    api_key = os.getenv("Openweather_API_KEY")
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    url = base_url + "appid=" + api_key + "&q=" + city
    url = f"{base_url}appid={api_key}&q={city}"
    response = requests.get(url).json()
    return response


if __name__ == "__main__":
    main()