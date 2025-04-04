import streamlit as st
from utils.gemini_helper import generate_itinerary, parse_travel_data
from utils.tools.flights_finder import get_flights
from utils.tools.hotels_finder import get_hotels
from utils.models import TravelPlan
import datetime

# Configure page settings
st.set_page_config(
    page_title="AI Travel Assistant",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
def load_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# App header
st.title("🌍 AI Travel Assistant")
st.markdown("Plan your perfect trip with AI-powered recommendations")

# Sidebar for user inputs
with st.sidebar:
    st.header("Trip Details")
    destination = st.text_input("Destination City")
    departure = st.text_input("Departure City") 
    start_date = st.date_input("Start Date", datetime.date.today())
    end_date = st.date_input("End Date", datetime.date.today())
    adults = st.number_input("Number of Adults", min_value=1, value=1)
    rooms = st.number_input("Number of Rooms", min_value=1, value=1)
    interests = st.multiselect("Interests", ["Beaches", "Hiking", "Museums", "Food", "Others"])
    if "Others" in interests:
        custom_interests = st.text_input("Enter your interests (comma-separated)")
        if custom_interests:
            # Remove "Others" and add custom interests
            interests.remove("Others")
            interests.extend([i.strip() for i in custom_interests.split(",")])
    perday_budget = st.text_input("Budget per day (INR) excluding hotel")
    if interests == "Others":
        interests = st.text_input("Enter your interests")
    if st.button("Plan My Trip", type="primary"):
        st.session_state.plan_requested = True

def display_flight_card(flight):
    with st.container():
        st.markdown("""
        <div class="flight-card">
            <img src="{logoUrl}" alt="{name}" class="flight-image"/>
            <div class="airline-header">
                <h3>{name}</h3>
                <p class="price">₹{price:,.2f}</p>
                <p class="currency">{currencyCode}</p>
            </div>
        </div>
        """.format(
            name=flight.name,
            price=flight.price,
            logoUrl=flight.logoUrl or "assets/images/banner.png",
            currencyCode=flight.currencyCode
        ), unsafe_allow_html=True)

def display_hotel_card(hotel):
    with st.container():
        st.markdown("""
        <div class="hotel-card">
            <img src="{image_url}" alt="{name}" class="hotel-image"/>
            <div class="hotel-info">
                <h3>{name}</h3>
                <p>📍 {location}</p>
                <p>⭐ {review_score}/5</p>
                <p class="price">₹{price:,.2f} for full Trip </p>
                <p>🏨 {amenities}</p>
            </div>
        </div>
        """.format(
            image_url=hotel.image_url or "assets/images/banner.png",
            name=hotel.name,
            location=hotel.location,
            # rating=hotel.rating,
            review_score=hotel.review_score,
            price=hotel.price,
            amenities=", ".join(hotel.amenities)
        ), unsafe_allow_html=True)

# Main content area
if st.session_state.get('plan_requested'):
    with st.spinner("Creating your personalized travel plan..."):
        # Get raw data
        flights_data = get_flights(departure, destination, start_date, adults)
        hotels_data = get_hotels(destination, start_date, end_date, adults, rooms)
        
        # Use Gemini to parse and structure the data
        travel_plan = parse_travel_data(flights_data, hotels_data)
        
        # Generate itinerary
        travel_plan.itinerary = generate_itinerary(destination, (end_date - start_date).days, interests,perday_budget)
        
        # Display sections
        st.header("🗺️ Your Travel Plan")
        
        tab1, tab2, tab3 = st.tabs(["📅 Itinerary", "✈️ Flights", "🏨 Hotels"])
        
        with tab1:
            st.markdown(travel_plan.itinerary)
        
        with tab2:
            st.subheader("Available Flights")
            if travel_plan.flights:
                flight_cols = st.columns(2)
                for idx, flight in enumerate(travel_plan.flights):
                    with flight_cols[idx % 2]:
                        display_flight_card(flight)
            else:
                st.warning("No flights found for the selected criteria.")
        
        with tab3:
            st.subheader("Recommended Hotels")
            if travel_plan.hotels:
                hotel_cols = st.columns(2)
                for idx, hotel in enumerate(travel_plan.hotels):
                    with hotel_cols[idx % 2]:
                        display_hotel_card(hotel)
            else:
                st.warning("No hotels found for the selected criteria.")
else:
    # Show welcome content when no plan requested
    st.image("assets/images/banner.png", use_container_width=True)
    st.markdown("""
    ## Plan Your Dream Vacation
    Created with ❤️ by [@Arpit Singh](https://github.com/dev-arpit5462)
                
    Our AI-powered travel assistant will:
    - ✨ Create a personalized daily itinerary
    - ✈️ Find the best flight deals
    - 🏨 Recommend perfect accommodations
    - 🗺️ Suggest must-see attractions
    
    Get started by entering your trip details in the sidebar!
    """)
