from dateutil import parser

class Lecture:
    def __init__(self, id, courseImplementationId, theme, description, startTime, endTime, courseImplementationLink, link, duration,
                 courseImplementationName, courseImplementationCode, teacherNames, venueNames, venueIds, teacherUserIds,
                 programTeacherUserIds):
        self.id = id
        self.courseImplementationId = courseImplementationId
        self.theme = theme
        self.description = description
        self.startTime = startTime
        self.endTime = endTime
        self.courseImplementationLink = courseImplementationLink
        self.link = link
        self.duration = duration
        self.courseImplementationName = courseImplementationName
        self.courseImplementationCode = courseImplementationCode
        self.start_datetime = parser.parse(startTime)
        self.end_datetime = parser.parse(endTime)
        self.start_string = self.start_datetime.strftime("%d.%b %H:%M")
        self.end_string = self.end_datetime.strftime("%d.%b %H:%M")
        self.teacherNames = teacherNames
        self.venueNames = venueNames
        self.venueId = None if len(venueIds) == 0 else venueIds[0]
        self.teacherUserIds = teacherUserIds
        self.programTeacherUserIds = programTeacherUserIds

