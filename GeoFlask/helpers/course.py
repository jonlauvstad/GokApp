import datetime

class Course:

    count = 0

    def __init__(self, code, name, points, category, teach_course, diploma_course, exam_course, course_implementation_table):
        Course.count += 1
        self.id = Course.count
        self.code = code
        self.name = name
        self.points = points
        self.category = category
        self.teach_course = teach_course
        self.diploma_course = diploma_course
        self.exam_course = exam_course
        self.course_implementation_table = course_implementation_table

    def implementations(self):
        return [item for item in self.course_implementation_table if item.course_id == self.id]

    def serialize(self):
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "points": self.points,
            "category": self.category,
            "teach_course": self.teach_course,
            "diploma_course": self.diploma_course,
            "exam_course": self.exam_course,
            "implementations": [item.serialize() for item in self.implementations()]
        }

    def serialize_x_impl(self):
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "points": self.points,
            "category": self.category,
            "teach_course": self.teach_course,
            "diploma_course": self.diploma_course,
            "exam_course": self.exam_course
        }

class CourseImplementation:
    count = 0

    def __init__(self, course_id, course_table, startdate, enddate, course_program_table):
        CourseImplementation.count += 1
        self.id = CourseImplementation.count
        self.startdate = datetime.datetime.strptime(startdate, "%d.%m.%y")
        self.enddate = datetime.datetime.strptime(enddate, "%d.%m.%y")
        self.semester = "V" if self.startdate.month < 7 else "H"
        self.end_semester = "V" if self.enddate.month < 7 else "H"
        self.year = self.startdate.year % 100
        self.end_year = self.enddate.year % 100
        self.course = [item for item in course_table if item.id == course_id][0]  # Utenfor tabellen
        self.code = f"{self.course.code}{self.semester}{self.year}"
        self.name = f"{self.course.name} {self.semester}{self.year}"
        self.course_program_table = course_program_table
        self.locations = []

    def programs(self):     # Strictly program_implementations!
        return [item for item in self.course_program_table if item.course_impl_id == self.id]

    def serialize(self):
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "course": self.course.serialize_x_impl(),
            "startdate": self.startdate.strftime("%d.%m.%y"),
            "enddate": self.enddate.strftime("%d.%m.%y"),
            "semester": self.semester,
            "end_semester": self.end_semester,
            "year": self.year,
            "end_year": self.end_year,
            "programs": [item.serialize() for item in self.programs()],     # Strictly program_implementations!
            "locations": [item.serialize() for item in self.locations]
        }

    def serialize_x_programs(self):
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "course": self.course.serialize_x_impl(),
            "startdate": self.startdate.strftime("%d.%m.%y"),
            "enddate": self.enddate.strftime("%d.%m.%y"),
            "semester": self.semester,
            "end_semester": self.end_semester,
            "year": self.year,
            "end_year": self.end_year,
            "locations": [item.serialize() for item in self.locations]
        }