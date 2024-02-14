from flask import render_template, session
from ..config import configuration
import requests


URLpre = configuration["URLpre"]


def get_venues():
    api_url = URLpre + "Venue"
    token = session.get("token")

    if token:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(api_url, headers=headers, verify=False)

        if response.ok:
            venues = response.json()
            return render_template("admin_venue.html", venues=venues)
        else:
            print(f"Error fetching venue data: {response.status_code}")
            # Consider redirecting to login or showing an error message
            return render_template("error.html", message="Failed to fetch venue data.")
    else:
        # Token not found in session, redirect to login or show an error
        return render_template("error.html", message="You are not logged in.")

# if __name__ == '__main__':
#     get_venues()



