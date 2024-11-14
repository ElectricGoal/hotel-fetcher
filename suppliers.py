from hotel import Hotel, Images, Image, Location, Amenities

import requests
from typing import List, Any, Union

def parse_data(dto: dict, keys: Union[List[str], str]) -> Any:
    """
    Safely retrieves data from a nested dictionary based on a key or a list of keys.
    Strips strings or elements of a list if applicable.

    :param dto: The dictionary to parse.
    :param keys: A single key as a string or a list of keys for nested access.
    :return: The stripped value corresponding to the key(s) or None if any key is missing.
    """
    if isinstance(keys, str):
        # Handle single key case
        data = dto.get(keys, None)
    else:
        # Handle list of keys for nested access
        current_data = dto
        for key in keys:
            if not isinstance(current_data, dict) or key not in current_data:
                return None
            current_data = current_data[key]
        data = current_data

    # Strip data if it's a string or list of strings
    if isinstance(data, str):
        return data.strip()
    elif isinstance(data, list):
        return [item.strip() if isinstance(item, str) else item for item in data]
    return data

class BaseSupplier:
    """Base class for supplier data"""
    def __init__(self, api_url: str):
        self.api_url = api_url

    def parse(obj: dict) -> Hotel:
        """Parse supplier-provided data into Hotel object"""

    def fetch(self):
        resp = requests.get(self.api_url)
        return [self.parse(dto) for dto in resp.json()]

class AcmeSupplier(BaseSupplier):
    """Supplier class for Acme data"""
    
    @staticmethod
    def parse(dto: dict) -> Hotel:
        return Hotel(
            id=parse_data(dto, "Id"),
            destination_id=parse_data(dto, "DestinationId"),
            name=parse_data(dto, "Name"),
            location=Location(
                lat=parse_data(dto, "Latitude"),
                lng=parse_data(dto, "Longitude"),
                address=parse_data(dto, "Address") + ', ' + parse_data(dto, "PostalCode"),
                city=parse_data(dto, "City"),
                country=parse_data(dto, "Country"),
            ),
            description=parse_data(dto, "Description"),
            amenities=Amenities(
                general=parse_data(dto, "Facilities"),
            )
        )
    
class PatagoniaSupplier(BaseSupplier):
    """Supplier class for Patagonia data"""
    
    @staticmethod
    def parse(dto: dict) -> Hotel:
        return Hotel(
            id=parse_data(dto, "id"),
            destination_id=parse_data(dto, "destination"),
            name=parse_data(dto, "name"),
            location=Location(
                lat=parse_data(dto, "lat"),
                lng=parse_data(dto, "lng"),
                address=parse_data(dto, "address")
            ),
            description=parse_data(dto, "info"),
            amenities=Amenities(
                general=parse_data(dto, "amenities"),
                room=[]
            ),
            images=Images(
                rooms=[
                    Image(
                        link=parse_data(room, "url"),
                        description=parse_data(room, "description")
                    )
                    for room in parse_data(dto, ["images", "rooms"])
                ],
                amenities=[
                    Image(
                        link=parse_data(amenity, "url"),
                        description=parse_data(amenity, "description")
                    )
                    for amenity in parse_data(dto, ["images", "amenities"])
                ],
            ),
        )
    
class PaperfliesSupplier(BaseSupplier):
    """Supplier class for Paperflies data"""
    
    @staticmethod
    def parse(dto: dict) -> Hotel:
        return Hotel(
            id=parse_data(dto, "hotel_id"),
            destination_id=parse_data(dto, "destination_id"),
            name=parse_data(dto, "hotel_name"),
            location=Location(
                address=parse_data(dto, ["location", "address"]),
                country=parse_data(dto, ["location", "country"]),
            ),
            description=parse_data(dto, "details"),
            amenities=Amenities(
                general=parse_data(dto, ["amenities", "general"]),
                room=parse_data(dto, ["amenities", "room"])
            ),
            images=Images(
                rooms=[
                    Image(
                        link=parse_data(room, "link"),
                        description=parse_data(room, "caption")
                    )
                    for room in parse_data(dto, ["images", "rooms"])
                ],
                site=[
                    Image(
                        link=parse_data(site, "link"),
                        description=parse_data(site, "caption")
                    )
                    for site in parse_data(dto, ["images", "site"])
                ],
            ),
            booking_conditions=parse_data(dto, "booking_conditions"),
        )