# student_resources_routes.py
from flask import render_template, session
import requests
from ..config import configuration

URLpre = configuration["URLpre"]


def get_resources():
    user = session.get("user")
    token = session.get("token")
    if not user or not token:
        return render_template("error.html", message="You are not logged in.")

    headers = {"Authorization": f"Bearer {token}"}
    courseId = 1
    url = f"{URLpre}StudentResources/{courseId}"

    response = requests.get(url, headers=headers, verify=False)
    if response.ok:
        resources = response.json()
        return render_template("student_resources.html", resources=resources, user=user)
    else:
        msg = f"Status code: {response.status_code}"
        return render_template("error.html", user=user, msg=msg, status=response.status_code)
