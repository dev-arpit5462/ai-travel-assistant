import os
import google.generativeai as genai
from dotenv import load_dotenv
from .models import Flight, Hotel, TravelPlan
import json

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def parse_travel_data(flights_data: dict, hotels_data: dict) -> TravelPlan:
    try:
        # Format flights data
        formatted_flights = []
        for flight in flights_data.get('flights', []):
            formatted_flight = {
                'name': str(flight.get('name', 'Unknown')),
                'price': float(flight.get('minPrice', {}).get('units', 0)),
                'currencyCode': str(flight.get('minPrice', {}).get('currencyCode', 'Unknown')),
                'logoUrl': str(flight.get('logoUrl', ''))
            }
            formatted_flights.append(formatted_flight)

        # Format hotels data
        formatted_hotels = []
        for hotel in hotels_data.get('hotels', []):
            formatted_hotel = {
                'name': str(hotel.get('name', 'Unknown')),
                'address': str(hotel.get('location', '')),
                'price': float(hotel.get('priceBreakdown', {}).get('grossPrice', {}).get('value', 0)),
                # 'rating': float(hotel.get('rating', 0)),
                'photoMainUrl': str(hotel.get('photoMainUrl', '')),
                'facilities': hotel.get('amenities', [])[:3],
                'reviewScore': float(hotel.get('reviewScore', 0))
            }
            formatted_hotels.append(formatted_hotel)

        # Create TravelPlan with formatted data
        return TravelPlan(
            flights=[Flight(**flight) for flight in formatted_flights],
            hotels=[Hotel(**hotel) for hotel in formatted_hotels],
            itinerary=""
        )
    except Exception as e:
        print(f"Error parsing travel data: {e}")
        return TravelPlan()  # Return empty travel plan on error

def generate_itinerary(destination: str, days: int, interests: list, budget) -> str:
    model = genai.GenerativeModel('gemini-1.5-pro')
    
    prompt = f"""
    Create a detailed {days}-day itinerary for {destination} focusing on {', '.join(interests)} also keeping budget of {budget} which is in INR of per day.
    If given budget is not enough you can suggest any other budget which is closest to given budget

    Include for each day:
    - Morning/afternoon/evening activities
    - Restaurant recommendations
    - Travel tips
    - Estimated costs change it in INR

    At the end of all days give a summary of total estimated cost in INR
    
    Format in Markdown with headings and bullet points.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating itinerary: {str(e)}"