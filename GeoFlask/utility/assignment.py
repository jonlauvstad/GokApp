from dateutil import parser

class Assignment:
    def __init__(self, id, name, description, deadline, courseImplementationId, courseImplementationCode, courseImplementationName,
                 courseImplementationLink, link):
        self.id = id
        self.name = name
        self.description = description
        self.deadline = deadline
        self.courseImplementationId = courseImplementationId
        self.courseImplementationCode = courseImplementationCode
        self.courseImplementationName = courseImplementationName
        self.courseImplementationLink = courseImplementationLink
        self.datetime = parser.parse(deadline)
        self.datetime_string = self.datetime.strftime("%d.%b %H:%M")
        self.link = link