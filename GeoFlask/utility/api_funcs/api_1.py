from flask import request, session, abort
import requests
from datetime import datetime
from ..config import configuration
from ..venue import Venue
from ..exam import Exam


URLpre = configuration["URLpre"]


def api_get_venues_func():
    from_ = request.args.get("from")
    to = request.args.get("to")

    url_ext = f"venue?from={from_}&to={to}"
    url = URLpre+url_ext

    headers = {"Authorization": f"Bearer {session['token']}"}
    response = requests.get(url, verify=False, headers=headers)

    if response.ok:
        as_lOfdics = response.json()
        return as_lOfdics
    abort(401)

def api_get_alerts_user_func(userId):
    seen = request.args.get("seen")
    number = request.args.get("number")
    # print(f"\nGET ALERTS.. CALLED from {userId}, seen={seen}\n")

    url_ext = f"alert/user/{userId}"
    url = URLpre + url_ext

    headers = {"Authorization": f"Bearer {session['token']}"}
    params = {
        "seen": True if seen else False
    }
    response = requests.get(url, verify=False, headers=headers, params=params)
    if response.ok:
        as_lOfdics = response.json()
        if number:
            dic = {"number": len(as_lOfdics)}
            # print(dic)
            return dic
        return as_lOfdics
    abort(401)

def api_update_alert_id_func(alertId):
    url_ext = f"alert/{alertId}"
    url = URLpre + url_ext

    headers = {"Authorization": f"Bearer {session['token']}"}
    response = requests.put(url, verify=False, headers=headers)
    if response.ok:
        dic = response.json()
        return dic
    print(response.text)
    return {"error_msg": f"Kunne ikke oppdatere varsel med id {alertId}"}

def api_exam_id_function(id):
    url_ext = f"exam/{id}"
    url = URLpre + url_ext

    headers = {"Authorization": f"Bearer {session['token']}"}
    response = requests.get(url, verify=False, headers=headers)
    if response.ok:
        dic = response.json()
        exam = Exam(dic['id'], dic['courseImplementationId'], dic['category'], dic['durationHours'], dic['periodStart'],
                    dic['periodEnd'],
                    dic['courseImplementationCode'], dic['courseImplementationName'],
                    dic['examImplementationIds'], dic['examResultIds'],
                    dic['link'], dic['courseImplementationLink'])
        if request.args.get("save"):
            session['exam'] = exam
        return exam.serialize()
    print(response.status_code, response.text)
    return {
        "err_msg": f"Kunne ikke finne eksamen med id {id}."
    }

