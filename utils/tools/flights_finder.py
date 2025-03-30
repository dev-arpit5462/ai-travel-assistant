import os
import requests
from dotenv import load_dotenv

load_dotenv()
from datetime import datetime


def des_id(from_location, to_location):

    try:
        url = "https://booking-com15.p.rapidapi.com/api/v1/flights/searchDestination"
        headers = {
            "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
            "X-RapidAPI-Host": "booking-com15.p.rapidapi.com"
        }
        query1 = {"query":from_location}
        query2 = {"query":to_location}
        response = requests.get(url, headers=headers, params=query1)
        from_id = response.json()["data"][0]["id"]
        response = requests.get(url, headers=headers, params=query2)
        to_id = response.json()["data"][0]["id"]
        return (from_id, to_id)
    except:
        return (None,None)
    

def get_flights(departure, destination, departDate, adults=1):
    try:
        from_id, to_id = des_id(departure, destination)
        if not from_id or not to_id:
            return {"flights": []}
            
        url = "https://booking-com15.p.rapidapi.com/api/v1/flights/searchFlights"
        headers = {
            "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
            "X-RapidAPI-Host": "booking-com15.p.rapidapi.com"
        }
        params = {
            "fromId": from_id,
            "toId": to_id,
            "departDate": departDate.strftime("%Y-%m-%d"),
            "adults": adults,
            "currency_code": "INR"
        }
        
        response = requests.get(url, headers=headers, params=params)
        full_data = response.json()
        
        simplified_flights = full_data['data']['aggregation']['airlines'][:4]
        
        return {"flights": simplified_flights}
    except Exception as e:
        print(f"Error fetching flight data: {str(e)}")
        return {"flights": []}


# Test the flight search
# departure = "Mumbai"
# destination = "Delhi"
# depart_date = datetime.strptime("2025-04-10", "%Y-%m-%d")  # or specify a future date

# results = get_flights(departure, destination, depart_date)
# print("Flight Search Results:")
# print(results)
