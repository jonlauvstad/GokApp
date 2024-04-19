import json

from flask import Flask, redirect, render_template, request, session, abort
from ..config import configuration
from ..global_vars import bank_holidays
import requests
from ..examImplementation import ExamImplementation
from ..exam import Exam
from ..user import User
from ..realExamGroup import RealExamGroup, make_groups
import datetime
from dateutil import parser
from dateutil import tz

tzinfos = {"CET": tz.gettz('Europe/Paris')}
tzinfos["UTC"] = datetime.timezone.utc

target_timezone = tz.gettz("CET")
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
                                 as_dic['location'], as_dic['courseImplementationLink'], as_dic['venueLink'], as_dic['link'], as_dic['examLink'])

        return render_template("admin/exam_imp/examImplementation.html", examImp=examImp, user=user)
    msg = f"Statuskode: {response.status_code}"
    return render_template("error.html", user=user, msg=msg, status=int(response.status_code))

def examImp_start():
    user = session["user"]

    # Get exams
    url_ext = f"exam?isOwner={True}"
    url = URLpre + url_ext
    headers = {"Authorization": f"Bearer {session['token']}"}
    response = requests.get(url, verify=False, headers=headers)
    if not response.ok:
        abort(404)
    lOfDics = response.json()
    exams = [
        Exam(dic['id'], dic['courseImplementationId'], dic['category'], dic['durationHours'], dic['periodStart'],
             dic['periodEnd'],
             dic['courseImplementationCode'], dic['courseImplementationName'],
             dic['examImplementationIds'], dic['examResultIds'],
             dic['link'], dic['courseImplementationLink'])
        for dic in lOfDics
    ]
    exams = [item for item in exams if item.periodStart_datetime > datetime.datetime.now()]

    return render_template("admin/exam_imp/examImp_start.html", user=user, exams=exams)     # , courseImps=cis_lOfdics

def examImp_register(exam_id):
    user = session["user"]
    groups = None
    grps = None
    err_msg = None
    if "err_msg" in session:
        err_msg = session.pop("err_msg")

    # Hente exam - varsle hvis allerede har examImplementation
    # A) Henter examImps -varsler hvis noen
    url_ext = f"ExamImplementation/Exam/{exam_id}"
    url = URLpre + url_ext
    headers = {"Authorization": f"Bearer {session['token']}"}
    response = requests.get(url, verify=False, headers=headers)
    if not response.ok:
        print("Line 82")
        abort(404)
    examImp_dics = response.json()
    alreadyExImp = len(examImp_dics) > 0
    alr_exImp = None if not alreadyExImp else f"Eksamen med id {exam_id} har allerede eksamens-gjennomføringer"

    # B) Henter exam
    url_ext = f"exam/{exam_id}"
    url = URLpre + url_ext
    headers = {"Authorization": f"Bearer {session['token']}"}
    response = requests.get(url, verify=False, headers=headers)
    if not response.ok:
        print("Line93")
        abort(404)
    dic = response.json()
    exam = Exam(dic['id'], dic['courseImplementationId'], dic['category'], dic['durationHours'], dic['periodStart'],
                dic['periodEnd'],
                dic['courseImplementationCode'], dic['courseImplementationName'],
                dic['examImplementationIds'], dic['examResultIds'],
                dic['link'], dic['courseImplementationLink'])

    # C) Legger til deltakere
    url_ext = f"CourseImplementation/Qualified/{exam.courseImplementationId}"
    url = URLpre + url_ext
    headers = {"Authorization": f"Bearer {session['token']}"}
    response = requests.get(url, verify=False, headers=headers)
    if not response.ok:
        print("Line 108")
        abort(404)
    user_ids = response.json()

    # D) Dersom exam.category er 'muntlig gruppe': Hente gruppene/lage dem
    if exam.category == "muntlig gruppe":
        url_ext = f"ExamGroup?examId={exam_id}"
        url = URLpre + url_ext
        response = requests.get(url, verify=False, headers=headers)
        if not response.ok:
            print("Line 119")
            abort(404)
        exGr_dics = response.json()
        groups = make_groups(exGr_dics)
        grps = [[elm['userId'] for elm in item.participants] for item in groups]

    # E) Rendre html m/exam - hjemme/skriftlig/muntlig/muntlig gruppe:

    start_tpkt = exam.periodStart_datetime + datetime.timedelta(hours=9)
    b_holidays = json.dumps([item.isoformat() for item in bank_holidays])

    return render_template("admin/exam_imp/examImp_reg.html", user=user, exam=exam, stud_ids=user_ids, start_tpkt=start_tpkt,
                           groups=groups, grps=grps, holidays=b_holidays, err_msg=err_msg, alr_exImp=alr_exImp)

