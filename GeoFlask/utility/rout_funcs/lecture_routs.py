from flask import Flask, redirect, render_template, request, session, abort
from ..config import configuration
import requests
from ..lecture import Lecture
from . import admin_routs
from dateutil import parser

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

    return render_template("admin/lecture/search_result_lecture.html", user=user, lectures=lectures)

def lecture_multiple_function():
    id_string = request.args.get("ids");
    return id_string