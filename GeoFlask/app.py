from flask import Flask, render_template, request
from flask_session import Session
import urllib3
from utility.config import configuration
from helper import *
import utility.rout_funcs.login_routs as lg_routs
import utility.rout_funcs.calendar_routs as cal_routs
import utility.rout_funcs.errorhandlers as err_handl
import utility.rout_funcs.admin_routs as adm_routs
import utility.rout_funcs.assignment_routs as ass_routs
import utility.rout_funcs.lecture_routs as lec_routs
import utility.rout_funcs.examImp_routs as exImp_routs
import utility.rout_funcs.a_admin_venue_routs as ven_routs
import utility.rout_funcs.a_student_resources_routs as stud_rescr

urllib3.disable_warnings()

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# MY GLOBAL VARIABLES
URLpre = configuration["URLpre"]                   # "https://localhost:7042/api/v1/"

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# ------------------------------------------------------------------



@app.route("/")
def index():
    if "user" not in session or datetime.now() > session['token_expiration_dt']:        # timezone.utc
        session.clear()
    user = session["user"] if "user" in session else False
    return render_template("index.html", user=user)

@app.route("/login", methods=["POST"])
def login():
    return lg_routs.login_function()

@app.route("/logout")
def logout():
    return lg_routs.logout_function()

@app.route("/calendar")
@login_required(roles=None)
def calendar():
    return cal_routs.calendar_function()

# ------------------------------------------------------------------
@app.route("/admin_venue")
@login_required(roles=["teacher", "admin"])
def admin_venue():
    return ven_routs.get_venues_and_events()

@app.route("/StudentResources")
@login_required(roles=None)
def student_resources():
    return stud_rescr.get_resources()
# ------------------------------------------------------------------


@app.route("/Assignment/<int:id>")
@login_required(roles=None)
def assignment_id(id):
    return ass_routs.assignment_id_function(id)

@app.route("/Lecture/<int:id>", methods=["get", "post"])
@login_required(roles=None)
def lecture_id(id):
    return lec_routs.lecture_id_function(id)

# @app.route("/Lecture/<int:id>", methods=["post"])
# @login_required(roles=["teacher, admin"])
# def lecture_id_post(id):
#     return lec_routs.lecture_id_post_function(id)

@app.route("/ExamImplementation/<int:id>")
@login_required(roles=None)
def examImplementation_id(id):
    return exImp_routs.examImplementation_id_function(id)

@app.route("/admin")
@login_required(roles=["teacher", "admin"])
def admin():
    return adm_routs.admin_function()

@app.route("/admin_lecture")
@login_required(roles=["teacher", "admin"])
def admin_lecture():
    return adm_routs.admin_lecture_function()

@app.route("/add_lecture")
@login_required(roles=["teacher", "admin"])
def add_lecture():
    return adm_routs.add_lecture_function()

@app.route("/add_lecture_one")
@login_required(roles=["teacher", "admin"])
def add_lecture_one():
    return adm_routs.add_lecture_one_function()

@app.route("/conf_lecture_one", methods=["POST"])
@login_required(roles=["teacher", "admin"])
def conf_lecture_one():
    return adm_routs.conf_lecture_one_function()

@app.errorhandler(404)
def page_not_found(error):
    return err_handl.page_not_found_function(error)

@app.errorhandler(500)
def internal_server_error(error):
    return err_handl.internal_server_error_function(error)
