from helpers import (
    AggHelpers as ah,
    FormatHelpers as fh
)

import pandas as pd
import re
from dataclasses import asdict, is_dataclass

class HotelsService:
    """Service class to fetch and filter hotels data."""
    def __init__(self):
        self.data = pd.DataFrame(
            columns=pd.Index([
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
            ])
        )

    def merge_and_save(self, suppliers_data):
        """Merge the data from suppliers and save it in memory""" 

        # Normalize the data from suppliers and convert it to a pandas dataframe
        suppliers_df = pd.json_normalize(
            list(asdict(d) for d in suppliers_data if is_dataclass(d))
        )

        # Merge data
        self.data = suppliers_df.groupby('id').agg({
            'destination_id': lambda x: int(x.iloc[0]), # select first value
            'name': ah.longest_valid_text, 
            'location.lat': ah.first_valid_num,
            'location.lng': ah.first_valid_num,
            'location.address': ah.longest_valid_text,
            'location.city': ah.longest_valid_text,
            'location.country': ah.longest_valid_text,
            'description': ah.longest_valid_text,
            'amenities.general': ah.merge_lists,
            'amenities.room': ah.longest_valid_list,
            'images.rooms': lambda x: ah.merge_dict_lists(x, 'link'),
            'images.site': lambda x: ah.merge_dict_lists(x, 'link'),
            'images.amenities': lambda x: ah.merge_dict_lists(x, 'link'),
            'booking_conditions': ah.longest_valid_list
        }).reset_index()

        def _process_amenities(row):
            """
            Remove duplicates of general amenities from room amenities
            Standardize values of amenities: BusinessCenter -> business center
            """
            # regex to split camel case, ex: BusinessCenter -> Business Center
            regex = r'([a-z])([A-Z])', r'\1 \2'

            # exceptions to the rule
            exceptions = set(["WiFi", "wiFi", "TV", "DVD", "LAN"])

            # new lists to store the standardized values
            new_general_amenities = []
            new_room_amenities = []
            unique_general_amenities = set()
            unique_room_amenities = set()

            for x in row['amenities.room']:
                x = x.replace('-', ' ').replace('_', ' ')
                tmp = x
                if isinstance(x, str):
                    # Convert to lowercase and remove spaces
                    x = x.lower().replace(' ', '')
                    unique_room_amenities.add(x)

                    # Standardize the value
                    if tmp not in exceptions:
                        tmp = re.sub(regex[0], regex[1], tmp).lower()
                    else:
                        tmp = tmp.lower()
                    # Add the standardized value to the new list
                    new_room_amenities.append(tmp)

            for x in row['amenities.general']:
                x = x.replace('-', ' ').replace('_', ' ')
                tmp = x
                if isinstance(x, str):
                    # Convert to lowercase and remove spaces
                    x = x.lower().replace(' ', '')

                    # Check if the value is not in the room amenities
                    if x not in unique_room_amenities and x not in unique_general_amenities:
                        unique_general_amenities.add(x)

                        # Standardize the value
                        if tmp not in exceptions:
                            tmp = re.sub(regex[0], regex[1], tmp).lower()
                        else:
                            tmp = tmp.lower()

                        # Add the standardized value to the new list
                        new_general_amenities.append(tmp)

            # Save the new lists
            row['amenities.general'] = new_general_amenities
            row['amenities.room'] = new_room_amenities

            return row

        # Process the amenities
        self.data = self.data.apply(_process_amenities, axis=1)


    def find(self, hotel_ids, destination_ids):
        """Filter the data based on hotel_ids and destination_ids"""

        if hotel_ids and destination_ids:
            self.data = self.data[
                pd.Series(self.data['id']).isin(hotel_ids) & 
                pd.Series(self.data['destination_id']).isin(destination_ids)
            ]
        elif hotel_ids:
            self.data = self.data[pd.Series(self.data['id']).isin(hotel_ids)]
        elif destination_ids:
            self.data = self.data[pd.Series(self.data['destination_id']).isin(destination_ids)]


        # convert the data to json format
        return fh.df_to_formatted_json(self.data)