from flask import Flask, redirect, render_template, request, session
import requests
from datetime import datetime, timezone
import jwt
from ..config import configuration
from ..user import User


URLpre = configuration["URLpre"]      #"https://localhost:7042/api/v1/"

def login_function():
    gokstadmail = request.form.get("gokstadmail")
    password = request.form.get("password")

    data = {
        "GokstadEmail": gokstadmail,    # "nora.moe@gokstadakademiet.no",   johannes.andersen@gokstadakademiet.no, MZHlhk54 (1)
        "Password": password,           # "POGxar99"                        ole.larsen@gokstadakademiet.no, UQTyho81 (10)
    }

    url_ext = "login"
    url = URLpre + url_ext

    response = requests.post(url, verify=False, json=data)

    if not response.ok:
        err_msg = "Kunne ikke logge deg inn.\n Feil brukernavn og/eller passord."
        return render_template("index.html", err_msg=err_msg)

    token = response.text
    decoded_token = jwt.decode(token, options={'verify_signature': False})
    # print(decoded_token)

    expiration = decoded_token['exp']
    # expiration_datetime = datetime.utcfromtimestamp(expiration)
    expiration_datetime = datetime.fromtimestamp(expiration)
    gokmail = decoded_token["gokstademail"]
    first = decoded_token["firstname"]
    last = decoded_token["lastname"]
    id = decoded_token["id"]
    role = decoded_token["role"]
    email2 = decoded_token["email2"]
    email3 = decoded_token["email3"]
    link = decoded_token["link"]

    session["user"] = User(id, gokmail, first, last, role, email2, email3, link)
    session["token"] = token
    session['token_expiration'] = expiration
    session['token_expiration_dt'] = expiration_datetime

    return redirect("/")


def logout_function():
    session.clear()
    return redirect("/")
