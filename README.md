## Hotel Fetcher

### Example output

```
{
    "id": "f8c9",
    "destination_id": 1122,
    "name": "Hilton Shinjuku Tokyo",
    "location": {
        "lat": 35.6926,
        "lng": 139.690965,
        "address": "160-0023, SHINJUKU-KU, 6-6-2 NISHI-SHINJUKU, JAPAN, 160-0023",
        "city": "Tokyo",
        "country": "Japan"
    },
    "description": "This sleek high-rise property is 10 minutes' walk from Shinjuku train station, 6 minutes' walk from the Tokyo Metropolitan Government Building and 3 km from Yoyogi Park. The polished rooms offer Wi-Fi and flat-screen TVs, plus minibars, sitting areas, and tea and coffeemaking facilities. Suites add living rooms, and access to a club lounge serving breakfast and cocktails. A free shuttle to Shinjuku station is offered. There's a chic Chinese restaurant, a sushi bar, and a grill restaurant with an open kitchen, as well as an English pub and a hip cocktail lounge. Other amenities include a gym, rooftop tennis courts, and a spa with an indoor pool.",
    "amenities": {
        "general": [
            "indoor pool",
            "business center",
            "wifi"
        ],
        "room": [
            "tv",
            "aircon",
            "minibar",
            "bathtub",
            "hair dryer"
        ]
    },
    "images": {
        "rooms": [
            {
                "link": "https://d2ey9sqrvkqdfs.cloudfront.net/YwAr/i10_m.jpg",
                "description": "Suite"
            },
            {
                "link": "https://d2ey9sqrvkqdfs.cloudfront.net/YwAr/i11_m.jpg",
                "description": "Suite - Living room"
            },
            {
                "link": "https://d2ey9sqrvkqdfs.cloudfront.net/YwAr/i1_m.jpg",
                "description": "Suite"
            },
            {
                "link": "https://d2ey9sqrvkqdfs.cloudfront.net/YwAr/i15_m.jpg",
                "description": "Double room"
            }
        ],
        "site": [
            {
                "link": "https://d2ey9sqrvkqdfs.cloudfront.net/YwAr/i55_m.jpg",
                "description": "Bar"
            }
        ],
        "amenities": [
            {
                "link": "https://d2ey9sqrvkqdfs.cloudfront.net/YwAr/i57_m.jpg",
                "description": "Bar"
            }
        ]
    },
    "booking_conditions": [
        "All children are welcome. One child under 6 years stays free of charge when using existing beds. There is no capacity for extra beds in the room.",
        "Pets are not allowed.",
        "Wired internet is available in the hotel rooms and charges are applicable. WiFi is available in the hotel rooms and charges are applicable.",
        "Private parking is possible on site (reservation is not needed) and costs JPY 1500 per day.",
        "When booking more than 9 rooms, different policies and additional supplements may apply.",
        "The hotel's free shuttle is offered from Bus Stop #21 in front of Keio Department Store at Shinjuku Station. It is available every 20-minutes from 08:20-21:40. The hotel's free shuttle is offered from the hotel to Shinjuku Train Station. It is available every 20-minutes from 08:12-21:52. For more details, please contact the hotel directly. At the Executive Lounge a smart casual dress code is strongly recommended. Attires mentioned below are strongly discouraged and may not permitted: - Night attire (slippers, Yukata robe, etc.) - Gym clothes/sportswear (Tank tops, shorts, etc.) - Beachwear (flip-flops, sandals, etc.) and visible tattoos. Please note that due to renovation works, the Executive Lounge will be closed from 03 January 2019 until late April 2019. During this period, guests may experience some noise or minor disturbances. Smoking preference is subject to availability and cannot be guaranteed."
    ]
}
```

### Merging solution

Using **pandas** to process and merge data.

Firstly, collect all data from suppliers and normalize it into a DataFrame.

Secondly, perform a group-by operation on the **id** field in the DataFrame, and for each field, apply the following aggregations:

- **destination_id**: Select first value
- **name**: Select longest valid text
- **location.lat**: Select first number
- **location.lng**: Select first number
- **location.address**: Select longest valid text
- **location.city**: Select longest valid text
- **location.country**: Select longest valid text
- **description**: Select longest valid text
- **amenities.general**: Select last valid list
- **amenities.room**: Select last valid list
- **images.rooms**: Merge list and remove duplicates
- **images.site**: Merge list and remove duplicates
- **images.amenities**: Merge list and remove duplicates
- **booking_conditions**: Select longest valid text

Finally, filtering on Dataframe