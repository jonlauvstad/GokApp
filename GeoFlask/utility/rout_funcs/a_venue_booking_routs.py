from flask import render_template, session, request, flash
import requests
from datetime import datetime, timedelta
from dateutil import parser

from .a_venue_calendar_routs import fetch_venue_by_id
from ..config import configuration

URLpre = configuration["URLpre"]


def venue_booking_lecture_function(day, date, time, venue_id):
    user = session["user"]
    token = session["token"]
    if not token:
        return render_template("error.html", message="You are not logged in.")
    headers = {"Authorization": f"Bearer {token}"}

    venue_details = fetch_venue_by_id(headers, venue_id)

    return render_template("venue_booking_lecture.html", user=user, day=day, date=date, time=time, venue_details=venue_details, venue_id=venue_id)


def venue_booking_exam_function(day, date, time, venue_id):
    user = session["user"]
    token = session["token"]
    if not token:
        return render_template("error.html", message="You are not logged in.")
    headers = {"Authorization": f"Bearer {token}"}

    venue_details = fetch_venue_by_id(headers, venue_id)

    return render_template("venue_booking_exam.html", user=user, day=day, date=date, time=time, venue_details=venue_details, venue_id=venue_id)
