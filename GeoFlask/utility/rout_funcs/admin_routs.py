import datetime
from dateutil import parser

from flask import Flask, redirect, render_template, request, session, abort
from ..config import configuration
from ..event import Event
from ..event_day import EventDay
from ..lectureBooking import LectureBooking
from ..lecture import Lecture
from ..prefill import Prefill


import requests
import json


URLpre = configuration["URLpre"]

def admin_function():
    user = session["user"]
    return render_template("admin/admin.html", user=user)


def admin_lecture_function():
    user = session["user"]
    return render_template("admin/lecture/a_lecture.html", user=user)


def add_lecture_function():
    user = session["user"]
    return render_template("admin/lecture/add_lecture.html", user=user)


def add_lecture_one_function(put=None, prefill=None):
    user = session["user"]

    if prefill:
        prefill = prefill.serialize()
        print("PREFILL\n", prefill)

    url_ext = f"courseImplementation"
    url = URLpre + url_ext
    now = datetime.datetime.now().isoformat()
    url += f"?endDate={now}&userRole=Balle"

    headers = {"Authorization": f"Bearer {session['token']}"}
    response = requests.get(url, verify=False, headers=headers)
    if response.ok:
        as_lOfdics = response.json()

        url_ext2 = "venue"
        url2 = URLpre + url_ext2
        response2 = requests.get(url2, verify=False, headers=headers)
        if response2.ok:
            as_lOfDicts_2 = response2.json()
            if not put:
                return render_template("admin/lecture/add_lecture_one.html", user=user, courseImps=as_lOfdics, venues=as_lOfDicts_2,
                                       prefill=prefill)

            # Make Api call to get the lecture to fill in values
            put_ext = f"lecture/{put}"
            url_put = URLpre + put_ext
            response = requests.get(url_put, verify=False, headers=headers)
            if response.ok:
                as_dic = response.json()
                lecture = Lecture(as_dic['id'], as_dic['courseImplementationId'], as_dic['theme'],
                                  as_dic['description'],
                                  as_dic['startTime'], as_dic['endTime'], as_dic['courseImplementationLink'],
                                  as_dic['link'], as_dic['duration'], as_dic['courseImplementationName'],
                                  as_dic['courseImplementationCode'],
                                  as_dic['teacherNames'], as_dic['venueNames'], as_dic['venueIds'], as_dic['teacherUserIds'],
                                as_dic['programTeacherUserIds'])
                return render_template("admin/lecture/add_lecture_one.html", user=user, courseImps=as_lOfdics, venues=as_lOfDicts_2,
                                       put=put, lecture=lecture, prefill=prefill)
            # Håndtere response.ok

    msg = f"Statuskode: {response.status_code if not response.ok else response2.status_code}"
    return render_template("error.html", user=user, msg=msg, status=int(response.status_code))

def conf_lecture_one_function():
    user = session["user"]

    courseId = request.form.get("courseId")
    theme = request.form.get("theme")
    description = request.form.get("description")
    start = request.form.get("start")
    end = request.form.get("end")
    venueId = request.form.get("venueId")

    des = description.replace(" ", "")
    if des == "\r\n":
        description = ""
    else:
        description = description.replace("\r\n", " ")

    data = {
        "CourseImplementationId": courseId,
        "Theme": theme,
        "Description": description,
        "StartTime": parser.parse(start).isoformat(),
        "EndTime": end,
        "VenueIds":  [venueId]      #json.dumps([venueId])
    }

    url_ext = f"lecture"
    url = URLpre + url_ext
    headers = {"Authorization": f"Bearer {session['token']}"}

    response = requests.post(url, verify=False, headers=headers, json=data)
    if response.ok:
        dic = response.json()
        lectBook = \
            LectureBooking(dic['lectureId'], dic['courseImplementationCode'],dic['numStudents'], dic['venueCapacity'], dic['venueName'],
                           dic['links'], dic['success'], dic['message'], dic['startTime'], dic['endTime'], dic['room'], dic['roomString'],
                           dic['lectureLink'])

        return render_template("admin/lecture/conf_lecture_one.html", user=user, lectBook=lectBook)

    msg = f"Statuskode: {response.status_code}"
    return render_template("error.html", user=user, msg=msg, status=int(response.status_code))


def search_lecture_function():
    user = session["user"]
    headers = {"Authorization": f"Bearer {session['token']}"}

    # CourseImplementation-context:
    url_ext_course = "CourseImplementation"
    url_course = URLpre + url_ext_course
    now = datetime.datetime.now().isoformat()
    response = requests.get(url_course, verify=False, headers=headers, params={"endDate": now})   # "startDate": now
    if not response.ok:
        msg = f"Statuskode: {response.status_code}"
        return render_template("error.html", user=user, msg=msg, status=int(response.status_code))
    courseImps = response.json()
    courseImps.sort(key=lambda x: x['id'])

    # Venue-context:
    url_ext_venue = "Venue"
    url_venue = URLpre + url_ext_venue
    response = requests.get(url_venue, verify=False, headers=headers)
    if not response.ok:
        msg = f"Statuskode: {response.status_code}"
        return render_template("error.html", user=user, msg=msg, status=int(response.status_code))
    venues = response.json()

    # Teacher-context:
    url_ext_teacher = "User"
    url_teacher = URLpre + url_ext_teacher
    response = requests.get(url_teacher, verify=False, headers=headers, params={"role": "teacher"})
    if not response.ok:
        msg = f"Statuskode: {response.status_code}"
        return render_template("error.html", user=user, msg=msg, status=int(response.status_code))
    users = response.json()

    return render_template("admin/lecture/search_lecture.html", user=user, courseImps=courseImps, venues=venues, users=users)

