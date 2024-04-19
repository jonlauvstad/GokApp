from flask import render_template, request, session, abort
from ..config import configuration
import requests

URLpre = configuration["URLpre"]

def venue_id_function(id):
    user = session["user"]
    id = int(id)

    url_ext = f"Venue/{id}"
    url = URLpre + url_ext
    headers = {"Authorization": f"Bearer {session['token']}"}
    response = requests.get(url, verify=False, headers=headers)

    if not response.ok:
        abort(404)

    dic = response.json()
    # return dic
    return render_template("venue.html", venue=dic)
