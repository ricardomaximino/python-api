import datetime
import requests
import time
import os

http_proxy = os.getenv("HTTP_PROXY")
https_proxy = os.getenv("HTTPS_PROXY")
proxies = {"http": http_proxy, "https": https_proxy}

while True:
    # print("\nISS API")
    iss_url = "http://api.open-notify.org/iss-now.json"
    response = requests.get(url=iss_url, proxies=proxies)
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # print(f"Latitude:\t{iss_latitude}\nLongitude:\t{iss_longitude}")

    # print("\nKanye Quote API")
    kanye_url = "https://api.kanye.rest"
    response = requests.get(kanye_url)
    response.raise_for_status()
    data = response.json()

    quote = data["quote"]

    # print(f"Quote: {quote}")

    # print("API With Parameters")
    office_latitude = 38.192360
    office_longitude = -0.555180
    sunrise_set_url = "https://api.sunrise-sunset.org/json"
    parameter = {"latitude": office_latitude, "longitude": office_longitude, "formatted": 0}
    response = requests.get(sunrise_set_url, params=parameter, proxies=proxies)
    response.raise_for_status()
    data = response.json()["results"]
    # for key in data:
    #     print(f"{key}:\t{data[key]}")

    # print("\n\nFinal Usage Of The APIs")
    iss_coordinates = {"latitude": iss_latitude, "longitude": iss_longitude}
    coordinates = {"latitude": office_latitude, "longitude": office_longitude}
    sunrise_hour = int(data["sunrise"].split("T")[1].split(":")[0])
    sunset_hour = int(data["sunset"].split("T")[1].split(":")[0])
    now_hour = datetime.datetime.now().hour


    def iss_is_overhead(iss_coord, coord):
        iss_lat = iss_coord["latitude"]
        iss_long = iss_coord["longitude"]

        latitude = coord["latitude"]
        longitude = coord["longitude"]
        if latitude - 5 <= iss_lat <= latitude + 5 and longitude - 5 <= iss_long <= longitude + 5:
            return True
        return False


    def is_night_time(rise_hour, set_hour, hour):
        if hour < rise_hour or hour > set_hour:
            return True
        return False

    overhead = iss_is_overhead(iss_coordinates, coordinates)
    if overhead:
        print(f"""
                Sunrise: {sunrise_hour}
                Sunset: {sunset_hour}
                Now: {now_hour}
                Is night time: {is_night_time(sunrise_hour, sunset_hour, now_hour)}
                Is ISS overhead: {overhead}
                """)
        break

    else:
        print(datetime.datetime.now())
        time.sleep(60)