def examImplementation_function():
    user = session["user"]
    url_ext = f"ExamImplementation"
    url = URLpre + url_ext
    headers = {"Authorization": f"Bearer {session['token']}"}

    if request.method == "POST":
        exam_id = int(request.form.get("examId"))
        category = request.form.get("category")

        if category == "hjemme":
            participantIds = [int(item) for item in request.form.getlist("participant")]
            venueId = 6
            startTime = parser.parse(request.form.get("startTime"))
            duration = float(request.form.get("duration"))
            endTime = startTime + datetime.timedelta(hours=int(duration)) + datetime.timedelta(minutes=(duration-int(duration))*60)

            exam_dto = {
                "ExamId": exam_id,
                "VenueId": venueId,
                "StartTime": startTime.isoformat(),
                "EndTime": endTime.isoformat(),
                "ParticipantIds": participantIds
            }
            examDTOs = [exam_dto]

        elif category == "skriftlig":
            startTime = parser.parse(request.form.get("startTime"))
            participantIds = [int(item) for item in request.form.get("participants").split(",")]
            venueIds = [int(item) for item in request.form.get("venueIds").split(",")]
            numstudents = [int(item) for item in request.form.get("numstudents").split(",")]
            num_studs_akk = [sum(numstudents[0:i+1]) for i in range(len(numstudents))]
            duration = float(request.form.get("duration"))
            endTime = startTime + datetime.timedelta(hours=int(duration)) + datetime.timedelta(minutes=(duration - int(duration)) * 60)
            examDTOs = [{
                "ExamId": exam_id,
                "VenueId": venueIds[i],
                "StartTime": startTime.isoformat(),
                "EndTime": endTime.isoformat(),
                "ParticipantIds": participantIds[0 if i==0 else num_studs_akk[i-1] : num_studs_akk[i]]
            } for i in range(len(venueIds))]

        else:                   # elif category == "muntlig":         # Eller else ?
            startTime = [parser.parse(f"{item} UTC", tzinfos=tzinfos).astimezone(target_timezone) for item in request.form.get("startTime").split(",")]
            endTime = [parser.parse(f"{item} UTC", tzinfos=tzinfos).astimezone(target_timezone) for item in request.form.get("endTime").split(",")]
            participantIds = json.loads(request.form.get("students"))
            venueIds = [int(item) for item in request.form.get("venueIds").split(",")]

            examDTOs = [{
                "ExamId": exam_id,
                "VenueId": venueIds[i % len(venueIds)],
                "StartTime": startTime[i].isoformat(),
                "EndTime": endTime[i].isoformat(),
                "ParticipantIds": participantIds[i]
            } for i in range(len(startTime))]

        response = requests.post(url, verify=False, headers=headers, json=examDTOs)
        if not response.ok:
            session["err_msg"] = f"{response.text}.%" \
                                 f"Sannsynligvis kolliderer den/de foreslåtte eksamenen(e) med andre for samme program-gjennomføring."
            return redirect(f"/implementation_exam/register/{exam_id}")

        examImp_dics = response.json()
        exams = [ExamImplementation(item['id'], item['examId'], item['venueId'], item['startTime'], item['endTime'],
                                    item['category'], item['durationHours'], item['courseImplementationId'],
                                    item['courseImplementationName'], item['courseImplementationCode'],
                                    item['venueName'],
                                    item['location'], item['courseImplementationLink'], item['venueLink'],
                                    item['link'], item['examLink']) for item in examImp_dics]
        return render_template("admin/exam_imp/examImps.html", user=user, exams=exams)

