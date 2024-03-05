from flask import render_template, session, request, flash
import requests
from datetime import datetime, timedelta
from dateutil import parser
from ..event import Event
from ..event_day import EventDay
from ..config import configuration
from ..venue import Venue

URLpre = configuration["URLpre"]

def venue_calendar_function():
    user = session["user"]
    token = session["token"]
    if not token:
        return render_template("error.html", message="You are not logged in.")
    headers = {"Authorization": f"Bearer {token}"}
    # 1. lage html design først
    # 3 loops
    # Ytre loop event day (x aksen) (for event in event days)
    # indre loop : (for venue in venues)
    # hvs id matcher, trejde loop
    # hvordan få tabell-rows til å bli relative i str
    # S - 8 / 16
    # s - 8 / 16 - 8

    # tidsramme ..
    # start_date_param = request.args.get('start')
    # start_date = datetime.now().date() if not start_date_param else parser.parse(start_date_param).date()
    # num_days = int(request.args.get('num_days', 14))

    # tidsramme v2
    start_date_str = request.args.get('start')
    if start_date_str:
        start_date = parser.parse(start_date_str).date()
    else:
        start_date = datetime.now().date()

    num_days = request.args.get('num_days', default=14, type=int)
    from_date = start_date
    to_date = from_date+timedelta(days=num_days)
    # to_date = start_date + timedelta(days=num_days)

    # get venues and events
    venues = fetch_venues(headers)
    events = fetch_events(headers, from_date=from_date.isoformat(), to_date=to_date.isoformat())
    days = []

    for i in range(num_days):
        day_date = start_date + timedelta(days=i)
        day_events = [event for event in events if event.date == day_date]
        days.append(EventDay(day_date, day_events))

    today = start_date.strftime("%Y-%m-%d")
    current_day = datetime.now().date().strftime("%a %d.%b")

    # debugging.. printer dager og eventer for hver dag
    for day in days:
        print(day.datestring, [f"{event.courseImpName}-{event.venueId}" for event in day.events])
    for day in days:
        print([event.venueId for event in day.events])
    return render_template("venue_calendar.html", user=user, events=events, venues=venues, days=days, num_days=num_days, today=today, current_day=current_day)


def fetch_venues(headers):
    venues_url = f"{URLpre}Venue/"
    response = requests.get(venues_url, headers=headers, verify=False)
    if response.ok:
        print("Venues JSON Data:", response.json())
        venues = [
            Venue(
                id=item['id'],
                name=item['name'],
                description=item['description'],
                locationId=item['locationId'],
                streetAddress=item['streetAddress'],
                postCode=item['postCode'],
                city=item['city'],
                capacity=item['capacity'],
                locationName=item['locationName'],
                link=item.get('link'),  # bruker .get() i tilfelle 'link' key ikke finnes..
                links=item.get('links')  # samme for 'links'
            ) for item in response.json()
        ]

    else:
        print(f"Error fetching venue data: {response.status_code}, {response.text}")
        venues = []
    return venues


def fetch_events(headers, from_date=None, to_date=None):
    events_url = f"{URLpre}Event/"

    params = {
        'from': from_date,
        'to_date': to_date
    }

    response = requests.get(events_url, headers=headers, params=params, verify=False)
    if response.ok:
        print("Events JSON Data:", response.json())
        events = [
            Event(
                item['time'],
                item['underlyingId'],
                item['type'],
                item['typeEng'],
                item['courseImplementationId'],
                item['courseImpCode'],
                item['courseImpName'],
                item['courseImplementationLink'],
                item['link'],
                item['timeEnd'] if item['timeEnd'] != '0001-01-01T00:00:00' else None,
                item['venueId'],
                item['venueName'],
                item['venueCapacity']
            ) for item in response.json()
        ]
        for event in events:
            event.datetime = parser.parse(event.time)
            event.datetimeFormatted = event.datetime.strftime("%Y-%m-%d %H:%M")
            if event.timeEnd and event.timeEnd != '0001-01-01T00:00:00':
                event.datetimeEnd = parser.parse(event.timeEnd)
                event.datetimeEndFormatted = event.datetimeEnd.strftime("%Y-%m-%d %H:%M")
            else:
                event.datetimeEnd = None
                event.datetimeEndFormatted = None
    else:
        print(f"Error fetching event data: {response.status_code}, {response.text}")
        events = []

    return events


def calculate_num_days(start_date, end_date):
    try:
        start = parser.parse(start_date)
        end = parser.parse(end_date)
    except ValueError:
        # Handle the error, e.g., by logging and returning a default value or re-raising a more descriptive exception
        print("Error parsing dates. Please ensure they are in the correct format.")
        return None  # Or consider raising an exception or returning 0

    # Check if either date is None after parsing attempt
    if start is None or end is None:
        print("One of the dates is None. Please provide valid dates.")
        return None

    delta = end - start
    return delta.days

"""def process_venue_availability(venues, events):
    venue_availability = {venue['id']: {'name': venue['name'], 'availability': {}} for venue in venues}

    for event in events:
        event_time = datetime.strptime(event['time'], '%Y-%m-%dT%H:%M:%S')
        venue_id = event['venueId']
        day_of_week = event_time.strftime('%A')

        if day_of_week not in venue_availability[venue_id]['availability']:
            venue_availability[venue_id]['availability'][day_of_week] = False

    return venue_availability"""


"""def organize_events(events):
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
"""

