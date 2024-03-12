from project import get_temp, feelslike_statement, get_time
from freezegun import freeze_time

def main():
    test_get_weather()
    test_get_temp_c()
    test_get_temp_f()
    test_feelslike_statement_c()
    test_feelslike_statement_f()
    test_get_time_error()
    test_get_time()

def test_get_weather():
    openweather_raw = {'main':{'humidity':75}, 'wind':{'speed':3.6}}
    humidity = (openweather_raw['main']['humidity'])
    wind_speed = (openweather_raw['wind']['speed'])
    assert humidity == 75
    assert wind_speed == 3.6

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

@freeze_time("2023-01-01")
def test_get_time():
    assert get_time('Africa/Windhoek', 24) == '02:00:00'
