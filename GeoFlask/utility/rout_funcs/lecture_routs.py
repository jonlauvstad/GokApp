from flask import Flask, redirect, render_template, request, session
from ..config import configuration
import requests
from ..lecture import Lecture

URLpre = configuration["URLpre"]


def lecture_id_function(id):
    user = session["user"]
    id = int(id)
    url_ext = f"Lecture/{id}"
    url = URLpre + url_ext

    headers = {"Authorization": f"Bearer {session['token']}"}
    response = requests.get(url, verify=False, headers=headers)
    if response.ok:
        as_dic = response.json()
        lecture = Lecture(as_dic['id'], as_dic['courseImplementationId'], as_dic['theme'], as_dic['description'],
                                as_dic['startTime'], as_dic['endTime'], as_dic['courseImplementationLink'],
                                as_dic['link'], as_dic['duration'], as_dic['courseImplementationName'], as_dic['courseImplementationCode'],
                                as_dic['teacherNames'], as_dic['venueNames'])

        return render_template("lecture.html", lecture=lecture, user=user)
    msg = f"Statuskode: {response.status_code}"
    return render_template("error.html", user=user, msg=msg, status=int(response.status_code))

def lecture_id_post_function(id):
    pass