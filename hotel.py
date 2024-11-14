from dataclasses import dataclass, field
from typing import List

@dataclass
class Image:
    link: str = None
    description: str = None

@dataclass
class Images:
    rooms: List[Image] = field(default_factory=list)
    site: List[Image] = field(default_factory=list)
    amenities: List[Image] = field(default_factory=list)

@dataclass
class Location:
    lat: float = None
    lng: float = None
    address: str = None
    city: str = None
    country: str = None

@dataclass
class Amenities:
    general: List[str] = field(default_factory=list)
    room: List[str] = field(default_factory=list)

@dataclass
class Hotel:
    id: str = None
    destination_id: int = None
    name: str = None
    location: Location = field(default_factory=Location)
    description: str = None
    amenities: Amenities = field(default_factory=Amenities)
    images: Images = field(default_factory=Images)
    booking_conditions: List[str] = field(default_factory=list)