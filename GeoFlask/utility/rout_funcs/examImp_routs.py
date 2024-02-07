from flask import Flask, redirect, render_template, request, session
from ..config import configuration
import requests
from ..examImplementation import ExamImplementation

URLpre = configuration["URLpre"]


def examImplementation_id_function(id):
    user = session["user"]
    id = int(id)
    url_ext = f"ExamImplementation/{id}"
    url = URLpre + url_ext

    headers = {"Authorization": f"Bearer {session['token']}"}
    response = requests.get(url, verify=False, headers=headers)
    if response.ok:
        as_dic = response.json()
        examImp = ExamImplementation(as_dic['id'], as_dic['examId'], as_dic['venueId'], as_dic['startTime'],
                                as_dic['endTime'], as_dic['category'], as_dic['durationHours'], as_dic['courseImplementationId'],
                                as_dic['courseImplementationName'], as_dic['courseImplementationCode'], as_dic['venueName'],
                                 as_dic['location'], as_dic['courseImplementationLink'], as_dic['venueLink'], as_dic['link'])

        return render_template("examImplementation.html", examImp=examImp, user=user)
    msg = f"Statuskode: {response.status_code}"
    return render_template("error.html", user=user, msg=msg, status=int(response.status_code))