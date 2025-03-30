import os
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()


def get_location_id(destination):
    try:
        url = "https://booking-com.p.rapidapi.com/v1/hotels/locations"

        querystring = {"locale":"en-us","name":destination}
        headers = {
	"x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),
	"x-rapidapi-host": "booking-com.p.rapidapi.com"
}

        response = requests.get(url, headers=headers, params=querystring)

        data = response.json()
        dest_type = data[0]["dest_type"]
        dest_id = data[0]["dest_id"]
        print(dest_type,dest_id)
        return (dest_type,dest_id)
    except:
        print("Error getting location id")
        return None

def get_hotels(location, check_in, check_out, adults, rooms):
    try:
        dest_type, dest_id = get_location_id(location)
        if not dest_type or not dest_id:
            return {"hotels": []}
            
        url = "https://booking-com.p.rapidapi.com/v2/hotels/search"
        querystring = {
            "include_adjacency":"true",
            "adults_number":f"{adults}",
            "units":"metric",
            "locale":"en-us",
            "dest_type":str(dest_type),
            "dest_id":str(dest_id),
            "checkin_date":check_in.strftime("%Y-%m-%d"),
            "checkout_date": check_out.strftime("%Y-%m-%d"),
            "filter_by_currency":"INR",
            "order_by":"price",
            "room_number":f"{rooms}"

        }
        
        response = requests.get(
            url,
            headers={
                "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
                "X-RapidAPI-Host": "booking-com.p.rapidapi.com"
            },
            params=querystring
        )
        full_data = response.json()
        # print(full_data)
        simplified_hotels = full_data['results'][:3]
        
        return {"hotels": simplified_hotels}
    except Exception as e:
        print(f"Error getting hotels: {str(e)}")
        return {"hotels": []}

# departure = "Mumbai"
# destination = "Delhi"
# check_in = datetime.strptime("2025-04-10", "%Y-%m-%d")  # or specify a future date
# check_out = datetime.strptime("2025-04-15", "%Y-%m-%d")  # or specify a future date

# output = get_hotels(destination, check_in, check_out,1,1)
# print("Flight Search Results:")
# print(output)
