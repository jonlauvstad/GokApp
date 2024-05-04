from datetime import datetime
import logging
from dateutil import parser
from flask import Flask, redirect, render_template, request, session, flash, url_for, jsonify, abort
from requests import RequestException

from ..config import configuration
import requests
from ..assignment import Assignment

URLpre = configuration["URLpre"]
logging.basicConfig(level=logging.DEBUG)
MAX_LENGTH = 50


def admin_assignment_function():
    user = session["user"]
    return render_template("admin/assignment/assignment_main.html", user=user)


def api_call(url, method='get', headers=None, json=None):
    try:
        if method == 'put':
            response = requests.put(url, headers=headers, json=json)
        elif method == 'delete':
            response = requests.delete(url, headers=headers)
        else:
            response = requests.get(url, headers=headers)

        response.raise_for_status()
        return response.json()
    except RequestException as e:
        logging.error(f"\n\tℹ️ API_CALL: Failed to {method} data: {str(e)}")

        print(f"API call failed: {e}")
        return None


def template_assignment_function(put=None, try_delete=None):
    logging.debug("\n\tℹ️ Entering TEMPLATE_ASSIGNMENT_FUNCTION with put=%s, try_delete=%s", put, try_delete)

    user = session["user"]
    logging.debug("\n\tℹ️ TEMPLATE_ASSIGNMENT_FUNCTION: User object at start of function: %s", user)
    options = ["registrére", "endre", "slette"]
    assignment = session.pop('assignment', None) if put else None
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
        logging.debug(f"\n\t✅ TEMPLATE_ASSIGNMENT_FUNCTION: API response received: {response.text}")
    except requests.RequestException as e:
        logging.error(f"\n\t❌ TEMPLATE_ASSIGNMENT_FUNCTION: Failed to fetch course implementations: {str(e)}")
        abort(404)

    courseImplementations = response.json()
    logging.debug(f"\n\t✅ TEMPLATE_ASSIGNMENT_FUNCTION: Parsed JSON data: {courseImplementations}")

    error_msg = None

    if assignment:
        valid_ids = [item['id'] for item in courseImplementations]
        if assignment.courseImplementationId not in valid_ids:
            logging.warning(f"\n\t❌ TEMPLATE_ASSIGNMENT_FUNCTION: Unauthorized access attempt by user {user} on assignment {assignment.id}")
            error_msg = f"Du er ikke  autorisert til å {option} arbeidskrav med id {assignment.id}."
            assignment = None
            put, try_delete, option = None, None, None

    logging.debug("\n\t✅ TEMPLATE_ASSIGNMENT_FUNCTION: Exiting with rendered template.")
    return render_template("admin/assignment/manage_assignment.html",
            user=user, options=options, courseImps=courseImplementations,
            put=put, assignment=assignment, try_delete=try_delete,
            option=option, error_msg=error_msg)


def conf_assignment_function():
    logging.debug("\n\tℹ️ Entering CONF_ASSIGNMENT_FUNCTION")
    user = session["user"]
    action = request.form.get("action", "")[:MAX_LENGTH]
    logging.info(f"\n\t✅ CONF_ASSIGNMENT_FUNCTION: Action received: {action}")

    match action:
        case "endre" | "slette":
            return template_assignment_function(put=True, try_delete=(action == "slette"))

    mandatory_value = request.form.get("mandatory", "false")  # Default to "false" if not provided
    is_mandatory = mandatory_value.lower() == 'true'  # Safely convert to boolean

    # registrere
    data = {
        "CourseImplementationId": request.form.get("courseId"),
        "Name": request.form.get("name"),
        "Deadline": request.form.get("deadline"),
        "Description": request.form.get("description"),
        "Mandatory": is_mandatory
    }
    logging.debug(f"\n\tℹ️ CONF_ASSIGNMENT_FUNCTION: Sending data: {data}")

    url = URLpre + "assignment"
    headers = {"Authorization": f"Bearer {session['token']}"}

    try:
        response = requests.post(url, verify=False, headers=headers, json=data)
        response.raise_for_status()
        dic = response.json()
        print("\n\tℹ️ CONF_ASSIGNMENT_FUNCTION: API response data:", dic)
        assignment = (Assignment
                      (dic['id'],
                       dic['name'],
                       dic['description'],
                       dic['deadline'],
                       dic['mandatory'],
                       dic['courseImplementationId'],
                       dic['courseImplementationCode'],
                       dic['courseImplementationName'],
                       dic['courseImplementationLink'],
                       dic['link']))

        print("\n\tℹ️ CONF_ASSIGNMENT_FUNCTION: API response data:", dic)  # This prints the raw API response
        print("\n\tℹ️ CONF_ASSIGNMENT_FUNCTION: Assignment to render:", vars(assignment))  # This prints the assignment object's properties

        logging.debug("\n\t✅ CONF_ASSIGNMENT_FUNCTION: New assignment created successfully with ID: %s", assignment.id)
        flash('Assignment created successfully!', 'success')
        return render_template("admin/assignment/assignment.html", user=user, assignment=assignment, headl_prefix="NY ")

    except requests.RequestException as e:
        error_message = response.json() if response else str(e)
        logging.error("\n\t❌ CONF_ASSIGNMENT_FUNCTION: Failed to create assignment %s", str(e))
        flash(f"Error: {error_message}", 'error')
        return render_template("admin/assignment/manage_assignment.html", user=user, form_data=request.form)


