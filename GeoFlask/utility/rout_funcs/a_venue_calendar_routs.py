from flask import render_template, session, request, flash
import requests
# from ..a_event import organize_events
from datetime import datetime, timedelta
from dateutil import parser
from ..event import Event
from ..event_day import EventDay
from ..config import configuration
from collections import defaultdict

from ..lecture import Lecture

URLpre = configuration["URLpre"]


def venue_calendar_function():
    user = session["user"]
    token = session["token"]

    if not token:
        return render_template("error.html", message="You are not logged in.")

    headers = {"Authorization": f"Bearer {session['token']}"}

    start_date = request.args.get('start')
    start = datetime.now().date()

    if start_date:
        start = parser.parse(start_date).date()
    today = start.strftime("%Y-%m-%d")
    num_days = request.args.get('num_days', default=14, type=int)

    # endpoints
    lectures_url = f"{URLpre}Lecture/GetLectures"
    venues_url = f"{URLpre}Venue/GetAllVenues"

    print(f"Requesting URL: {lectures_url}")
    print(f"Requesting URL: {venues_url}")

    try:
        # events
        lectures_response = requests.get(lectures_url, verify=False, headers=headers)
        if lectures_response.ok:
            lectures = lectures_response.json()
            # lectures = [Lecture(item['theme'], item['startTime'], item['endTime'], item['courseImplementationName'], item['teacherNames'], item['venueNames']) for item in response]
            # days = EventDay.make_days(start, num_days, lectures)
            print(lectures)
            return render_template("venue_calendar.html", user=user, lectures=lectures, num_days=num_days, today=today)

        msg = f"Statuskode: {lectures_response.status_code}"
        return render_template("error.html", message="An unexpected error occurred.", status=lectures_response.status_code)

    except requests.exceptions.RequestException as e:
        print(f'An error occurred: {e}')


"""        # venues
        venues_response = requests.get(venues_url, verify=False, headers=headers)
        if venues_response.ok:
            venues_data = [Venue(**data) for data in venues_response.json()]
        else:
            venues_data = []

        # print(lectures_data)
        print(venues_data)"""

def get_venues_and_events():
    user = session["user"]
    token = session["token"]

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
    response = requests.get(URLpre + "Venue/GetAllVenues", headers=headers, verify=False)
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
        print("Sample event data:", events[0] if events else "No events found")
        return events

    else:
        print(f"Error fetching event data: {response.status_code}, {response.text}")
        return []


def sort_events(events):
    organized_events = organize_events(events)
    return organized_events


def process_venue_availability(venues, events):
    venue_availability = {venue['id']: {'name': venue['name'], 'availability': {}} for venue in venues}

    for event in events:
        event_time = datetime.strptime(event['time'], '%Y-%m-%dT%H:%M:%S')
        venue_id = event['venueId']
        day_of_week = event_time.strftime('%A')

        if day_of_week not in venue_availability[venue_id]['availability']:
            venue_availability[venue_id]['availability'][day_of_week] = False

    return venue_availability


def organize_events(events):
    # Initialiserer en struktur for å holde eventer organisert etter Venue og dag
    events_by_venue_and_day = defaultdict(lambda: defaultdict(list))

    for event in events:
        try:
            event_date = datetime.datetime.strptime(event['time'], '%Y-%m-%dT%H:%M:%S').date()
            weekday = event_date.strftime('%A')
            venue_name = event['venueName']
        except KeyError as e:
            print(f"Missing key {e} for event: {event}")
            continue

        events_by_venue_and_day[venue_name][weekday].append(event)

    return events_by_venue_and_day


