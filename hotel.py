from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Image:
    link: Optional[str] = None
    description: Optional[str] = None

@dataclass
class Images:
    rooms: List[Image] = field(default_factory=list)
    site: List[Image] = field(default_factory=list)
    amenities: List[Image] = field(default_factory=list)

@dataclass
class Location:
    lat: Optional[float] = None
    lng: Optional[float] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None

@dataclass
class Amenities:
    general: List[str] = field(default_factory=list)
    room: List[str] = field(default_factory=list)

@dataclass
class Hotel:
    id: str = ''
    destination_id: int = 0
    name: Optional[str] = None
    location: Location = field(default_factory=Location)
    description: Optional[str] = None
    amenities: Amenities = field(default_factory=Amenities)
    images: Images = field(default_factory=Images)
    booking_conditions: List[str] = field(default_factory=list)