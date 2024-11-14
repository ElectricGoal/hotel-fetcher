from helpers import (
    AggHelpers as ah,
    FormatHelpers as fh
)

import pandas as pd
from dataclasses import asdict, is_dataclass

class HotelsService:
    """Service class to fetch and filter hotels data."""
    def __init__(self):
        self.data = pd.DataFrame(
            columns=[
                'id', 
                'destination_id', 
                'name', 
                'location.lat', 
                'location.lng', 
                'location.address', 
                'location.city', 
                'location.country', 
                'description', 
                'amenities.general', 
                'amenities.room', 
                'images.rooms', 
                'images.site', 
                'images.amenities', 
                'booking_conditions'
            ]
        )

    def merge_and_save(self, suppliers_data):
        """Merge the data from suppliers and save it in memory""" 

        # Normalize the data from suppliers and convert it to a pandas dataframe
        suppliers_df = pd.json_normalize(
            asdict(d) for d in suppliers_data if is_dataclass(d)
        )

        # Merge data
        self.data = suppliers_df.groupby('id').agg({
            'destination_id': 'first',
            'name': ah.longest_valid_text, 
            'location.lat': ah.first_valid_num,
            'location.lng': ah.first_valid_num,
            'location.address': ah.longest_valid_text,
            'location.city': ah.longest_valid_text,
            'location.country': ah.longest_valid_text,
            'description': ah.longest_valid_text,
            'amenities.general': ah.last_valid_list,
            'amenities.room': ah.last_valid_list,
            'images.rooms': ah.merge_lists,
            'images.site': ah.merge_lists,
            'images.amenities': ah.merge_lists,
            'booking_conditions': ah.longest_valid_text
        }).reset_index()


    def find(self, hotel_ids, destination_ids):
        """Filter the data based on hotel_ids and destination_ids"""

        if hotel_ids and destination_ids:
            self.data = self.data[self.data['id'].isin(hotel_ids) & self.data['destination_id'].isin(destination_ids)]
        elif hotel_ids:
            self.data = self.data[self.data['id'].isin(hotel_ids)]
        elif destination_ids:
            self.data = self.data[self.data['destination_id'].isin(destination_ids)]

        
        # convert the data to a dictionary
        return fh.df_to_formatted_json(self.data)
    


