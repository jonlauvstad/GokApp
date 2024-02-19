from collections import defaultdict
import datetime


def organize_events(events):
    # Initialize a structure to hold events organized by venue and day
    events_by_venue_and_day = defaultdict(lambda: defaultdict(list))

    for event in events:
        try:
            # Assuming 'event' is a dictionary with 'venueName', 'time', and other details
            event_date = datetime.datetime.strptime(event['time'], '%Y-%m-%dT%H:%M:%S').date()
            weekday = event_date.strftime('%A')  # Adjust based on your locale if needed
            venue_name = event['venueName']  # or event['venue']['name'] if nested
        except KeyError as e:
            print(f"Missing key {e} for event: {event}")
            continue  # Skip this event or handle the missing key appropriately

        events_by_venue_and_day[venue_name][weekday].append(event)

    return events_by_venue_and_day




