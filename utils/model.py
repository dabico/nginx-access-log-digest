from dataclasses import InitVar
from dataclasses import asdict, dataclass, field
from datetime import datetime
from ipaddress import IPv4Address
from typing import Any

from humanfriendly import format_size
from urllib.parse import parse_qs, urlparse
from user_agents import parse as parse_user_agent


@dataclass
class Access:
    data: InitVar[tuple[str | Any, ...]]

    ip: IPv4Address = field(init=False)
    time: datetime = field(init=False)
    query: dict[str, list[str]] = field(init=False)
    status: int = field(init=False)
    size: str = field(init=False)
    referer: str = field(init=False)
    user_agent: Any = field(init=False)

    def __post_init__(self, data):
        length = len(data)
        if length != 7:
            raise ValueError(f"Expected 7 elements, got {length}")
        ip, timestamp, request, status, size, referer, user_agent = data
        self.ip = IPv4Address(ip)
        self.time = datetime.strptime(timestamp, "%d/%b/%Y:%H:%M:%S %z")
        _, request, _ = request.split(" ")
        path = urlparse(request)
        self.query = parse_qs(path.query)
        self.status = int(status)
        self.size = format_size(int(size))
        self.referer = None if referer == "-" else referer
        self.user_agent = parse_user_agent(user_agent)

    def __dict__(self):
        return {
            "ip": self.ip.compressed,
            "time": self.time.isoformat().replace("+00:00", "Z"),
            "query": self.query,
            "status": self.status,
            "size": self.size,
            "referer": self.referer,
            "user_agent": {
                "browser": self.user_agent.get_browser(),
                "os": self.user_agent.get_os(),
                "device": self.user_agent.get_device()
            }
        }


@dataclass
class Position:
    loc: InitVar[str]

    latitude: float = field(init=False)
    longitude: float = field(init=False)

    def __post_init__(self, loc):
        parts = loc.split(",")
        if len(parts) != 2:
            raise ValueError(f"Invalid location format: {loc}")
        self.latitude, self.longitude = map(float, parts)

    def __dict__(self):
        return asdict(self)


@dataclass
class Continent:
    code: str
    name: str

    def __dict__(self):
        return asdict(self)


@dataclass
class Country:
    name: str
    code: str
    continent: Continent

    def __dict__(self):
        return asdict(self)


@dataclass
class City:
    name: str
    region: str
    country: Country
    position: Position

    def __dict__(self):
        return asdict(self)


@dataclass
class Event:
    access: Access
    city: City

    def __dict__(self):
        return {
            "access": self.access.__dict__(),
            "city": self.city.__dict__()
        }
