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

    # get start & end dates
    start_date_str = request.args.get('start')
    end_date_str = request.args.get('end')

    if start_date_str:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%dT%H:%M")
    else:
        start_date = datetime.now()

    if end_date_str:
        end_date = datetime.strptime(end_date_str, "%Y-%m-%dT%H:%M")
    else:
        end_date = start_date + timedelta(days=7)


    # get venues and events
    venues = fetch_venues(headers)
    events = fetch_events(headers, from_date=start_date.isoformat(), to_date=end_date.isoformat())

    print(f"ℹ️ venue_calendar_function() : events:  {events}")

    # Genererer "days" med "events" + weekend logic
    num_days = (end_date - start_date).days + 1
    days = []
    for i in range(num_days):
        day_date = start_date + timedelta(days=i)
        day_events = [event for event in events if event.datetime.date() == day_date.date()]
        print(f"ℹ️ DAY_EVENTS: {day_events}")
        day = EventDay(day_date, day_events)
        day.is_weekend = day_date.weekday() >= 5
        days.append(day)

    # Date-formater ..
    today = start_date.strftime("%Y-%m-%d")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M")
    current_day = datetime.now().date().strftime("%a %d.%b")

    return render_template("venue_calendar.html",
                           user=user,
                           events=events,
                           venues=venues,
                           days=days,
                           today=today,
                           tomorrow=tomorrow,
                           current_day=current_day,
                           start_date=start_date.strftime("%Y-%m-%dT%H:%M"),
                           end_date=end_date.strftime("%Y-%m-%dT%H:%M"))


def fetch_events(headers, from_date=None, to_date=None):
    events_url = f"{URLpre}Event/"

    params = {
        'from': from_date,
        'to_date': to_date
    }

    response = requests.get(events_url, headers=headers, params=params, verify=False)
    print(f"ℹ️ RESPONSE: {response}")

    if response.ok:
        # print("Events JSON Data:", response.json())
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

        filteredEvents = [item for item in events if item.typeEng == "Lecture"]

        print(len(filteredEvents))
        print(f"ℹ️ FILTERED EVENTS: {filteredEvents}")

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

    for event in events:
        print(f"Event Date: {event.datetime.date()}")

    return events


def venue_cal_single_day(date_str):
    user = session.get("user")
    token = session.get("token")
    if not token:
        return render_template("error.html", message="You are not logged in.")
    headers = {"Authorization": f"Bearer {token}"}

    # Parse the date from the URL parameter
    try:
        date = parser.parse(date_str).date()
    except ValueError:
        return render_template("error.html", message="Invalid date format.")

    # Assuming you have a similar setup for fetching venues and events
    venues = fetch_venues(headers)
    events = fetch_events(headers, from_date=date.isoformat(), to_date=(date + timedelta(days=1)).isoformat())

    # Filter events for the specific day
    day_events = [event for event in events if event.datetime.date() == date]
    day = EventDay(date, day_events)
    day.generate_time_blocks_with_rowspan()

    # Render the SingleDayView template with the day's data
    return render_template("venue_cal_single_day.html",
                           user=user,
                           events=day_events,
                           venues=venues,
                           day=day)


def fetch_venues(headers):
    venues_url = f"{URLpre}Venue/"
    response = requests.get(venues_url, headers=headers, verify=False)
    if response.ok:
        # print("Venues JSON Data:", response.json())
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


def fetch_venue_by_id(headers, venue_id):
    user = session["user"]
    token = session["token"]
    if not token:
        return render_template("error.html", message="You are not logged in.")
    headers = {"Authorization": f"Bearer {token}"}

    print(f"Attempting to fetch details for venue ID: {venue_id}")
    venue_url = f"{URLpre}Venue/{venue_id}"
    print(f"Fetching venue details from: {venue_url}")

    try:
        response = requests.get(venue_url, headers=headers, verify=False)
        print(f"Response status code: {response.status_code}")  # Print the status code of the response
        if response.ok:
            item = response.json()
            print("Venue data received:", item)  # Print the JSON data received
            venue = Venue(
                    id=item['id'],
                    name=item['name'],
                    description=item['description'],
                    locationId=item['locationId'],
                    streetAddress=item['streetAddress'],
                    postCode=item['postCode'],
                    city=item['city'],
                    capacity=item['capacity'],
                    locationName=item['locationName'],
                    link=item.get('link'),  # Using .get() in case 'link' key doesn't exist
                    links=item.get('links')  # Same for 'links'
                )
            return venue
        else:
            print(f"Error fetching venue data: {response.status_code}, {response.text}")  # Print the error status code and text
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")  # Print the exception if the request failed
    return None




def calculate_num_days(start_date, end_date):
    if not start_date or not end_date:
        print("One of the dates is None. Please provide valid dates.")
        return None

    try:
        start = parser.parse(start_date)
        end = parser.parse(end_date)
        delta = end - start
        return delta.days

    except ValueError:
        print("Error parsing dates. Please ensure they are in the correct format.")
        return None


def venue_booking_data(day, date, time, venue_id):
    user = session["user"]
    token = session["token"]
    if not token:
        return render_template("error.html", message="You are not logged in.")
    headers = {"Authorization": f"Bearer {token}"}

    venue_details = fetch_venue_by_id(headers, venue_id)
    print("Venue ID (fra routs func):", venue_id)
    print("Venue Details (fra routs func):", venue_details)
    print("Time (fra routs func)", time)
    print("Date (fra routs func):", date)

    time_list = time.split(":")
    time_str0 = time.split(":")[0]
    time_str1 = time.split(":")[1]
    if time_str0[0] == "0":
        time_str0 = time_str0[-1]
    if time_str1[0] == "0":
        time_str1 = time_str1[-1]
    time_float = int(time_str0) + int(time_str1)/60

    return render_template('venue_booking.html', user=user, day=day, date=date, time=time, time_float=time_float,
                           venue_details=venue_details, venue_id=venue_id)


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

