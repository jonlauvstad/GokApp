from flask import Flask, redirect, render_template, request, session, abort
from ..config import configuration
# from ..global_vars import weekdays
import requests
# from ..lecture import Lecture
# from . import admin_routs
# from dateutil import parser
# import datetime
# from ..util_funcs import *
from ..alert import Alert

URLpre = configuration["URLpre"]

def alert_see_unseen_function():
    user = session["user"]
    # url_ext = f"Alert/User"
    url_ext = f"Alert/User/{user.id}"
    url = URLpre + url_ext

    headers = {"Authorization": f"Bearer {session['token']}"}
    params = {"seen": False}
    # response = requests.put(url, verify=False, headers=headers, params=params)
    response = requests.get(url, verify=False, headers=headers, params=params)
    if response.ok:
        listOfDicts = response.json()
        alerts = [
            Alert(item['id'], item['userId'], item['message'], item['time'], item['seen'], item['links'])
            for item in listOfDicts
        ]
        for alert in alerts:
            print(alert)
        return render_template("alerts.html", user=user, alerts=alerts)
    abort(404)