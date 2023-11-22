# Local Time & Weather Info

#### Video Demo: <https://youtu.be/Jy5RzHOr8F4>

#### Features:
- Select between 24-hour and 12-hour time formats.
- Choose between Celsius (C) and Fahrenheit (F) temperature units.
- Option to display detailed weather information including temperature, weather description, wind speed, humidity, and a "feels like" statement.
- Support for multiple cities and continents.
- Automatic detection of user's local time based on the selected city.
- Fetches real-time weather data using the OpenWeatherMap API.

#### Description: 
The program supports roughly 400 locations, and will provide the user with all supported locations in a "Region/City" format, except for some American locations that support "Region/State|Country/City". Follow the on-screen prompts to select your preferences for time format, temperature units, and whether to display detailed weather information. You will then be prompted to choose a continent and city. The program will provide you with the current time and weather information based on your selections.
Complex weather information can be specified and can be updated should an API subscription with more access gets used.


# Openweather API Key
Built into the project is the functionality for the user to get their own **API key** from Openweather and assert it into a **.env** file (this must be created and the OpenWeatherMap API Key added like 'Openweather_API_KEY='your_key') Running the **project** file will create and read an environment variable for the current user. I will not include my api key in **.env** in the final upload.
The project uses Openweather API in combination with the pytz and datetime modules to provide users with accurate data updated every second. The base API is free to use up to 1,000 uses a day, and takes ONLY the city as an argument to determine what the API should output to my program, whereas pytz and datetime take both continent & city as arguments to determine the validity and time info of an input.

Other requirements can be installed by creating a virtual environment and runnning requirements.txt

## Future versions
This program took a few days of research and programming to create, and in the future I would love to create a user interface for this program and add more functionality such as detailed weather comparisons or time differences. I definitely could use different folders and files for the main instance of project, however for this project I decided to keep everything within one project file to prevent mistakes.

## Version 1.1
- Improved general user experience.
- Improved code efficiency in get_location(), get_temp()
- Added support for numbers instead of typing location
- Improved information given by error messages
