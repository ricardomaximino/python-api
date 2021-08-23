import os
import requests
from twilio.rest import Client


open_weather_key = os.getenv("OPEN_WEATHER_KEY")
lat = 38.192360
lon = -0.555180
city_name = "Santa Pola"
state_code = "AL"
country_code = "ES"
twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")

http_proxy = os.getenv("HTTP_PROXY")
https_proxy = os.getenv("HTTPS_PROXY")
proxies = {"http": http_proxy, "https": https_proxy}

parameters = {
    "q": f"{city_name}, {state_code}, {country_code}",
    "appid": open_weather_key
}
url = "https://api.openweathermap.org/data/2.5/weather"

url_one_call = "https://api.openweathermap.org/data/2.5/onecall"
parameters_one_call = {
    "lat": lat,
    "lon": lon,
    "exclude": "current,minutely,daily",
    "appid": open_weather_key
}

response = requests.get(url=url_one_call, params=parameters_one_call, proxies=proxies)
response.raise_for_status()

data = response.json()

print(data)
going_to_rain = False
for hour in data["hourly"][:12]:
    for weather in hour["weather"]:
        if int(weather["id"]) < 700:
            going_to_rain = True
            break
    if going_to_rain:
        break

if going_to_rain:
    client = Client(twilio_account_sid, twilio_auth_token)
    message = client.messages.create(
        body="My own weather alert app It's going to rain today!!",
        from_="+12532012602",
        to="+34634753562"
    )
else:
    print("It's NOT going to rain today!!")
