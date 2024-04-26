from dateutil import parser
from datetime import datetime
from typing import Optional

class Assignment:
    def __init__(self, id, name, description, deadline, courseImplementationId, courseImplementationCode, courseImplementationName,
                 courseImplementationLink, link):
        self.id = id
        self.name = name
        self.description = description
        self.courseImplementationId = courseImplementationId
        self.courseImplementationCode = courseImplementationCode
        self.courseImplementationName = courseImplementationName
        self.courseImplementationLink = courseImplementationLink
        self.link = link

        self.datetime: Optional[datetime] = None
        self.datetime_string: str = "No deadline provided or invalid format"
        self.datetime_local_format: str = ""  # Suitable for datetime-local input

        if isinstance(deadline, str):
            try:
                self.datetime = parser.parse(deadline)
                self.datetime_string = self.datetime.strftime("%d.%b %Y %H:%M")
                self.datetime_local_format = self.datetime.strftime("%Y-%m-%dT%H:%M")  # Proper format for datetime-local
            except ValueError:
                self.datetime_string = "Invalid date"
                self.datetime_local_format = ""  # Ensure this is empty if parsing fails


"""class Assignment:
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
        self.link = link"""
