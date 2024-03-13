from project import get_temp, feelslike_statement, get_time, get_weather
from freezegun import freeze_time

# Run tests using 'pytest unit_tests.py' on terminal
"""'get_location() and get_user_commands()' not included due to 
functions requiring some form of input. Unable to do reliably
using pytest."""

def main():
    test_get_weather_no_func() # Tests if code logic is sound
    test_get_weather_func() # Tests actual function with similar raw data to actual programm
    test_get_temp_c()
    test_get_temp_f()
    test_feelslike_statement_c()
    test_feelslike_statement_f()
    test_get_time_error()
    test_get_time_24()
    test_get_time_12()


def test_get_weather_no_func():
    openweather_raw = {'main':{'humidity':75}, 'wind':{'speed':3.6}}
    humidity = (openweather_raw['main']['humidity'])
    wind_speed = (openweather_raw['wind']['speed'])
    assert humidity == 75
    assert wind_speed == 3.6


def test_get_weather_func():
    openweather_raw = {"coord":{"lon":10.99,"lat":44.34},"weather":[{"id":501,"main":"Rain","description":"moderate rain","icon":"10d"}],"base":"stations","main":{"temp":298.48,"feels_like":298.74,"temp_min":297.56,"temp_max":300.05,"pressure":1015,"humidity":64,"sea_level":1015,"grnd_level":933},"visibility":10000,"wind":{"speed":0.62,"deg":349,"gust":1.18},"rain":{"1h":3.16},"clouds":{"all":100},"dt":1661870592,"sys":{"type":2,"id":2075663,"country":"IT","sunrise":1661834187,"sunset":1661882248},"timezone":7200,"id":3163858,"name":"Zocca","cod":200}
    assert get_weather(openweather_raw) == (64, 0.62)


def test_get_temp_c():
    openweather_raw = {"main":{'temp':300}}
    assert get_temp(openweather_raw, 'C') == "26.85°C"


def test_get_temp_f():
    openweather_raw = {"main":{'temp':300}}
    assert get_temp(openweather_raw, 'F') == "80.60°F"

def test_feelslike_statement_c():
    openweather_raw = {"main":{'feels_like':305}}
    assert feelslike_statement(openweather_raw, 'C') == "31.85°C, drink some water! It's a hot day"


def test_feelslike_statement_f():
    openweather_raw = {"main":{'feels_like':280}}
    assert feelslike_statement(openweather_raw, 'F') == "44.60°F, bring a jacket... It's a cold day"


def test_get_time_error():
    assert get_time('Fake/City', 24) == "This city is not supported in this version of the Timezone Converter"


@freeze_time("2024-01-01")
def test_get_time_24():
    assert get_time('Africa/Windhoek', 24) == '02:00:00'


@freeze_time("2024-01-01")
def test_get_time_12():
    assert get_time('America/Argentina/Buenos_Aires', 12) == '21:00:00'