def examImplementation_ExamId_function(exam_id):
    user = session["user"]
    url_ext = f"ExamImplementation/Exam/{exam_id}"
    url = URLpre + url_ext
    headers = {"Authorization": f"Bearer {session['token']}"}
    deleted = False
    empty = False

    if not request.args.get("delete"):
        response = requests.get(url, verify=False, headers=headers)
    else:
        deleted = True
        response = requests.delete(url, verify=False, headers=headers)
    if not response.ok:
        print(response.text)
        abort(404)

    examImp_dics = response.json()
    exams = [ExamImplementation(item['id'], item['examId'], item['venueId'], item['startTime'], item['endTime'],
                                item['category'], item['durationHours'], item['courseImplementationId'],
                                item['courseImplementationName'], item['courseImplementationCode'],
                                item['venueName'],
                                item['location'], item['courseImplementationLink'], item['venueLink'],
                                item['link'], item['examLink']) for item in examImp_dics]
    if deleted:
        num_studs = sum([len(item["userExamImplementation"]) for item in examImp_dics])
        deleted = f"{len(exams)} gjennomføringer slettet, {num_studs} studenter påvirket"

    if len(examImp_dics) == 0:
        empty = True

    return render_template("admin/exam_imp/examImps.html", user=user, exams=exams, deleted=deleted, empty=empty, exam_id=exam_id)


def examImp_group(exam_id):
    user = session["user"]

    # A) Henter exam
    url_ext = f"exam/{exam_id}"
    url = URLpre + url_ext
    headers = {"Authorization": f"Bearer {session['token']}"}
    response = requests.get(url, verify=False, headers=headers)
    if not response.ok:
        abort(404)
    dic = response.json()
    exam = Exam(dic['id'], dic['courseImplementationId'], dic['category'], dic['durationHours'], dic['periodStart'],
                dic['periodEnd'],
                dic['courseImplementationCode'], dic['courseImplementationName'],
                dic['examImplementationIds'], dic['examResultIds'],
                dic['link'], dic['courseImplementationLink'])

    # B) Henter kvalifiserte deltakere
    url_ext = f"CourseImplementation/QualifiedObject/{exam_id}"
    url = URLpre + url_ext
    response = requests.get(url, verify=False, headers=headers)
    if not response.ok:
        abort(404)
    user_dics = response.json()
    qual_studs = [
        User(item['id'], item['gokstadEmail'], item['firstName'], item['lastName'], item['email2'], item['email3'], item['role'], item['link'])
        for item in user_dics
    ]

    # C) Henter gruppe-entries for examen
    url_ext = f"ExamGroup?examId={exam_id}"
    url = URLpre + url_ext
    response = requests.get(url, verify=False, headers=headers)
    if not response.ok:
        abort(404)
    exGr_dics = response.json()
    exGr_userIds = [item['userId'] for item in exGr_dics]
    qual_studs = [item for item in qual_studs if item.id not in exGr_userIds]

    return render_template("admin/exam_imp/examGroup_start.html", user=user, exam=exam, qual_studs=qual_studs)


