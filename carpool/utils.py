import requests
import urllib.parse
from carpool import settings
from datetime import datetime, timedelta


def geocode_address(address):
    """Convert an address to latitude and longitude using Google Maps API."""
    API_KEY = settings.GOOGLE_MAPS_API_KEY
    address = urllib.parse.quote(address)
    url = f"https://api.geocod.io/v1.7/geocode?q={address}&api_key={API_KEY}&format=simple"
    # print(url)
    response = requests.get(url)
    data = response.json()

    if data.get("lat") !=   None:
        print(data)
        return data["lat"], data["lng"]
    print("No coordinates found")
    return None, None

def mins_before(schedule, mins):
    '''utility function to subtract mins from a schedule returns time object'''
    arrvl_time = schedule.arrival_time
    arrvl_dt = datetime.combine(datetime.today(), arrvl_time)

    chgd_dt = arrvl_dt + timedelta(minutes=mins)

    return chgd_dt.time()

