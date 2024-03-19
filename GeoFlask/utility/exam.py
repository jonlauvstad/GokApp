from dateutil import parser

class Exam:
    def __init__(self, id, courseImplementationId, category, duration_hours, periodStart, periodEnd,
                courseImplementationCode, courseImplementationName,
                examImplementationIds, ExamResultIds,
                link, courseImplementationLink):
        self.id = id
        self.courseImplementationId = courseImplementationId
        self.category = category
        self.duration_hours = duration_hours
        self.periodStart = periodStart
        self.periodEnd = periodEnd
        self.courseImplementationCode = courseImplementationCode
        self.courseImplementationName = courseImplementationName
        self.examImplementationIds = examImplementationIds
        self.ExamResultIds = ExamResultIds
        self.link = link
        self.courseImplementationLink = courseImplementationLink
        self.periodStart_datetime = parser.parse(periodStart)
        self.periodEnd_datetime = parser.parse(periodEnd)
        self.periodStart_string = self.periodStart_datetime.strftime("%d.%b %H:%M")
        self.periodEnd_string = self.periodEnd_datetime.strftime("%d.%b %H:%M")
        self.periodStart_iso = self.periodStart_datetime.isoformat()
        self.periodEnd_iso =  self.periodEnd_datetime.isoformat()
        self.hours = int(duration_hours)
        self.minutes = int(60 * (duration_hours - self.hours))

    def serialize(self):
        return {
            "id": self.id,
            "courseImplementationId": self.courseImplementationId,
            "category": self.category,
            "durationHours": self.duration_hours,
            "periodStart": self.periodStart_datetime,
            "periodEnd": self.periodEnd_datetime,
            "link": self.link,
            "courseImplementationLink": self.courseImplementationLink,
            "hours": self.hours,
            "minutes": self.minutes
        }