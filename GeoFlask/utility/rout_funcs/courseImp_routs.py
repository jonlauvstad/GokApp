from flask import render_template, request, session, abort
from ..config import configuration
import requests
import datetime
from dateutil import parser

URLpre = configuration["URLpre"]

def courseImp_id_function(id):
    user = session["user"]
    id = int(id)

    url_ext = f"CourseImplementation/{id}"
    url = URLpre + url_ext
    headers = {"Authorization": f"Bearer {session['token']}"}
    response = requests.get(url, verify=False, headers=headers)

    if not response.ok:
        abort(404)

    dic = response.json()
    dic['startDate']  = parser.parse(dic['startDate'])
    dic['endDate'] = parser.parse(dic['endDate'])

    return render_template("courseImp.html", course_imp=dic, user=user)

def course_id_function(id):
    user = session["user"]
    id = int(id)

    url_ext = f"Course/{id}"
    url = URLpre + url_ext
    headers = {"Authorization": f"Bearer {session['token']}"}
    response = requests.get(url, verify=False, headers=headers)

    if not response.ok:
        abort(404)

    dic = response.json()
    return render_template("course.html", course=dic, user=user)