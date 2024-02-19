from flask import render_template, session
import requests
from ..config import configuration
from ..a_event import organize_events
from datetime import datetime, timedelta


URLpre = configuration["URLpre"]

def get_venues_and_events():
    user = session.get("user")
    token = session.get("token")
    if not token:
        return render_template("error.html", message="You are not logged in.")

    headers = {'Authorization': f'Bearer {token}'}

    user_id = user.id if hasattr(user, 'id') else None

    venues_data = fetch_venues(headers)
    events_data = fetch_events(headers, user_id=user_id, event_type=None, from_date=None, to_date=None)
    days = organize_events(events_data)

    return render_template("admin_venue.html", venues=venues_data, days=days, user=user)

def fetch_venues(headers):
    # Implement fetching of venues
    response = requests.get(URLpre + "Venue", headers=headers, verify=False)
    if response.ok:
        return response.json()
    else:
        print(f"Error fetching venue data: {response.status_code}")
        return []


def fetch_events(headers, user_id, event_type=None, from_date=None, to_date=None):
    # Construct the URL with the user ID
    url = f"{URLpre}Event/User/{user_id}"

    # Prepare query parameters for filtering, if provided
    params = {}
    if event_type:
        params['type'] = event_type
    if from_date:
        params['from'] = from_date.strftime('%Y-%m-%d')
    if to_date:
        params['to'] = to_date.strftime('%Y-%m-%d')

    # Make the GET request with headers and query parameters
    response = requests.get(url, headers=headers, params=params, verify=False)

    if response.ok:
        events = response.json()
        print("Sample event data:", events[0] if events else "No events found")  # Add this line for debugging
        return events

    else:
        print(f"Error fetching event data: {response.status_code}, {response.text}")
        return []

def sort_events(events):
    organized_events = organize_events(events)
    return organized_events




def process_venue_availability(venues, events):
    # Initialize a dictionary to hold availability data
    venue_availability = {venue['id']: {'name': venue['name'], 'availability': {}} for venue in venues}

    # Process each event to mark venue availability
    for event in events:
        event_time = datetime.strptime(event['time'], '%Y-%m-%dT%H:%M:%S')
        venue_id = event['venueId']  # Assuming you have venueId in your event data
        day_of_week = event_time.strftime('%A')

        # If the venue and day_of_week not in availability, initialize it
        if day_of_week not in venue_availability[venue_id]['availability']:
            venue_availability[venue_id]['availability'][day_of_week] = False  # Mark as not available

    return venue_availability

