from flask import Flask, redirect, render_template, request, session, flash, url_for, jsonify, abort
from ..config import configuration
import requests
from ..assignment import Assignment

# URLpre = configuration["URLpre"]

URLpre = "https://localhost:7042/api/v1/"


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


def template_assignment_function():
    user = session["user"]
    role = session.get('role')
    options = ["registrere", "endre", "slette"]

    courseImpId = request.form.get('courseImplementationId') if request.method != 'GET' else None

    if request.method == 'POST':
        return assignment_create_function()

    elif request.method == 'GET':
        return assignment_id_function(id)

    else:
        return "Not implemented", 501

    # elif request.method == 'PUT   ':
        # return jsonify({'message': 'PUT method not yet implemented'}), 501
        # return assignment_update_function()
    # elif request.method == 'DELETE':
        # return jsonify({'message': 'DELETE method not yet implemented'}), 501
        # return assignment_delete_function()



def assignment_create_function():
    user = session["user"]
    headers = {
        "Authorization": f"Bearer {session['token']}",
        "Content-Type": "application/json"}

    url = f"{URLpre}Assignment"

    new_assignment_data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'deadline': request.form['deadline'],
        'courseImplementationId': int(request.form['courseImplementationId'])
        }

    print(f"HEADERS! {headers}")

    response = requests.post(url, json=new_assignment_data, verify=False, headers=headers)

    if response.ok:
        assignment_new = response.json()
        assignment = Assignment(assignment_new.get('id'),
                                assignment_new.get('name'),
                                assignment_new.get('description'),
                                assignment_new.get('deadline'),
                                assignment_new.get('courseImplementation', None),
                                assignment_new.get('courseImplementationCode', ''),
                                assignment_new.get('courseImplementationName', ''),
                                assignment_new.get('courseImplementationLink', ''),
                                assignment_new.get('link', ''))
        print(f"ASSIGNMENT DATA!!: {assignment_new}")

        return render_template(
            'admin/assignment/get_assignments.html',
            assignment=assignment, user=user)
    else:
        msg = f"Statuskode: {response.status_code}"
        return render_template("error.html", user=user, msg=msg, status=int(response.status_code))


def assignment_getAll_function():
    user = session["user"]

    action = request.args.get("action")
    courseImpId = request.args.get("courseImpId")
    params = {} if not courseImpId else {"courseImpId": int(courseImpId)}

    url_ext = f"Assignment"
    url = URLpre + url_ext
    headers = {"Authorization": f"Bearer {session['token']}"}
    response = requests.get(url, verify=False, headers=headers, params=params)
    if not response.ok:
        abort(404)
    lOfDics = response.json()
    assignments = [
        Assignment(dic['id'], dic['courseImplementationId'], dic['category'], dic['durationHours'], dic['periodStart'],
             dic['periodEnd'],
             dic['courseImplementationCode'], dic['courseImplementationName'],
             dic['examImplementationIds'])
        for dic in lOfDics
    ]


    return render_template("admin/assignment/get_assignments", user=user, assignments=assignments, action=action)


def conf_assignment_function():
    user = session["user"]

    action = request.form.get("action")

    match action:
        case "endre":
            return
