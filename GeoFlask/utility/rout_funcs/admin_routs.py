import datetime
from dateutil import parser

from flask import Flask, redirect, render_template, request, session
from ..config import configuration
from ..lectureBooking import LectureBooking

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

def add_lecture_one_function():
    user = session["user"]

    url_ext = f"courseImplementation"
    url = URLpre + url_ext
    now = datetime.datetime.now().isoformat()
    url += f"?endDate={now}&userRole=Balle"

    headers = {"Authorization": f"Bearer {session['token']}"}
    response = requests.get(url, verify=False, headers=headers)
    if response.ok:
        as_lOfdics = response.json()
        # as_lOfdics = response.text

        url_ext2 = "venue"
        url2 = URLpre + url_ext2
        response2 = requests.get(url2, verify=False, headers=headers)
        if response2.ok:
            as_lOfDicts_2 = response2.json()

            return render_template("admin/lecture/add_lecture_one.html", user=user, courseImps=as_lOfdics, venues=as_lOfDicts_2)

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

    data = {
        "CourseImplementationId": courseId,
        "Theme": theme,
        "Description": description,
        "StartTime": parser.parse(start).isoformat(),
        "EndTime": end,
        "VenueIds":  [venueId]      #json.dumps([venueId])
    }
    # for key in data:
    #     print(f"{key}: {data[key]}")
    # now = datetime.datetime.now().isoformat()
    # print(now)


    url_ext = f"lecture"
    url = URLpre + url_ext
    headers = {"Authorization": f"Bearer {session['token']}"}

    response = requests.post(url, verify=False, headers=headers, json=data)
    if response.ok:
        dic = response.json()
        print("SUCCESS:", dic['success'])
        lectBook = \
            LectureBooking(dic['lectureId'], dic['courseImplementationCode'],dic['numStudents'], dic['venueCapacity'], dic['venueName'],
                           dic['links'], dic['success'], dic['message'], dic['startTime'], dic['endTime'], dic['room'], dic['roomString'],
                           dic['lectureLink'])
    # lectBook = LectureBooking(20, 50, 90, "Fjorden", {"NewLecture": ""}, "true", "Vellykket osv")
        return render_template("admin/lecture/conf_lecture_one.html", user=user, lectBook=lectBook)

    # print(response.text, response.headers)
    msg = f"Statuskode: {response.status_code}"
    return render_template("error.html", user=user, msg=msg, status=int(response.status_code))