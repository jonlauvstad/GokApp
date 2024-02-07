from flask import Flask, redirect, render_template, request, session


def page_not_found_function(error):
    code = "404 Not Found"
    user = None
    if "user" in session:
        user = session['user']
    return render_template('server_error.html', error=error, user=user, code=code), 404

def internal_server_error_function(error):
    code = "500 Internal Server Error"
    user = None
    if "user" in session:
        user = session['user']
    return render_template('server_error.html', error=error, user=user, code=code), 500
