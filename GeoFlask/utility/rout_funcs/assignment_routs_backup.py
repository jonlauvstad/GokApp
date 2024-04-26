from datetime import datetime
import logging
from dateutil import parser
from flask import Flask, redirect, render_template, request, session, flash, url_for, jsonify, abort
from requests import RequestException

from ..config import configuration
import requests
from ..assignment import Assignment

# URLpre = configuration["URLpre"]
logging.basicConfig(level=logging.DEBUG)

URLpre = "https://localhost:7042/api/v1/"


def api_call(url, method='get', **kwargs):
    try:
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()  # Raises HTTPError for bad responses
        return response.json()
    except RequestException as e:
        print(f"API call failed: {e}")
        return None


def template_assignment_function(put=None, try_delete=None):
    logging.debug("\n\tℹ️Entering template_assignment_function with put=%s, try_delete=%s", put, try_delete)

    user = session["user"]
    logging.debug("\n\tℹ️User object at start of function: %s", user)
    options = ["registrére", "endre", "slette"]
    assignment = session.pop('exam', None) if put else None
    option = "slette" if try_delete and put else ("endre" if put else None)

    # Getting CourseImplementationIds:
    url = URLpre + "courseImplementation"
    now = datetime.now().isoformat()
    user_role = user.role if hasattr(user, 'role') else 'Balle'
    url += f"?endDate={now}&userRole={user_role}"
    headers = {"Authorization": f"Bearer {session['token']}"}

    try:
        response = requests.get(url, verify=False, headers=headers)
        response.raise_for_status()
        logging.debug("\n\t✅ API response received: %s", response.text)
    except requests.RequestException as e:
        logging.error("\n\t❌Failed to fetch course implementations: %s", str(e))
        abort(404)

    cis_lOfdics = response.json()
    logging.debug("\n\t✅ Parsed JSON data: %s", cis_lOfdics)

    error_msg = None

    if assignment:
        valid_ids = [item['id'] for item in cis_lOfdics]
        if assignment.courseImplementationId not in valid_ids:
            logging.warning("\n\t❌Unauthorized access attempt by user %s on assignment %s", user, assignment.id)
            error_msg = f"Du er ikke  autorisert til å {option} arbeidskrav med id {assignment.id}."
            assignment = None
            put, try_delete, option = None, None, None

    logging.debug("\n\t✅Exiting template_assignment_function with rendered template.")
    return render_template("admin/assignment/add_assignment.html",
            user=user, options=options, courseImps=cis_lOfdics,
            put=put, assignment=assignment, try_delete=try_delete,
            option=option, error_msg=error_msg)


def conf_assignment_function():
    logging.debug("\n\tℹ️Entering conf_assignment_function")
    user = session["user"]
    action = request.form.get("action")
    logging.info("\n\t✅Action received: %s", action)

    match action:
        case "endre" | "slette":
            return template_assignment_function(put=True, try_delete=(action == "slette"))

    # 'registrére'
    data = {
        "CourseImplementationId": request.form.get("courseId"),
        "Name": request.form.get("name"),
        "Deadline": request.form.get("deadline"),
        "Description": request.form.get("description"),
        "Link": request.form.get("link")
    }

    logging.debug("ℹ️Form data for new assignment: %s", data)

    url = URLpre + "assignment"
    headers = {"Authorization": f"Bearer {session['token']}"}



    try:
        response = requests.post(url, verify=False, headers=headers, json=data)
        response.raise_for_status()
        dic = response.json()
        assignment = (Assignment
                 (dic['id'],
                  dic['name'],
                  dic['description'],
                  dic['deadline'],
                  dic['courseImplementationId'],
                  dic['courseImplementationCode'],
                  dic['courseImplementationName'],
                  dic['courseImplementationLink'],
                  dic['link']))

        logging.debug("\n\t✅New assignment created successfully with ID: %s", assignment.id)
        return render_template("admin/assignment/conf_assignment.html", user=user, assignment=assignment, headl_prefix="NY ")

    except requests.RequestException as e:
        logging.error("\n\t❌Failed to create assignment %s", str(e))
        abort(response.status_code if response else 500)



