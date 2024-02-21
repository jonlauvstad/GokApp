from flask import Flask, redirect, render_template, request, session
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
    # print("REQUEST:", request)

    if (request.method == "GET"):
        response = requests.get(url, verify=False, headers=headers)
        # Håndtere response.ok
    else:
        to_do = request.form.get("to_do")
        if to_do == "DELETE":
            to_do = "SLETTET "
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
            print("DATA:", data)
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
                                as_dic['teacherNames'], as_dic['venueNames'], as_dic['venueIds'])

        return render_template("lecture.html", lecture=lecture, user=user, to_do=to_do)
    msg = f"Statuskode: {response.status_code}"
    return render_template("error.html", user=user, msg=msg, status=int(response.status_code))

def lecture_id_post_function(id):
    pass