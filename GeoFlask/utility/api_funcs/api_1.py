from flask import request, session, abort
import requests
from datetime import datetime
from ..config import configuration
from ..venue import Venue


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
    print(f"\nGET ALERTS.. CALLED from {userId}, seen={seen}\n")

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
            print(dic)
            return dic
        return as_lOfdics
    abort(401)