from program import Program, ProgramImplementation
from course import Course, CourseImplementation

def make_programs(program_implementation_table):
    return [
        Program("HS-BEP", "Backend-programmering", 120, "Toårig fagskolestudium", 554151, program_implementation_table),
        Program("HS-BEI", "Bærekraftig entrepenørskap og innovasjon", 120, "Toårig fagskolestudium", 541112, program_implementation_table),
        Program("HS-BEPN", "Backend-programmering", 120, "Toårig fagskolestudium", 554151, program_implementation_table),
        Program("HD-QA", "QA Programvaretesting", 120, "Toårig fagskolestudium", 554151, program_implementation_table)
    ]

def make_courses(course_implementation_table):
    return [
        Course("GRLP", "Grunnleggende programmering", 15, "course", True, True, True, course_implementation_table),
        Course("DBSQ", "Databaser og SQL", 15, "course", True, True, True, course_implementation_table),
        Course("OBJP", "Objektorientert programmering", 20, "course", True, True, True, course_implementation_table),
        Course("PRUM", "Programvareutviklingsmetoder", 10, "course", True, True, True, course_implementation_table),
        Course("AVAP", "Avansert programmering", 15, "course", True, True, True, course_implementation_table),
        Course("ALGO", "Algoritmiske metoder", 7.5, "course", True, True, True, course_implementation_table),
        Course("SOFD", "Software design", 7.5, "course", True, True, True, course_implementation_table),
        Course("CWAK", "Cloud-WebArkitektur-Container", 15, "course", True, True, True, course_implementation_table),
        Course("PROJ", "Prosjektoppgave", 15, "course", True, True, True, course_implementation_table)
    ]
    # (self, code, name, points, category, teach_course, diploma_course, exam_course)

def make_progImplementations(programs, course_program_table):
    return [
        ProgramImplementation(1, programs, "01.07.22", "30.06.24", course_program_table),     # Mangler course_program_table som siste argument
        ProgramImplementation(3, programs, "01.07.22", "30.06.24", course_program_table),
        ProgramImplementation(2, programs, "01.07.23", "30.06.25", course_program_table),
        ProgramImplementation(1, programs, "01.07.23", "30.06.25", course_program_table),
        ProgramImplementation(3, programs, "01.07.23", "30.06.25", course_program_table),
        ProgramImplementation(4, programs, "01.07.23", "30.06.25", course_program_table)
    ]

def make_courseImplementations(courses, course_program_table):
    return [
        CourseImplementation(1, courses, "01.07.22", "31.12.22", course_program_table)
    ]

    # (self, course_id, course_table, startdate, enddate, course_program_table)


# def programs_get_implementations(programs, implementations):
#     for prog in programs:
#         prog.implementations = [item for item in implementations if item.program_id == prog.id]