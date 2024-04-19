from dateutil import parser
# from datetime import datetime
import datetime
# from utility.event import Event
from datetime import datetime, timedelta, time      # Tror Andreas adda denne importen og det kødda til linje 21


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
            timedelta_ = timedelta(days=i)      # 8. april Måtte endre fra timedelta = datetime.timedelta(days=i)
            date = start_date + timedelta_


            event_day = EventDay(date, [item for item in events if item.date==date])   #  if item.date==date.date()
            days.append(event_day)
        return days

    def generate_time_blocks(self, start_hour=8, end_hour=15, duration=1):
        self.time_blocks = []  # Initialiserer time_blocks her
        current_time = datetime.combine(self.date, time(start_hour, 0))

        while current_time.hour < end_hour:
            end_time = current_time + timedelta(hours=duration)
            events_in_block = [event for event in self.events if current_time <= event.datetime < end_time]

            self.time_blocks.append({
                "start": current_time,
                "end": end_time,
                "events": events_in_block
            })

            current_time += timedelta(hours=duration)
    def get_free_time_blocks(self):
        # Returnerer en liste med tidsblokker hvor det ikke er noen hendelser planlagt
        return [block for block in self.time_blocks if not block["events"]]

    def calculate_rowspan(self, event):
        # Anta at tidsblokker varer i en time og starter hver hele time
        event_start = event.datetime
        event_end = event.datetimeEnd or event_start + timedelta(hours=1)  # Anta en default varighet hvis ikke oppgitt

        # Finn startblokken for eventet
        start_block_index = None
        for i, block in enumerate(self.time_blocks):
            if block['start'].time() <= event_start.time() < block['end'].time():
                start_block_index = i
                break

        # Hvis vi ikke finner en startblokk, returner 1 som standard (skal ikke skje hvis dataene er korrekte)
        if start_block_index is None:
            return 1

        # Beregn antall tidsblokker eventet varer ved å sammenligne event_start og event_end med blokkene
        rowspan = 1
        for block in self.time_blocks[start_block_index + 1:]:
            if block['start'].time() < event_end.time():
                rowspan += 1
            else:
                break

        return rowspan

    def generate_time_blocks_with_rowspan(self, time_blocks_duration=60):
        """
        Genererer tidsblokker og kalkulerer rowspan for hvert event.
        time_blocks_duration: Varigheten av hver tidsblokk i minutter.
        """
        self.time_blocks = []
        start_time = datetime.combine(self.date, time(8, 0))  # Anta start kl 08:00
        end_time = datetime.combine(self.date, time(15, 0))  # Anta slutt kl 15:00
        current_time = start_time

        while current_time < end_time:
            block_end_time = current_time + timedelta(minutes=time_blocks_duration)
            events_in_block = [event for event in self.events if
                               event.datetime >= current_time and event.datetime < block_end_time]

            for event in events_in_block:
                event_duration = (event.datetimeEnd - event.datetime).total_seconds() / 60
                event.rowspan = int(event_duration // time_blocks_duration)

            self.time_blocks.append({
                "start": current_time,
                "end": block_end_time,
                "events": events_in_block
            })

            current_time = block_end_time


