from hotel_service import HotelsService
from suppliers import AcmeSupplier, PatagoniaSupplier, PaperfliesSupplier

import argparse
import simplejson
import dotenv
import os

dotenv.load_dotenv()

def fetch_hotels(hotel_ids, destination_ids):
    """Fetch hotels data from suppliers and return as json"""
    
    # Initialize suppliers, able to add more suppliers here
    suppliers = [
        AcmeSupplier(api_url=os.getenv('ACME_API_URL')),
        PatagoniaSupplier(api_url=os.getenv('PATAGONIA_API_URL')),
        PaperfliesSupplier(api_url=os.getenv('PAPERFLIES_API_URL')),
    ]

    # Fetch data from all suppliers
    supplier_data = []
    for supplier in suppliers:
        supplier_data.extend(supplier.fetch())

    # Merge all the data and save it in-memory somewhere
    svc = HotelsService()
    svc.merge_and_save(supplier_data)

    # Fetch filtered data
    filtered = svc.find(hotel_ids, destination_ids)

    # Return as json
    return simplejson.dumps(filtered, ignore_nan=True)
    
def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("hotel_ids", type=str, help="Hotel IDs")
    parser.add_argument("destination_ids", type=str, help="Destination IDs")
    
    # Parse the arguments
    args = parser.parse_args()
    
    hotel_ids = args.hotel_ids
    destination_ids = args.destination_ids

    # Processing the arguments
    if hotel_ids.lower().strip() != 'none':
        hotel_ids = hotel_ids.split(',')
    else:
        hotel_ids = []

    if destination_ids.lower().strip() != 'none':
        destination_ids = destination_ids.split(',')
        destination_ids = [int(x) for x in destination_ids]
    else:
        destination_ids = []
        
    # Fetch hotels
    result = fetch_hotels(hotel_ids, destination_ids)
    print(result)

if __name__ == "__main__":
    main()