def assignment_id_function(id):
    logging.debug(f"\n\tℹ️ ASSIGNMENT_ID_FUNCTION: Fetching assignment with ID: {id}")

    user = session["user"]
    id = int(id)
    url_ext = f"assignment/{id}"
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
            # UPDATE
            courseId = request.form.get("courseId")
            description = request.form.get("description")
            deadline = request.form.get("deadline")
            mandatory = request.form.get("mandatory")

            data = {
                "CourseImplementationId": courseId,
                "Description": description,
                "Deadline": deadline,
                "Mandatory": mandatory
            }
            headl_prefix = "ENDRET"
            response = requests.put(url, verify=False, headers=headers, json=data)
    if not response.ok:
        return redirect(request.referrer)
    dic = response.json()

    assignment = (Assignment(
                    dic['id'],
                    dic['name'],
                    dic['description'],
                    dic['deadline'],
                    dic['mandatory'],
                    dic['courseImplementationId'],
                    dic['courseImplementationCode'],
                    dic['courseImplementationName'],
                    dic['courseImplementationLink'],
                    dic['link']))
    return render_template("admin/assignment/assignment.html", user=user, assignment=assignment, headl_prefix=headl_prefix)




def assignment_getAll_function():
    courseImpId = request.args.get("courseImpId")
    params = {} if not courseImpId else {"courseImpId": int(courseImpId)}

    url = f"{URLpre}Assignment"
    headers = {"Authorization": f"Bearer {session['token']}"}
    response = requests.get(url, verify=False, headers=headers, params=params)

    if response.ok:
        assignment_dictlist = response.json()
        assignments = [
            Assignment(
                id=dic['id'],
                name=dic['name'],
                description=dic['description'],
                deadline=dic['deadline'],
                mandatory=dic['mandatory'],
                courseImplementationId=dic.get('courseImplementationId'),
                courseImplementationCode=dic.get('courseImplementationCode'),
                courseImplementationName=dic.get('courseImplementationName'),
                courseImplementationLink=dic.get('courseImplementationLink'),
                link=dic.get('link')
            )
            for dic in assignment_dictlist
        ]
        print("Parsed Assignments:", assignments)  # Debug to check if objects are created properly
        return assignments
    else:
        print("Failed to fetch assignments", response.status_code)  # More detailed error message
        return []


def get_assignments():
    user = session["user"]

    # Get assignments
    url_ext = f"assignment?isOwner={True}"
    url = URLpre + url_ext
    headers = {"Authorization": f"Bearer {session['token']}"}
    response = requests.get(url, verify=False, headers=headers)
    if not response.ok:
        print(f"\n\t❌ GET_ASSIGNMENTS_FUNCTION: Failed to fetch assignments: {response.status_code}")
        abort(404)
    assignmentDictList = response.json()
    assignments = []
    for dic in assignmentDictList:
        try:
            assignment = Assignment(
                id=dic['id'],
                name=dic['name'],
                description=dic['description'],
                deadline=dic['deadline'],
                mandatory=dic['mandatory'],
                courseImplementationId=dic['courseImplementationId'],
                courseImplementationCode=dic['courseImplementationCode'],
                courseImplementationName=dic['courseImplementationName'],
                courseImplementationLink=dic['courseImplementationLink'],
                link=dic['link']
            )
            assignments.append(assignment)
        except KeyError as e:
            print(f"\n\t❌ GET_ASSIGNMENTS_FUNCTION: Missing key in assignment data: {e}")

    return render_template("admin/assignment/get_assignments.html", user=user, assignments=assignments)



def assignment_update_function(id, form_data):
    url = f"{URLpre}assignment/{id}"
    headers = {"Authorization": f"Bearer {session['token']}"}
    response = requests.put(url, json=form_data, headers=headers)
    if response.status_code == 200:
        return {'status': 'success', 'data': response.json()}
    else:
        return {'status': 'failure', 'error': response.text}



def assignment_delete_function(id):
    url = f"{URLpre}assignment/{id}"
    headers = {"Authorization": f"Bearer {session['token']}"}
    response = requests.delete(url, headers=headers)
    if response.status_code == 200:
        return {'status': 'success', 'data': response.json()}  # Ensure it's a dictionary
    else:
        return {'status': 'failure', 'error': response.text}



"""def assignment_getAll_function():
    user = session["user"]
    action = request.args.get("action")
    courseImpId = request.args.get("courseImpId")
    params = {} if not courseImpId else {"courseImpId": int(courseImpId)}

    url = f"{URLpre}Assignment"
    headers = {"Authorization": f"Bearer {session['token']}"}
    response = requests.get(url, verify=False, headers=headers, params=params)

    if response.ok:
        assignment_dictlist = response.json()
        assignments = [
            Assignment(
                dic.get('id'),
                dic.get('name'),
                dic.get('description'),
                dic.get('deadline'),
                dic.get('mandatory', True),
                # True if dic.get('mandatory', 'True') in [True, 'True', 'true', 1, '1'] else False,
                dic.get('courseImplementationId', 'No Id'),
                dic.get('courseImplementationCode', 'No Code'),
                dic.get('courseImplementationName', 'No CourseImpName'),
                dic.get('courseImplementationLink', 'No CourseImpLink'),
                dic.get('link', 'No link')
            )
            for dic in assignment_dictlist
        ]

        return render_template("admin/assignment/assignment_main.html", user=user, assignments=assignments, action=action)
    else:
        print("Failed to fetch assignments")  # Debugging line
        return []  # Return an empty list if the API call fails"""