def assignment_getAll_function():
    user = session["user"]
    url = f"{URLpre}Assignment"
    headers = {"Authorization": f"Bearer {session['token']}"}
    courseImpId = request.args.get("courseImpId")
    params = {} if not courseImpId else {"courseImpId": int(courseImpId)}
    response = requests.get(url, verify=False, headers=headers, params=params)

    if response.ok:
        lOfDics = response.json()
        # print(f"Assignments received: {lOfDics}")  # Debugging line
        assignments = [
            Assignment(
                dic.get('id'),
                dic.get('name'),
                dic.get('description'),
                dic.get('deadline'),
                dic.get('courseImplementationId', 'No Id'),
                dic.get('courseImplementationCode', 'No Code'),
                dic.get('courseImplementationName', 'No CourseImpName'),
                dic.get('courseImplementationLink', 'No CourseImpLink'),
                dic.get('link', 'No link')
            )
            for dic in lOfDics
        ]
        return assignments
    else:
        print("Failed to fetch assignments")  # Debugging line
        return []  # Return an empty list if the API call fails


def get_assignments():
    assignments = assignment_getAll_function()
    return render_template('admin/assignment/get_assignments.html', assignments=assignments)


def assignment_get_function(id):
    user = session["user"]
    url = f"{URLpre}Assignment/{id}"
    headers = {"Authorization": f"Bearer {session['token']}"}

    assignment_data = api_call(url, headers=headers)
    if assignment_data:
        assignment = Assignment(**assignment_data)
        return render_template("admin/assignment/get_assignment_by_id.html", assignment=assignment, user=user)
    else:
        msg = "Failed to retrieve assignment data."
        return render_template("error.html", user=user, msg=msg, status=500)

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
            'admin/assignment/create_assignment.html',
            assignment=assignment, user=user)
    else:
        msg = f"Statuskode: {response.status_code}"
        return render_template("error.html", user=user, msg=msg, status=int(response.status_code))


def assignment_update_function(id):
    user = session["user"]
    url = f"{URLpre}Assignment/{id}"
    headers = {
        "Authorization": f"Bearer {session['token']}",
        "Content-Type": "application/json"
    }

    update_data = {
        'name': request.form.get('name'),
        'description': request.form.get('description'),
        'deadline': request.form.get('deadline'),
        'courseImplementationId': int(request.form.get('courseImplemenationId'))
    }

    response = api_call(url, method='put', headers=headers, json=update_data)

    if response:
        return render_template('admin/assignment/update_sucess.html')
    else:
        msg = "Klarte ikke å oppdatere Arbeidskrav."
        return render_template("error.html", user=user, msg=msg, status=500)


def assignment_delete_function(id):
    user = session["user"]
    url = f"{URLpre}Assignment/{id}"
    headers = {"Authorization": f"Bearer {session['token']}"}

    response = api_call(url, method='delete', headers=headers)

    if response:
        return render_template('admin/assignment/delete_success.html', user=user)



"""def template_assignment_function():
    user = session["user"]
    role = session.get('role')
    id = request.args.get('id') or request.form.get('id')

    method = request.form.get('_method')
    if request.method == 'POST' and method:
        if method == 'PUT':
            return assignment_update_function(id)
        elif method == 'DELETE':
            return assignment_delete_function(id)
        elif method == 'GET' and not id:
            return assignment_getAll_function()
    return assignment_get_function(id)"""



"""
def assignment_get_function(id):
    user = session["user"]
    url = f"{URLpre}Assignment/{id}"
    headers = {"Authorization": f"Bearer {session['token']}"}

    response = requests.get(url, verify=False, headers=headers)
    if response.ok:
        as_dic = response.json()
        assignment = Assignment(as_dic['id'], as_dic['name'], as_dic['description'], as_dic['deadline'],
                                as_dic['courseImplementationId'],
                                as_dic['courseImplementationCode'], as_dic['courseImplementationName'],
                                as_dic['courseImplementationLink'],
                                as_dic['link'])
        return render_template("assignment.html", assignment=assignment, user=user)
    msg = f"Statuskode: {response.status_code}"
    return render_template("error.html", user=user, msg=msg, status=int(response.status_code))

"""
