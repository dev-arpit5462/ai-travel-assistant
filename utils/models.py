from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Flight(BaseModel):
    name: str
    logoUrl: Optional[str]
    price: float
    currencyCode: str
    class Config:
        populate_by_name = True

class Hotel(BaseModel):
    name: str
    location: str = Field(alias='address')
    price: float = Field(default=0.0)
    # rating: float = Field(default=0.0)
    image_url: Optional[str] = Field(default='', alias='photoMainUrl')
    amenities: List[str] = Field(default_factory=list, alias='facilities')
    review_score: Optional[float] = Field(default=0.0, alias='reviewScore')

    class Config:
        populate_by_name = True

class TravelPlan(BaseModel):
    flights: List[Flight] = Field(default_factory=list)
    hotels: List[Hotel] = Field(default_factory=list)
    itinerary: str = Field(default="") 