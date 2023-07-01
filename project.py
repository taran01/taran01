import requests
import re
from datetime import datetime, timedelta
from tabulate import tabulate

api_key = "c41ec3d0141f217aa2d716797618e6a1"


def main():
    print()
    print("A simple command-line weather program")
    print("Usage: Unit = C/F and City = any valid city name")
    print("Press ctrl + D to end city promt")
    print()

    while True:
        try:
            unit = get_unit(input("Unit: ").strip().lower())
            break
        except (ValueError, EOFError):
            pass

    cities = []
    while True:
        try:
            cities.append(get_city(input("City: ").strip().lower()))
        except ValueError:
            pass
        except EOFError:
            print()
            print()
            break

    for city in cities:
        url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units={}".format(
            city, api_key, unit
        )
        response = requests.get(url)
        data = response.json()

        check_response = check_error(data)
        if check_response == "pass":
            print(
                tabulate(
                    get_table(data, unit),
                    tablefmt="rounded_grid",
                    headers=[city.upper(), data["sys"]["country"]],
                    colalign=["left", "center"],
                )
            )
            print()
        else:
            print(check_response)
            print()


def get_city(s):
    if not s:
        print("Please provide a city name")
        raise ValueError
    if re.search(r"^[a-z]+( )?[a-z]*( )?[a-z]*$", s):
        return s
    else:
        print("Invalid city name")
        raise ValueError


def get_unit(u):
    if not u:
        print("Please provide unit keyword: C for (Celcius) or F for (Fahren    heit)")
        raise ValueError
    if u not in ["c", "f"]:
        print("Please provide unit keyword: C for (Celcius) or F for (Fahrenheit)")
        raise ValueError
    if u == "c":
        return "metric"
    if u == "f":
        return "imperial"


def check_error(data):
    if data["cod"] == 200:
        return "pass"
    elif data["cod"] == "401":
        return data["message"]
    elif data["cod"] == "404":
        return data["message"]


def convert_unix(unix, tz_offset):
    utc_time = datetime.utcfromtimestamp(unix)
    offset = timedelta(seconds=tz_offset)
    local_time = utc_time + offset
    return local_time


def get_table(data, unit):
    if unit == "metric":
        table = [
            ["⛅ Weather", f"{data['weather'][0]['description']}".title()],
            ["🌡️ Temperature", f"{data['main']['temp']}°C"],
            ["❄️  Feels Like", f"{data['main']['feels_like']}°C"],
            ["💧 Humidity", f"{data['main']['humidity']}%"],
            ["💨 Wind Speed", f"{data['wind']['speed']} m/s"],
            ["🧭 Wind Direction", f"{data['wind']['deg']} deg"],
            [
                "🌅 Sunrise",
                convert_unix(data["sys"]["sunrise"], data["timezone"]).strftime(
                    "%I:%M: %p"
                ),
            ],
            [
                "🌙 Sunset:",
                convert_unix(data["sys"]["sunset"], data["timezone"]).strftime(
                    "%I:%M: %p"
                ),
            ],
        ]
        return table
    else:
        table = [
            ["⛅ Weather", f"{data['weather'][0]['description']}".title()],
            ["🌡️ Temperature", f"{data['main']['temp']}°F"],
            ["❄️  Feels Like", f"{data['main']['feels_like']}°F"],
            ["💧 Humidity", f"{data['main']['humidity']}%"],
            ["💨 Wind Speed", f"{data['wind']['speed']} miles/h"],
            ["🧭 Wind Direction", f"{data['wind']['deg']} deg"],
            [
                "🌅 Sunrise",
                convert_unix(data["sys"]["sunrise"], data["timezone"]).strftime(
                    "%I:%M: %p"
                ),
            ],
            [
                "🌙 Sunset:",
                convert_unix(data["sys"]["sunset"], data["timezone"]).strftime(
                    "%I:%M: %p"
                ),
            ],
        ]
        return table


if __name__ == "__main__":
    main()
