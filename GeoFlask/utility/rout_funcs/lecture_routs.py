from flask import Flask, redirect, render_template, request, session, abort
from ..config import configuration
from ..global_vars import weekdays
import requests
from ..lecture import Lecture
from . import admin_routs
from dateutil import parser
import datetime
from ..util_funcs import *

URLpre = configuration["URLpre"]


def lecture_id_function(id):
    user = session["user"]
    id = int(id)
    url_ext = f"Lecture/{id}"
    url = URLpre + url_ext

    headers = {"Authorization": f"Bearer {session['token']}"}
    to_do = None

    deleted = False

    if (request.method == "GET"):
        response = requests.get(url, verify=False, headers=headers)
        # Håndtere response.ok
    else:
        to_do = request.form.get("to_do")
        if to_do == "DELETE":
            to_do = "SLETTET "
            deleted = True
            response = requests.delete(url, verify=False, headers=headers)
            # Håndtere response.ok
        elif to_do == "PUT_EXECUTE":
            to_do = "ENDRET "
            courseId = request.form.get("courseId")
            theme = request.form.get("theme")
            description = request.form.get("description")
            start = request.form.get("start")
            end = request.form.get("end")
            venueId = request.form.get("venueId")

            data = {
                "Id": id,
                "CourseImplementationId": courseId,
                "Theme": theme,
                "Description": description,
                "StartTime": parser.parse(start).isoformat(),
                "EndTime": end,
                "VenueIds": [venueId]  # json.dumps([venueId])
            }

            response = requests.put(url, verify=False, headers=headers, json=data)
            # Håndtere response.ok
        else:
            # SKAL NÅ CALLLE add_lecture_one_function()
            return admin_routs.add_lecture_one_function(put=id)    # put=int(to_do)

    if response.ok:
        as_dic = response.json()
        lecture = Lecture(as_dic['id'], as_dic['courseImplementationId'], as_dic['theme'], as_dic['description'],
                                as_dic['startTime'], as_dic['endTime'], as_dic['courseImplementationLink'],
                                as_dic['link'], as_dic['duration'], as_dic['courseImplementationName'], as_dic['courseImplementationCode'],
                                as_dic['teacherNames'], as_dic['venueNames'], as_dic['venueIds'], as_dic['teacherUserIds'],
                                as_dic['programTeacherUserIds'])

        if deleted:
            showUpdateDeleteButtons = False
        else:
            if user.role == "admin" or int(user.id) in lecture.teacherUserIds or int(user.id) in lecture.programTeacherUserIds:
                showUpdateDeleteButtons = True
            else:
                showUpdateDeleteButtons = False

        return render_template("lecture.html", lecture=lecture, user=user, to_do=to_do, showButtons=showUpdateDeleteButtons)

    abort(404, f"Vi kunne ikke finne forelesning med id {id}\n"
               "Standardmelding:\n"
               "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.\n"
               "not_sorry")
    # msg = f"Statuskode: {response.status_code}"
    # return render_template("error.html", user=user, msg=msg, status=int(response.status_code))

def lecture_search_result_function():
    user = session['user']

    startAfter = None if request.form.get("startAfter") == "" else request.form.get("startAfter")
    endBy = None if request.form.get("endBy") == "" else request.form.get("endBy")
    courseImpId = None if request.form.get("courseImpId") == "" else request.form.get("courseImpId")
    venueId = None if request.form.get("venueId") == "" else request.form.get("venueId")
    teacherId = None if request.form.get("teacherId") == "" else request.form.get("teacherId")

    params = {}
    if startAfter:
        params['startAfter'] = startAfter
    if endBy:
        params['endBy'] = endBy
    if courseImpId:
        params['courseImpId'] = courseImpId
    if venueId:
        params['venueId'] = venueId
    if teacherId:
        params['teacherId'] = teacherId

    headers = {"Authorization": f"Bearer {session['token']}"}
    url_ext = f"Lecture"
    url = URLpre + url_ext
    response = requests.get(url, verify=False, headers=headers, params=params)
    if not response.ok:
        abort(int(response.status_code))

    lectures = response.json()

    lectures = [
        Lecture(as_dic['id'], as_dic['courseImplementationId'], as_dic['theme'], as_dic['description'],
                as_dic['startTime'], as_dic['endTime'], as_dic['courseImplementationLink'],
                as_dic['link'], as_dic['duration'], as_dic['courseImplementationName'],
                as_dic['courseImplementationCode'],
                as_dic['teacherNames'], as_dic['venueNames'], as_dic['venueIds'], as_dic['teacherUserIds'],
                as_dic['programTeacherUserIds'])
        for as_dic in lectures
    ]
    found_none = len(lectures) == 0

    return render_template("admin/lecture/search_result_lecture.html", user=user, lectures=lectures, found_none=found_none)

