from flask import Flask, redirect, render_template, request, session
import requests
from datetime import datetime, timezone
from dateutil import parser
from ..config import configuration
from ..event_day import EventDay
from ..event import Event


URLpre = configuration["URLpre"]      #"https://localhost:7042/api/v1/"


def calendar_function():
    user = session["user"]

    start_date = request.args.get('start')
    start = datetime.now().date()

    if start_date:
        start = parser.parse(start_date).date()    #, dayfirst=True
    today = start.strftime("%Y-%m-%d")
    num_days = request.args.get('num_days')
    if not num_days:
        num_days = 14
    else:
        num_days = int(num_days)

    headers = {"Authorization": f"Bearer {session['token']}"}

    url_ext = f"Event/User/{user.id}"
    url = URLpre + url_ext
    response = requests.get(url, verify=False, headers=headers)
    if response.ok:
        response = response.json()
        events = [Event(item['time'], item['underlyingId'], item['type'], item['typeEng'], item['courseImplementationId'], item['courseImpCode'],
                        item['courseImpName'], item['courseImplementationLink'], item['link'], item['timeEnd']) for item in response]
        days = EventDay.make_days(start, num_days, events)
        return render_template("events.html", user=user, events=events, days=days, num_days=num_days, today=today)
    msg = f"Statuskode: {response.status_code}"
    return render_template("error.html", user=user, msg=msg, status=int(response.status_code))
