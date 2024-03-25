from flask import render_template, session, request, flash
import requests
from datetime import datetime, timedelta
from dateutil import parser

from . import admin_routs, exam_routs
from .a_venue_calendar_routs import fetch_venue_by_id
from ..config import configuration
from ..prefill import Prefill

URLpre = configuration["URLpre"]


def venue_booking_lecture_function(day, date, time, venue_id):
    user = session["user"]
    token = session["token"]
    if not token:
        return render_template("error.html", message="You are not logged in.")
    headers = {"Authorization": f"Bearer {token}"}

    venue_details = fetch_venue_by_id(headers, venue_id)

    prefill = Prefill(venue_id, start_date=date, end_date=None, with_time=time)

    return admin_routs.add_lecture_one_function(prefill=prefill) # må legge til context argument som må reflekteres i funksjonen
    # return render_template("venue_booking_lecture.html", user=user, day=day, date=date, time=time, venue_details=venue_details, venue_id=venue_id)


def venue_booking_exam_function(day, date, time, venue_id):
    user = session["user"]
    token = session["token"]
    if not token:
        return render_template("error.html", message="You are not logged in.")
    headers = {"Authorization": f"Bearer {token}"}

    venue_details = fetch_venue_by_id(headers, venue_id)

    prefill = Prefill(venue_id, start_date=date, end_date=None, with_time=time)

    return exam_routs.template_exam_function(prefill=prefill)

"""def venue_fetch_courses():
    user = session["user"]
    token = session["token"]
    if not token:
        return render_template("error.html", message="You are not logged in.")
    headers = {"Authorization": f"Bearer {token}"}
"""