def lecture_multiple_function():
    user = session['user']
    params = {"id_string": request.args.get("ids")}

    headers = {"Authorization": f"Bearer {session['token']}"}
    url_ext = f"Lecture"
    url = URLpre + url_ext

    deleted = True
    added = False

    # NYTT FOR ADD_MULTIPLE
    if request.method == "POST":
        courseImpId = int(request.form.get("courseImpId"))
        firstDate = request.form.get("firstDate")
        lastDate = request.form.get("lastDate")
        max_lectures = int(request.form.get("maxLectures"))
        max_time = int(request.form.get("maxTime"))

        weekdays = request.form.getlist("weekday")
        starts = request.form.getlist("start")
        hours = request.form.getlist("hours")
        minutes = request.form.getlist("minutes")
        rooms = request.form.getlist("room")

        partial_lectures = [
            {
                "wd": int(weekdays[i]),
                "start_int": int(starts[i].split(":")[0]) + int(starts[i].split(":")[1])/60,
                "time": int(hours[i]) + int(minutes[i])/60,
                "end_int": int(starts[i].split(":")[0]) + int(starts[i].split(":")[1])/60 + int(hours[i]) + int(minutes[i])/60,
                "room": rooms[i]
            }
            for i in range(len(starts))
        ]
        no_overlap = consistent_lectures(partial_lectures)
        if not no_overlap:
            return lecture_add_multiple_function(err_msg="Forelesningene du prøver å legge inn overlapper!")

        add_lectures = make_multiple_lectures(courseImpId, firstDate, lastDate, partial_lectures, max_lectures=max_lectures, max_time=max_time)

        deleted = False
        added = True
        url += "/multiple"
        response = requests.post(url, verify=False, headers=headers, json=add_lectures) # ikke data=add_lectures

        # Velger å re-rendre siden med en melding dersom response not ok, som med no_overlap
        if not response.ok:
            e_msg = "Kunne ikke legge inn forelesningene. Sannsynligvis er læreren eller lokalet opptatt, eller det er" \
                    " noe inkonsistent i dataene du la inn"
            return lecture_add_multiple_function(err_msg=e_msg)

    # FRA FØR - RESTEN!
    if request.method == "GET":
        response = requests.delete(url, verify=False, headers=headers, params=params)

    if not response.ok:
        abort(int(response.status_code))

    lectures = response.json()
    lectures = [
        Lecture(as_dic['id'], as_dic['courseImplementationId'], as_dic['theme'], as_dic['description'],
                as_dic['startTime'], as_dic['endTime'], as_dic['courseImplementationLink'],
                as_dic['link'], as_dic['duration'], as_dic['courseImplementationName'],
                as_dic['courseImplementationCode'],
                as_dic['teacherNames'], as_dic['venueNames'], as_dic['venueIds'], as_dic['teacherUserIds'],
                as_dic['programTeacherUserIds'])
        for as_dic in lectures
    ]
    return render_template("admin/lecture/search_result_lecture.html", user=user, lectures=lectures, deleted=deleted, added=added)

def lecture_add_multiple_function(err_msg=None):
    user = session['user']

    headers = {"Authorization": f"Bearer {session['token']}"}

    # CourseImplementation-context:
    url_ext_course = "CourseImplementation"
    url_course = URLpre + url_ext_course
    now = datetime.datetime.now().isoformat()
    url_course += f"?endDate={now}&userRole=Balle"
    response = requests.get(url_course, verify=False, headers=headers)
    if not response.ok:
        msg = f"Statuskode: {response.status_code}"
        return render_template("error.html", user=user, msg=msg, status=int(response.status_code))
    courseImps = response.json()
    courseImps.sort(key=lambda x: x['name'])

    # Venue-context:
    url_ext_venue = "Venue"
    url_venue = URLpre + url_ext_venue
    response = requests.get(url_venue, verify=False, headers=headers)
    if not response.ok:
        msg = f"Statuskode: {response.status_code}"
        return render_template("error.html", user=user, msg=msg, status=int(response.status_code))
    venues = response.json()

    return render_template("admin/lecture/add_lecture_multiple.html", user=user, courseImps=courseImps, venues=venues,
                           weekdays=weekdays, err_msg=err_msg)