from flask import request, session, abort
import requests
from datetime import datetime
from ..config import configuration
from ..venue import Venue


URLpre = configuration["URLpre"]


def api_get_venues_func():
    from_ = request.args.get("from")
    to = request.args.get("to")

    from_dt_iso = datetime.fromisoformat(from_.replace("T", " ")).isoformat()
    to_dt_iso = datetime.fromisoformat(to.replace("T", " ")).isoformat()


    url_ext = f"venue?from={from_}&to={to}"
    url = URLpre+url_ext
    print(url)

    headers = {"Authorization": f"Bearer {session['token']}"}
    response = requests.get(url, verify=False, headers=headers)

    if response.ok:
        as_lOfdics = response.json()
        return as_lOfdics
    abort(401)

    # return {"message": "Hei fra GetVenues!",
    #         "feedback": [from_, to]}