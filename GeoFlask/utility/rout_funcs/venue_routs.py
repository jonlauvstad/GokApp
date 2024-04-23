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
    return render_template("venue.html", venue=dic, user=user)

def venue_admin_function():
    user = session["user"]

    url_ext = f"Venue"
    url = URLpre + url_ext
    headers = {"Authorization": f"Bearer {session['token']}"}
    response = requests.get(url, verify=False, headers=headers)

    if not response.ok:
        abort(404)

    lOfdics = response.json()
    venues = [item for item in lOfdics if item["name"] != 'Hjemme']

    return render_template("venue_admin.html", user=user, venues=venues)

def venue_register_function():
    user = session["user"]
    headers = {"Authorization": f"Bearer {session['token']}"}

    if request.method == "GET":
        url_ext = f"Location"
        url = URLpre + url_ext
        response = requests.get(url, verify=False, headers=headers)
        if not response.ok:
            abort(404)
        lOfdics = response.json()
        locations = [item for item in lOfdics if item["name"] != 'Internett']
        return render_template("venue_register.html", user=user, locations=locations)

    name= request.form.get("name")
    description = request.form.get("description")
    locationId= request.form.get("locationId")
    streetAddress = request.form.get("streetAddress")
    postCode = request.form.get("postCode")
    city = request.form.get("city")
    capacity= request.form.get("capacity")

    data = {
        "Name": name,
        "Description": description,
        "LocationId": locationId,
        "StreetAddress": streetAddress,
        "PostCode": postCode,
        "City": city,
        "Capacity": capacity
    }

    url_ext = f"Venue"
    url = URLpre + url_ext
    response = requests.post(url, verify=False, headers=headers, json=data)
    if not response.ok:
        abort(404)
    dic = response.json()

    return render_template("venue.html", venue=dic, user=user, headl_prefix="NYTT ")

def venue_update_function(id):
    user = session["user"]
    headers = {"Authorization": f"Bearer {session['token']}"}
    url_ext = f"Venue/{id}"
    url = URLpre + url_ext

    if request.method == "GET":
        response = requests.get(url, verify=False, headers=headers)
        if not response.ok:
            abort(404)
        dic = response.json()

        url_ext = f"Location"
        url = URLpre + url_ext
        response = requests.get(url, verify=False, headers=headers)
        if not response.ok:
            abort(404)
        lOfdics = response.json()
        locations = [item for item in lOfdics if item["name"] != 'Internett']

        return render_template("venue_update.html", user=user, venue=dic, locations=locations)

    # POST: returnere "venue.html" headl_prefix="ENDRET "
    name = request.form.get("name")
    description = request.form.get("description")
    locationId = request.form.get("locationId")
    streetAddress = request.form.get("streetAddress")
    postCode = request.form.get("postCode")
    city = request.form.get("city")
    capacity = request.form.get("capacity")

    data = {
        "Name": name,
        "Description": description,
        "LocationId": locationId,
        "StreetAddress": streetAddress,
        "PostCode": postCode,
        "City": city,
        "Capacity": capacity
    }

    response = requests.put(url, verify=False, headers=headers, json=data)
    if not response.ok:
        abort(404)
    dic = response.json()
    return render_template("venue.html", venue=dic, user=user, headl_prefix="ENDRET ")
    # return {
    #     "URL": url,
    #     "Date": data
    # }


def venue_delete_function(id):
    user = session["user"]
    headers = {"Authorization": f"Bearer {session['token']}"}
    url_ext = f"Venue/{id}"
    url = URLpre + url_ext
    response = requests.delete(url, verify=False, headers=headers)
    if not response.ok:
        abort(404)
    dic = response.json()
    return render_template("venue.html", venue=dic, user=user, headl_prefix="SLETTET ", delete=True)