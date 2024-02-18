from dataclasses import asdict, fields
from os import environ
from re import search

from ipinfo import getHandler as get_handler
from pandas import DataFrame

from utils import (
    Access,
    City,
    Continent,
    Country,
    Event,
    Position
)
from utils import NGINX_LOG_LINE

if __name__ == "__main__":
    token = environ.get("IPINFO_TOKEN")
    handler = get_handler(
        access_token=token,
        cache_options={"maxsize": 512, "ttl": 120}
    )
    with open("access.txt", "r") as log:
        df = DataFrame(columns=[field.name for field in fields(Event)])
        for line in log:
            groups = search(NGINX_LOG_LINE, line).groups()
            access = Access(groups)
            details = handler.getDetails(access.ip).all
            if "bogon" in details:  # Skip private addresses
                continue
            position = Position(details["loc"])
            continent = Continent(**details["continent"])
            country = Country(details["country_name"], details["country"], continent)
            city = City(details["city"], details["region"], country, position)
            event = Event(access, city)
            df.loc[len(df)] = event.__dict__()
        df.to_csv("access.csv", index=False, header=False)