def exam_group(exam_id):
    user = session["user"]
    headers = {"Authorization": f"Bearer {session['token']}"}

    if request.method == "GET":
        name = request.args.get("name")

        # GETTING ALL GROUPS FOR EXAM_ID
        if not name:
            url_ext = f"ExamGroup?examId={exam_id}"
            url = URLpre + url_ext
            response = requests.get(url, verify=False, headers=headers)
            if not response.ok:
                abort(404)
            exGr_dics = response.json()
            groups = make_groups(exGr_dics)
            return render_template("admin/exam_imp/examGroups.html", user=user, groups=groups, exam_id=exam_id)

        # GETTING ONE GROUP (BY NAME)
        url_ext = f"ExamGroup?examId={exam_id}&name={name}"
        url = URLpre + url_ext
        response = requests.get(url, verify=False, headers=headers)
        if not response.ok:
            abort(404)
        exGr_dics = response.json()
        try:
            exGr = RealExamGroup(exGr_dics)
        except ValueError as e:
            print(e)
            abort(404)
        qual_studs = get_qual_studs(exam_id)
        return render_template("admin/exam_imp/examGroup.html", user=user, exGr=exGr, action="GET_ONE", qual_studs=qual_studs)

    request_method = request.form.get("requestMethod")

    # ADDED NEW GROUP
    if request_method == "ADD":
        group_name = request.form.get("groupName")
        student_ids = [int(item) for item in request.form.getlist("studentId")]

        examDTOs = [{"ExamId": exam_id, "UserId": item, "Name": group_name} for item in student_ids]
        url_ext = f"ExamGroup/Exam/{exam_id}"
        url = URLpre + url_ext
        response = requests.post(url, verify=False, headers=headers, json=examDTOs)
        if not response.ok:
            abort(404)
        exGr_dics = response.json()
        try:
            exGr = RealExamGroup(exGr_dics)
        except ValueError as e:
            print(e)
            abort(404)
        qual_studs = get_qual_studs(exam_id)
        return render_template("admin/exam_imp/examGroup.html", user=user, exGr=exGr, action=request_method, qual_studs=qual_studs)

    # DELETED GROUP
    if request_method == "DELETE":
        name = request.form.get("name")
        # Calle API
        url_ext = f"ExamGroup"
        url = URLpre + url_ext
        params = {"examId": exam_id, "name": name}
        response = requests.delete(url, verify=False, headers=headers, params=params)
        if not response.ok:
            abort(404)
        dic = response.json()
        # Returnere html
        return render_template("admin/exam_imp/examGroup_delete.html", user=user, name=name, num_deleted=dic['numDeleted'], exam_id=exam_id)

    # ADD ONE
    if request_method == "ADD_ONE":
        name = request.form.get("name")
        userId = int(request.form.get("userId"))
        data = {
            "ExamId": exam_id,
            "UserId": userId,
            "Name": name
        }
        # Calle API
        url_ext = f"ExamGroup"
        url = URLpre + url_ext
        response = requests.post(url, verify=False, headers=headers, json=data)
        if not response.ok:
            abort(404)
        exGr_dic = response.json()
        return render_template("admin/exam_imp/examGroupOne.html", user=user, examGroup=exGr_dic, added=True)

    # REMOVE
    if request_method == "REMOVE":
        id = request.form.get("id")
        # Calle API
        url_ext = f"ExamGroup/{id}"
        url = URLpre + url_ext
        response = requests.delete(url, verify=False, headers=headers)
        if not response.ok:
            abort(404)
        exGr_dic = response.json()
        return render_template("admin/exam_imp/examGroupOne.html", user=user, examGroup=exGr_dic, removed=True)



# HELPERS

def get_qual_studs(exam_id):
    headers = {"Authorization": f"Bearer {session['token']}"}

    # 1) Henter kvalifiserte deltakere
    url_ext = f"CourseImplementation/QualifiedObject/{exam_id}"
    url = URLpre + url_ext
    response = requests.get(url, verify=False, headers=headers)
    if not response.ok:
        abort(404)
    user_dics = response.json()
    qual_studs = [
        User(item['id'], item['gokstadEmail'], item['firstName'], item['lastName'], item['email2'], item['email3'],
             item['role'], item['link'])
        for item in user_dics
    ]

    # 2) Henter gruppe-entries for examen
    url_ext = f"ExamGroup?examId={exam_id}"
    url = URLpre + url_ext
    response = requests.get(url, verify=False, headers=headers)
    if not response.ok:
        abort(404)
    exGr_dics = response.json()
    exGr_userIds = [item['userId'] for item in exGr_dics]

    # 3) Trekker 2 fra 1
    return [item for item in qual_studs if item.id not in exGr_userIds]
