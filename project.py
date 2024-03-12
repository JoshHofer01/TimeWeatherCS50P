import pytz
from datetime import datetime
import requests
import os
import sys
from dotenv import load_dotenv


def main():
    print("""Time & Weather information.
CS50P Final Project by Josh Hofer - England""")
    #user commands variable must be in main otherwise interfers with pytest.
    #assigns variables to methods in class
    timestyle, temptype, details = get_user_commands()
    city, city2, continent = get_location()
    if not city2:
        location = "/".join([continent, city])
    else:
        location = "/".join([continent, city, city2])

    try:
        openweather_raw = get_openweather_info(city)
    except:
        sys.exit("ERROR: Missing or Invalid API Key, please revisit environment variable to check API Key.")

    if city2 != None:
            city = city2
    if details:
        print(f"You chose {continent}, {city.replace('_', ' ')}!")
        print(f"The time in {city.replace('_', ' ')} is {get_time(location, timestyle)}")
        try:
            print(f"The temperature is currently {get_temp(openweather_raw, temptype)}, with {openweather_raw['weather'][0]['description']}.")
            print(f"Wind speed is {get_weather(openweather_raw)[1]}m/ph, with a humidity of {get_weather(openweather_raw)[0]}%.")
            print(f"Finally, it feels like {feelslike_statement(openweather_raw, temptype)}")
        except:
            print(f"Unfortunately, the weather for '{city.replace('_', ' ')}' is not supported in this version...")
    else:
        print(f"You chose {continent}, {city.replace('_', ' ')}!")
        print(f"The local time in {city.replace('_', ' ')} is {get_time(location, timestyle)}")
        try:
            print(f"The current weather there is: {openweather_raw['weather'][0]['description'].capitalize()}")
        except:
            print(f"Unfortunately, the weather for '{city.replace('_', ' ')}' is not supported in this version...")


def get_weather(openweather_raw):
    humidity = openweather_raw['main']['humidity']
    wind_speed = openweather_raw['wind']['speed']
    return humidity, wind_speed


def get_temp(openweather_raw, temptype):
    temp_kelvin = openweather_raw['main']['temp']
    if temptype == 'C':
        temp_celsius = temp_kelvin - 273.15
        return f"{temp_celsius:.2f}°C"
    elif temptype == 'F':
        temp_fahrenheit = 1.8 * (temp_kelvin - 273) + 32
        return f"{temp_fahrenheit:.2f}°F"


def feelslike_statement(openweather_raw, temptype):
    temp_kelvin = openweather_raw['main']['feels_like']
    if temptype == 'C':
        temp = temp_kelvin - 273.15
        temp = f"{temp:.2f}°C"
    elif temptype == 'F':
        temp = 1.8 * (temp_kelvin - 273) + 32
        temp = f"{temp:.2f}°F"

    # Returns custom message based on kelvin provided by API, and includes temp in return message based on chosen tempstyle
    if temp_kelvin >= 303.15:
        return f"{temp}, drink some water! It's a hot day"
    elif temp_kelvin >= 293.15 and temp_kelvin < 303.15:
        return f"{temp}, it's a great day to get outside!"
    elif temp_kelvin > 283.15 and temp_kelvin < 293.15:
        return f"{temp}. Yeh you might want a hoodie, its not warm."
    elif temp_kelvin <= 283.15:
        return f"{temp}, bring a jacket... It's a cold day"


def get_time(location, timestyle):
    try:
        timezone = pytz.timezone(location)
        time_at_city = datetime.now(timezone)
        if timestyle == '12':
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


def get_user_commands():
    """Gets general information from user and returns 3 variables for use in programm """
    while True:
        timestyle = input("'24' or '12' hour time format: ").strip()
        if timestyle == '24' or timestyle == '12':
            break
        else:
            print("Invalid input, please enter '24' or '12'.")

    while True:
        details = input("Would you like detailed weather info: (Y/N) ").strip().upper()
        if details == 'N':
            details = False
            temptype = None
            return timestyle, temptype, details

        #Getting details
        elif details == 'Y':
            details = True
            #Get temptype
            while True:
                temptype = input("Celsius(C) or Fahrenheit(F) temperature format: ").strip().upper()
                if temptype in ["C", "F"]:
                    return timestyle, temptype, details
                else:
                    print("Invalid input, please enter 'C' or 'F'.")


def get_location():
    """First part of function populates the cities list with location info pytz
    timezone module."""
    LOCATIONS = pytz.common_timezones # Gathers list in format xx/xx/xx from pytz module
    continent_options = ['Africa','America','Asia','Antarctica','Australia','Europe']
    cities = []
    cities2 = []

    print("Type the number corresponding with your choice: ")
    for index, continent in enumerate(continent_options, start=1):
        print(f"{index}. {continent}")

    while True:
        try:
            continent_number = int(input("Continent: "))
            if continent_number >= 1 and continent_number <= len(continent_options):
                break
            else:
                print(f"Invalid input, please enter a number between 1-{len(continent_options)}.")
        except ValueError:
            print(f"Please enter valid integer")
    continent_choice = continent_options[continent_number - 1] # Converts user choice to continent
    
    # Adds all supported cities in chosen continent to list
    for location in LOCATIONS:
        if '/' in location and location.startswith(continent_choice):
            continent, city = location.split('/', 1)
            if '/' in city:
                if city.split('/')[0]not in cities:
                    cities.append(city.split('/')[0])
            else:
                if city not in cities:
                    cities.append(city)

    # Prints all supported cities
    print(f"Cities in {continent_choice}, select a number corresponding with your choice:")
    for index, city in enumerate(cities, start=1):
        print(f"{index}. {city}")

    while True:
        try:
            city_number = int(input("City: "))
            if city_number > 0 and city_number <= len(cities):
                break
            else:
                print(f"Invalid input, please enter a number between 1-{len(cities)}.")
        except:
            print(f"Please enter valid integer")
    city = cities[city_number - 1]

    # asks user for second city if the first city they entered are in below list
    # pytz module has different settings for these below places
    if city in ['Argentina', 'North_Dakota', 'Kentucky', 'Indiana']:
        for location in LOCATIONS:
            if location.startswith(f"{continent_choice}/{city}") and location not in cities2:
                cities2.append(location.split('/')[2])
        for index, city in (enumerate(cities2, start=1)):
            print(f"{index}. {city}")

        # returns inputs to class methods
        while True:
            try:
                city2_number = int(input("City: "))
                if city2_number > 0 and city2_number <= len(cities2):
                    break
                else:
                    print(f"Invalid input, please enter a number between 1-{len(cities2)}.")
            except:
                print(f"Please enter valid integer")
        city2 = cities2[city2_number - 1]
        return city, city2, continent_choice
    
    # If city does need extra information
    city2 = False # assert city2 to exist with no value
    return city, city2, continent_choice

if __name__ == "__main__":
    main()