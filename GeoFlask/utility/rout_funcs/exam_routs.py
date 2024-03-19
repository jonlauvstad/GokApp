import datetime
from dateutil import parser
import requests
from flask import Flask, redirect, render_template, request, session, abort
from ..config import configuration
from ..exam import Exam

URLpre = configuration["URLpre"]


def admin_exam_function():
    user = session["user"]
    return render_template("admin/exam/exam_or_imp.html", user=user)


def template_exam_function(put=None, try_delete=None):
    user = session["user"]
    options = ["registrére", "endre", "slette"]

    exam = session.pop('exam', None) if put else None
    option = None
    if put:
        option = "slette" if try_delete else "endre"

    # Getting CourseImplementationIds:
    url_ext = f"courseImplementation"
    url = URLpre + url_ext
    now = datetime.datetime.now().isoformat()
    url += f"?endDate={now}&userRole=Balle"
    headers = {"Authorization": f"Bearer {session['token']}"}
    response = requests.get(url, verify=False, headers=headers)
    if not response.ok:
        abort(404)

    cis_lOfdics = response.json()

    error_msg = None
    if exam:
        if exam.courseImplementationId not in [item['id'] for item in cis_lOfdics]:
            error_msg = f"Du er ikke  autorisert til å {option} eksamen med id {exam.id}."
            exam = None
            put = None
            try_delete = None
            option = None

    return render_template("admin/exam/add_exam.html",
           user=user, options=options, courseImps=cis_lOfdics, put=put, exam=exam, try_delete=try_delete,
           categories=configuration["exam_categories"], option=option, error_msg=error_msg)


def conf_exam_function():
    user = session["user"]

    action = request.form.get("action")

    match action:
        case "endre":
            return template_exam_function(put=True)
        case "slette":
            return template_exam_function(put=True, try_delete=True)

    courseId = request.form.get("courseId")
    category = request.form.get("category")
    hours = int(request.form.get("hours"))
    minutes = int(request.form.get("minutes"))
    start = request.form.get("start")
    end = request.form.get("end")

    # Hvis vi kommer hit, er det en Add
    data = {
        "CourseImplementationId": courseId,
        "Category": category,
        "DurationHours": hours + minutes/60,
        "Start": parser.parse(start).isoformat(),
        "End": parser.parse(end).isoformat()
    }

    url_ext = f"exam"
    url = URLpre + url_ext
    headers = {"Authorization": f"Bearer {session['token']}"}

    response = requests.post(url, verify=False, headers=headers, json=data)
    if not response.ok:
        abort(404)
    dic = response.json()
    exam = Exam(dic['id'], dic['courseImplementationId'], dic['category'], dic['durationHours'], dic['periodStart'], dic['periodEnd'],
                dic['courseImplementationCode'], dic['courseImplementationName'],
                dic['examImplementationIds'], dic['examResultIds'],
                dic['link'], dic['courseImplementationLink'])
    return render_template("admin/exam/exam.html", user=user, exam=exam, headl_prefix="NY ")


def exam_id_function(id):
    user = session["user"]
    id = int(id)
    url_ext = f"exam/{id}"
    url = URLpre + url_ext
    headers = {"Authorization": f"Bearer {session['token']}"}
    headl_prefix = None

    if (request.method == "GET"):
        response = requests.get(url, verify=False, headers=headers)

    else:
        action = request.form.get("action")
        if action == "slette":
            headl_prefix = "SLETTET "
            response = requests.delete(url, verify=False, headers=headers)
        else:
            courseId = request.form.get("courseId")
            category = request.form.get("category")
            hours = int(request.form.get("hours"))
            minutes = int(request.form.get("minutes"))
            start = request.form.get("start")
            end = request.form.get("end")

            data = {
                "CourseImplementationId": courseId,
                "Category": category,
                "DurationHours": hours + minutes / 60,
                "Start": parser.parse(start).isoformat(),
                "End": parser.parse(end).isoformat()
            }
            headl_prefix = "ENDRET"
            response = requests.post(url, verify=False, headers=headers, json=data)
    if not response.ok:
        return redirect(request.referrer)
    dic = response.json()
    exam = Exam(dic['id'], dic['courseImplementationId'], dic['category'], dic['durationHours'], dic['periodStart'], dic['periodEnd'],
                dic['courseImplementationCode'], dic['courseImplementationName'],
                dic['examImplementationIds'], dic['examResultIds'],
                dic['link'], dic['courseImplementationLink'])
    return render_template("admin/exam/exam.html", user=user, exam=exam, headl_prefix=headl_prefix)