from datetime import timedelta

from dateutil import parser


class Prefill:
    def __init__(self, venue_id, start_date, end_date=None, with_time=False):
        self.venue_id = venue_id
        if not with_time:
            self.start_date = start_date
            self.start_date_dt = parser.parse(start_date)
        else:
            date_elm = parser.parse(start_date)
            time_elm = with_time.split(":")[0]
            if time_elm[0] == "0":
                time_elm = time_elm[-1]
            time_elm = int(time_elm)
            self.start_date_dt = date_elm+timedelta(hours=time_elm)
            self.start_date = self.start_date_dt.__str__()
        self.end_date = end_date
        self.end_date_dt = None if end_date == None else parser.parse(end_date)

    def serialize(self):
        return {
            "venue_id": self.venue_id,
            "start_date": self.start_date,
            "start_date_dt": self.start_date_dt,
            "end_date": self.end_date,
            "end_date_dt": self.end_date_dt,
        }

prefill = Prefill(venue_id=1, start_date="2024-03-21", with_time="10:00")

print(prefill.serialize())
