from dateutil import parser
# from datetime import datetime
import datetime
# from utility.event import Event

class EventDay:
    def __init__(self, date, events):
        self.date = date                    # date skal være et DateTime-objekt
        self.weekday = date.weekday()
        self.datestring = date.strftime("%a %d.%b")
        self.events = []  # events er en liste med Event-objekter
        for item in events:
            self.events.append(item)

    @staticmethod
    def make_days(start_date, num_days, events):
        days = []
        for i in range(num_days):
            timedelta = datetime.timedelta(days=i)
            date = start_date + timedelta

            event_day = EventDay(date, [item for item in events if item.date==date])   #  if item.date==date.date()
            days.append(event_day)
        return days