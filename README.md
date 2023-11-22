# Local Time & Weather Info

#### Video Demo: <https://youtu.be/Jy5RzHOr8F4>
#### Description: 
This project provides the user with the local time and weather at any given location. The program supports roughly 400 locations, and will provide the user with all supported locations in a "Region/City" format, except for some American locations that support "Region/State|Country/City".
Complex weather information can be specified and can be updated should an API subscription with more access is used.

The project uses Openweather API in combination with the pytz and datetime modules to provide users with accurate data updated every second. The base API is free to use up to 1,000 uses a day, and takes ONLY the city as an argument to determine what the API should output to my program, whereas pytz and datetime take both continent & city as arguments to determine the validity and time info of an input.


# Openweather API Key
Built into the project is the functionality for the user to get their own **API key** from Openweather and assert it into the **.env** file. Running the **project** file will create and read an environment variable for the current user. I will not include my api key in **.env** in the final upload.

Other requirements can be installed by creating a virtual environment and runnning requirements.txt

## Future versions
This program took a few of research and programming to create, and in the future I would love to create a user interface for this program and add more functionality such as detailed weather comparisons or time differences. I definitely could use different folders and files for the main instance of project, however for this project I decided to keep everything within one project file to prevent mistakes.

## Version 1.1
- Improved general user experience.
- Improved code efficiency in get_location(), get_temp()
- Added support for numbers instead of typing location
- Improved information given by error messages
