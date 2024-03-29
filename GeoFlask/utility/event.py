from dateutil import parser

class Event:
    def __init__(self, time, underlyingId, type, typeEng, courseImplementationId, courseImpCode, courseImpName, courseImplementationLink, link, timeEnd,
                 venueId=0, venueName="", venueCapacity=0):
        self.time = time
        self.underlyingId = underlyingId
        self.type = type
        self.typeEng = typeEng
        self.courseImplementationId = courseImplementationId
        self.courseImpCode = courseImpCode
        self.courseImpName = courseImpName
        self.courseImplementationLink = courseImplementationLink
        self.datetime = parser.parse(time)
        self.date = self.datetime.date()
        self.strftime = self.datetime.strftime("%H:%M")
        self.link = link
        self.timeEnd = timeEnd
        self.venueId = venueId
        self.venueName = venueName
        self.venueCapacity = venueCapacity

