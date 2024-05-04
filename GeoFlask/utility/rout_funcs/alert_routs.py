from flask import Flask, redirect, render_template, request, session, abort
from ..config import configuration
import requests
from ..alert import Alert

URLpre = configuration["URLpre"]

def alert_see_unseen_function():
    user = session["user"]
    url_ext = f"Alert/User/{user.id}"
    url = URLpre + url_ext

    headers = {"Authorization": f"Bearer {session['token']}"}
    params = {"seen": False}
    response = requests.get(url, verify=False, headers=headers, params=params)
    if response.ok:
        listOfDicts = response.json()
        alerts = [
            Alert(item['id'], item['userId'], item['message'], item['time'], item['seen'], item['links'])
            for item in listOfDicts
        ]
        return render_template("alerts.html", user=user, alerts=alerts)
    abort(404)