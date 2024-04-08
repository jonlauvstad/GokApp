from dateutil import parser

class ExamImplementation:
    def __init__(self, id, examId, venueId, startTime, endTime, category, durationHours, courseImplementationId,
                 courseImplementationName, courseImplementationCode, venueName, location,
                 courseImplementationLink, venueLink, link, examLink):
        self.id = id
        self.examId = examId
        self.venueId = venueId
        self.startTime = startTime
        self.endTime = endTime
        self.category = category
        self.durationHours = durationHours
        self.courseImplementationId = courseImplementationId
        self.courseImplementationName = courseImplementationName
        self.courseImplementationCode = courseImplementationCode
        self.venueName = venueName
        self.location = location
        self.courseImplementationLink = courseImplementationLink
        self.venueLink = venueLink
        self.link = link
        self.start_datetime = parser.parse(startTime)
        self.end_datetime = parser.parse(endTime)
        self.start_string = self.start_datetime.strftime("%d.%b %H:%M")
        self.end_string = self.end_datetime.strftime("%d.%b %H:%M")
        self.duration = f"{self.durationHours:.0f} timer" if durationHours % 1 == 0 else f"{self.durationHours:.2f} timer"
        self.examLink = examLink

class ExamImpReduced:
    def __init__(self, examId, venueId, startTime, endTime, userExamImplementation):
        self.id = id
        self.examId = examId
        self.venueId = venueId
        self.startTime = startTime
        self.endTime = endTime
        self.userExamImplementation = userExamImplementation