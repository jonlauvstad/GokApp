from flask import Flask, redirect, render_template, request, session
from ..config import configuration
import requests
from ..assignment import Assignment

URLpre = configuration["URLpre"]


def assignment_id_function(id):
    user = session["user"]
    id = int(id)
    url_ext = f"Assignment/{id}"
    url = URLpre + url_ext

    headers = {"Authorization": f"Bearer {session['token']}"}
    response = requests.get(url, verify=False, headers=headers)
    if response.ok:
        as_dic = response.json()
        assignment = Assignment(as_dic['id'], as_dic['name'], as_dic['description'], as_dic['deadline'], as_dic['courseImplementationId'],
                                as_dic['courseImplementationCode'], as_dic['courseImplementationName'], as_dic['courseImplementationLink'],
                                as_dic['link'])
        return render_template("assignment.html", assignment=assignment, user=user)
    msg = f"Statuskode: {response.status_code}"
    return render_template("error.html", user=user, msg=msg, status=int(response.status_code))
