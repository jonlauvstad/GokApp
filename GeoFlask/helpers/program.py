import datetime

class Program:

    count = 0

    def __init__(self, code, name, points, level, NUS_code, program_implementation_table):
        Program.count += 1
        self.id = Program.count
        self.code = code
        self.name = name
        self.points = points
        self.level = level
        self.NUS_code = NUS_code
        self.program_implementation_table = program_implementation_table
        self.fields = {
            "id": lambda x: x.id,
            "code": lambda x: x.code,
            "name": lambda x: x.name,
            "points": lambda x: x.points,
            "level": lambda x: x.level,
            "NUS_code": lambda x: x.NUS_code,
            "implementations": lambda x: [item.serialze() for item in x.implementations()]
        }

    def implementations(self):
        return [item for item in self.program_implementation_table if item.program_id == self.id]

    def serialize_x_keys(self, keys):   # Se user.py og test.py for skrevet uten dict-comp!
        return {key: value(self) for (key, value) in self.fields.items() if key not in keys}

    def serialize(self):
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "points": self.points,
            "level": self.level,
            "NUS_code": self.NUS_code,
            "implementations": [item.serialize() for item in self.implementations()]
        }

    def serialize_x_impl(self):
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "points": self.points,
            "level": self.level,
            "NUS_code": self.NUS_code
        }

class ProgramImplementation:

    count = 0

    def __init__(self, program_id, program_table, startdate, enddate,
                 course_program_table, course_imp_table,
                 program_location_table, location_table,
                 teacher_program_table, student_program_table, user_table):   # locations/courses som egen tabell-registreringstabell = []
        ProgramImplementation.count += 1
        self.id = ProgramImplementation.count
        self.program_id = program_id
        self.startdate = datetime.datetime.strptime(startdate, "%d.%m.%y")
        self.enddate = datetime.datetime.strptime(enddate, "%d.%m.%y")
        self.semester = "V" if self.startdate.month < 7 else "H"
        self.end_semester = "V" if self.enddate.month < 7 else "H"
        self.year = self.startdate.year % 100
        self.end_year = self.enddate.year % 100
        self.program = [item for item in program_table if item.id == program_id][0]     # Utenfor tabellen
        self.code = f"{self.program.code}{self.semester}{self.year}"
        self.name = f"{self.program.name} {self.semester}{self.year}"
        self.course_program_table = course_program_table
        self.course_imp_table = course_imp_table
        self.program_location_table = program_location_table
        self.location_table = location_table
        self.teacher_program_table = teacher_program_table
        self.student_program_table = student_program_table
        self.user_table = user_table

        self.fields = {
            "id": lambda x: x.id,
            "code": lambda x: x.code,
            "name": lambda x: x.name,
            "program": lambda x: x.program.serialize_x_impl(),
            "startdate": lambda x: x.startdate.strftime("%d.%m.%y"),
            "enddate": lambda x: x.enddate.strftime("%d.%m.%y"),
            "semester": lambda x: x.semester,
            "end_semester": lambda x: x.end_semester,
            "year": lambda x: x.year,
            "end_year": lambda x: x.end_year,
            "locations": lambda x: [item.serialize() for item in x.locations()],
            "courses": lambda x: [item.serialize() for item in x.courses()],
            "students": lambda x: [item.serialize() for item in x.students()],
            "teachers": lambda x: [item.serialize() for item in x.teachers()]
        }

    def courses(self):      # Strictly: course_implementations!
        course_ids = [item.course_id for item in self.course_program_table if item.program_id == self.id]
        return [item for item in self.course_imp_table if item.id in course_ids]
        # return [item.course_id for item in self.course_program_table if item.program_id == self.id]

    def locations(self):
        location_ids = [item.location_id for item in self.program_location_table if item.program_id == self.id]
        return [item for item in self.location_table if item.id in location_ids]
        # return [item.location for item in self.program_location_table]

    def teachers(self):
        teacher_ids = [item.user_id for item in self.teacher_program_table if item.program_id == self.id]
        return [item for item in self.user_table if item.id in teacher_ids]

    def students(self):
        student_ids = [item.user_id for item in self.student_program_table if item.program_id == self.id]
        return [item for item in self.user_table if item.id in student_ids]

    def serialize_x_keys(self, keys):   # Se user.py og test.py for skrevet uten dict-comp!
        return {key: value(self) for (key, value) in self.fields.items() if key not in keys}

    def serialize(self):
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "program": self.program.serialize_x_impl(),
            "startdate": self.startdate.strftime("%d.%m.%y"),
            "enddate": self.enddate.strftime("%d.%m.%y"),
            "semester": self.semester,
            "end_semester": self.end_semester,
            "year": self.year,
            "end_year": self.end_year,
            "locations": [item.serialize_x_keys("programs") for item in self.locations()],
            # "courses": [item.serialize_x_programs() for item in self.courses()],     # Strictly: course_implementations!
            "courses": [item.serialize_x_keys(["programs"]) for item in self.courses()],
            "teachers": [item.serialize_x_keys(["teatcher_programs", "student_programs"]) for item in self.teachers()],
            "students": [item.serialize_x_keys(["teatcher_programs", "student_programs"]) for item in self.students()]
        }

    def serialize_x_courses(self):
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "program": self.program.serialize_x_impl(),
            "startdate": self.startdate.strftime("%d.%m.%y"),
            "enddate": self.enddate.strftime("%d.%m.%y"),
            "semester": self.semester,
            "end_semester": self.end_semester,
            "year": self.year,
            "end_year": self.end_year,
            "locations": [item.serialize() for item in self.locations()]
        }