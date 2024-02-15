from dateutil import parser

class LectureBooking:
    def __init__(self, lectureId, courseImplementationCode, numStudents, venueCapacity, venueName, links, success, message,
                 startTime, endTime, room, roomString, lectureLink):
        self.lectureId = lectureId
        self.courseImplementationCode = courseImplementationCode
        self.numStudents = numStudents
        self.venueCapacity = venueCapacity
        self.venueName = venueName
        self.links = links
        self.success = success # True if success == "true" else False
        self.message = message # message.replace("<br>", "\n")
        self.startTime = parser.parse(startTime).strftime("%d.%b.%Y %H:%M")
        self.endTime = parser.parse(endTime).strftime("%d.%b.%Y %H:%M")
        self.room = room
        self.roomString = roomString
        self.lectureLink = lectureLink