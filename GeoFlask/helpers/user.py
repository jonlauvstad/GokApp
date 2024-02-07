class User:

    count = 0

    def __init__(self, gokstad_email, first_name, last_name, role, salt, hashed_pw,
                 attendance_table, lecture_table,
                 student_program_table, teacher_program_table, program_table,
                 teacher_course_table, course_table,
                 email2=None, email3=None):
        User.count += 1
        self.id = User.count
        self.gokstad_email = gokstad_email
        self.first_name = first_name
        self.last_name = last_name
        self.email2 = email2
        self.email3 = email3
        self.role = role
        self.salt = salt
        self.hashed_pw = hashed_pw
        self.attendance_table = attendance_table
        self.lecture_table = lecture_table
        self.student_program_table = student_program_table
        self.teacher_program_table = teacher_program_table
        self.program_table = program_table
        self.teacher_course_table = teacher_course_table
        self.course_table = course_table
        self.fields = {
            "gokstad_email": lambda x: x.gokstad_email,
            "id": lambda x: x.id,
            "first_name": lambda x: x.first_name,
            "last_name": lambda x: x.last_name,
            "email2": lambda x: x.email2,
            "email3": lambda x: x.email3,
            "role": lambda x: x.role,
            "attendances": lambda x: [item.serialize() for item in x.attendances()],
            "student_programs": lambda x: [item.serialize_x_keys(["students", "teachers"]) for item in x.student_programs()],
            "teacher_programs": lambda x: [item.serialize() for item in x.teacher_programs()],
            "teacher_courses": lambda x: [item.serialize() for item in x.teacher_courses()]
        }

    def attendances(self):
        lecture_ids = [item.lecture_id for item in self.attendance_table if item.user_id == self.id]
        return [item for item in self.lecture_table if item.id in lecture_ids]

    def student_programs(self):
        program_ids = [item.program_id for item in self.student_program_table if item.user_id == self.id]
        return [item for item in self.program_table if item.id in program_ids]

    def teacher_programs(self):
        program_ids = [item.program_id for item in self.teacher_program_table if item.user_id == self.id]
        return [item for item in self.program_table if item.id in program_ids]

    def teacher_courses(self):
        course_ids = [item.course_id for item in self.teacher_course_table if item.user_id == self.id]
        return [item for item in self.course_table if item.id in course_ids]

    def serialize(self):
        return {
            "gokstad_email": self.gokstad_email,
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email2": self.email2,
            "email3": self.email3,
            "role": self.role,
            # "salt": self.salt,
            # "hashed_pw": self.hashed_pw,
            "attendances": [item.serialize_x_keys(["students"]) for item in self.attendances()],
            "student_programs": [item.serialize_x_keys(["students"]) for item in self.student_programs()],
            "teacher_programs": [item.serialize_x_keys(["teachers"]) for item in self.teacher_programs()],
            "teacher_courses": [item.serialize_x_keys(["teachers"]) for item in self.teacher_courses()]
        }

    def serialize_x_keys(self, keys):
        dic = {}
        for field in self.fields:
            if field not in keys:
                dic[field] = self.fields[field](self)
        return dic

# u = User("jon.lauvstad@gokstad.com", first_name="Jon", last_name="Andersen", salt="s", hashed_pw="pw")
# u_s = u.serialize_x_keys([])
# u_s_xt = u.serialize_x_keys(["teacher_programs", "teacher_courses"])
# print(u_s)
# print(u_s_xt)