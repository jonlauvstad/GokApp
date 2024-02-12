import datetime

from flask import Flask, redirect, render_template, request, session
from ..config import configuration

import requests

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
    url += f"?endDate={now}"

    headers = {"Authorization": f"Bearer {session['token']}"}
    response = requests.get(url, verify=False, headers=headers)
    if response.ok:
        as_lOfdics = response.json()
        # as_lOfdics = response.text

        return render_template("admin/lecture/add_lecture_one.html", user=user, courseImps=as_lOfdics)
    msg = f"Statuskode: {response.status_code}"
    return render_template("error.html", user=user, msg=msg, status=int(response.status_code))
