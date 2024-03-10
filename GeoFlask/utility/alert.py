from dateutil import parser

class Alert:
    def __init__(self, id, userId, message, time, seen, links):
        self.id = id
        self.userId = userId
        self.message = message
        self.time = time
        self.seen = seen
        self.links = links
        self.datetime = parser.parse(time)
        self.time_string = self.datetime.strftime("%d.%b %H:%M")
        self.links_list = [] if "slettet" in message else self.links.split(',')

    def __str__(self):
        return f"Alert time:{self.time_string} message:{self.message} seen:{self.seen} links:{self.links_list}"