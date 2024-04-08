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



def assignment_create_function():
    # authenticate user and get url
    user = session["user"]
    url_ext = f"Assignment"
    url = URLpre + url_ext

    new_assignment_data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'deadline': request.form['deadline'],
        'courseImplementationId': int(request.form['courseImplementationId'])
        }

    headers = {
        "Authorization": f"Bearer {session['token']}",
        "Content-Type": "application/json"
    }

    print(f"HEADERS! {headers}")


    response = requests.post(url, json=new_assignment_data, verify=False, headers=headers)

    if response.ok:
        assignment_new = response.json()
        assignment = Assignment(assignment_new['id'],
                                assignment_new['name'],
                                assignment_new['description'],
                                assignment_new['deadline'],
                                assignment_new.get('courseImplementation', None),
                                assignment_new.get('courseImplementationCode', ''),
                                assignment_new.get('courseImplementationName', ''),
                                assignment_new.get('courseImplementationLink', ''),
                                assignment_new.get('link', ''))
        print(f"ASSIGNMENT DATA!!: {assignment_new}")

        return render_template('admin/assignment/add_assignment.html', assignment=assignment, user=user)
    msg = f"Statuskode: {response.status_code}"
    return render_template("error.html", user=user, msg=msg, status=int(response.status_code))


