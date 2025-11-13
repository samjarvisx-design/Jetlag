from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from zoneinfo import ZoneInfo
from Jetlagg import get_sleep_recommendations, get_timezone_abbreviation

app = FastAPI(title="Jetlag Sleep Calculator API")

# Enable CORS for web frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class JetlagRequest(BaseModel):
    origin_tz: str  # e.g., "America/New_York"
    dest_tz: str     # e.g., "Europe/London"
    departure_time: str  # Format: "2024-12-15 14:30"
    flight_duration_hours: float = 0.0


class JetlagResponse(BaseModel):
    time_difference_hours: float
    arrival_time_dest: str
    is_eastward: bool
    pre_flight_sleep: list
    post_flight_sleep: list
    tips: list
    origin_tz_abbrev: str
    dest_tz_abbrev: str


@app.get("/")
def read_root():
    return {
        "message": "Jetlag Sleep Calculator API",
        "endpoints": {
            "/": "This message",
            "/calculate": "POST - Calculate jetlag sleep recommendations",
            "/timezones": "GET - List common timezones",
            "/docs": "API documentation"
        }
    }


@app.get("/timezones")
def get_timezones():
    """Get list of common timezones"""
    return {
        "timezones": {
            "America/New_York": "New York (EST/EDT)",
            "America/Chicago": "Chicago (CST/CDT)",
            "America/Denver": "Denver (MST/MDT)",
            "America/Los_Angeles": "Los Angeles (PST/PDT)",
            "Europe/London": "London (GMT/BST)",
            "Europe/Paris": "Paris (CET/CEST)",
            "Asia/Tokyo": "Tokyo (JST)",
            "Asia/Shanghai": "Shanghai (CST)",
            "Australia/Sydney": "Sydney (AEDT/AEST)",
            "Pacific/Auckland": "Auckland (NZDT/NZST)",
        }
    }


@app.post("/calculate", response_model=JetlagResponse)
def calculate_jetlag(request: JetlagRequest):
    """
    Calculate jetlag sleep recommendations based on travel details.
    
    Example request:
    {
        "origin_tz": "America/New_York",
        "dest_tz": "Europe/London",
        "departure_time": "2024-12-15 14:30",
        "flight_duration_hours": 7.5
    }
    """
    try:
        # Parse departure time
        try:
            departure_time = datetime.strptime(request.departure_time, '%Y-%m-%d %H:%M')
            departure_time = departure_time.replace(tzinfo=ZoneInfo(request.origin_tz))
        except ValueError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid departure_time format. Use 'YYYY-MM-DD HH:MM'. Error: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid timezone or datetime. Error: {str(e)}"
            )
        
        # Calculate recommendations
        recommendations = get_sleep_recommendations(
            request.origin_tz,
            request.dest_tz,
            departure_time,
            request.flight_duration_hours
        )
        
        # Format response
        return JetlagResponse(
            time_difference_hours=recommendations['time_difference_hours'],
            arrival_time_dest=recommendations['arrival_time_dest'].strftime('%Y-%m-%d %H:%M %Z'),
            is_eastward=recommendations['is_eastward'],
            pre_flight_sleep=recommendations['pre_flight_sleep'],
            post_flight_sleep=recommendations['post_flight_sleep'],
            tips=recommendations['tips'],
            origin_tz_abbrev=get_timezone_abbreviation(request.origin_tz),
            dest_tz_abbrev=get_timezone_abbreviation(request.dest_tz)
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error calculating jetlag recommendations: {str(e)}"
        )
