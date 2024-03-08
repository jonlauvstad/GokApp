from dateutil import parser
import datetime

# Bør beskrives!
def consistent_lectures(partial_lectures):
    for i in range(len(partial_lectures)):
        for j in range (i+1, len(partial_lectures)):
            if partial_lectures[i]["wd"] == partial_lectures[j]["wd"]:
                if partial_lectures[j]["start_int"] < partial_lectures[i]["end_int"] and\
                        partial_lectures[j]["end_int"] > partial_lectures[i]["start_int"]:
                    return False
    return True

def make_multiple_lectures(courseImpId, firstDate, lastDate, partial_lectures, max_lectures=1000, max_time=10000):
    holidays = []
    first = parser.parse(firstDate)
    last = parser.parse(lastDate)
    lectures = []
    time = 0
    num_lectures = 0
    date = first
    while date <= last and time < max_time and num_lectures < max_lectures:
        if date not in holidays:
            for lec in partial_lectures:
                if date.weekday() == lec["wd"]:
                    lectures.append({
                        "CourseImplementationId": courseImpId,
                        "StartTime": (date + datetime.timedelta(hours=lec["start_int"])).isoformat(),
                        "EndTime": (date + datetime.timedelta(hours=lec["end_int"])).isoformat(),
                        "VenueIds": [int(lec["room"])] if lec["room"] != "" else []
                    })
                    time += lec["time"]
                    num_lectures += 1
        date += datetime.timedelta(days=1)
    return lectures


def format_datetime(value, format='%H:%M'):
    if value is None:
        return ""
    return value.strftime(format)
