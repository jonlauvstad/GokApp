import requests
from flask import Flask, render_template, request, url_for, flash, jsonify

from utility.rout_funcs import a_venue_calendar_routs
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
import utility.rout_funcs.a_venue_calendar_routs as ven_routs
import utility.rout_funcs.a_venue_booking_routs as ven_book_routs
import utility.rout_funcs.a_student_resources_routs as stud_rescr
import utility.api_funcs.api_1 as api_1
import utility.rout_funcs.alert_routs as alert_routs
import utility.rout_funcs.exam_routs as exam_routs
from utility.util_funcs import format_datetime
import utility.rout_funcs.venue_routs as venue_routs
import utility.rout_funcs.courseImp_routs as courseImp_routs

urllib3.disable_warnings()

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.jinja_env.filters['date'] = format_datetime
app.jinja_env.add_extension('jinja2.ext.do')


# MY GLOBAL VARIABLES
URLpre = configuration["URLpre"]                   # "https://localhost:7042/api/v1/"

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# ----------------------------------------------------
# ---------------- MAIN ------------------------------
# ----------------------------------------------------

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

# ----------------------------------------------------
# ---------------- VENUE -----------------------------
# ----------------------------------------------------


@app.route("/venue_calendar")
@login_required(roles=["teacher", "admin"])
def venue_calendar():
    return ven_routs.venue_calendar_function()


@app.route("/book_from_venue", methods=['GET'])
@login_required(roles=["teacher", "admin"])
def book_from_venue():
    date = request.args.get('date')
    day = request.args.get('day')
    time = request.args.get('time')
    venue_id = request.args.get('venue_id')
    return ven_routs.venue_booking_data(date, day, time, venue_id)


@app.route("/book_from_venue_lecture", methods=["GET", "POST"])
@login_required(roles=["teacher", "admin"])
def venue_booking_lecture():
    date = request.args.get('date')
    day = request.args.get('day')
    time = request.args.get('time')
    venue_id = request.args.get('venue_id')
    return ven_book_routs.venue_booking_lecture_function(date, day, time, venue_id)


@app.route("/book_from_venue_exam", methods=["GET", "POST"])
@login_required(roles=["teacher", "admin"])
def venue_booking_exam():
    date = request.args.get('date')
    day = request.args.get('day')
    time = request.args.get('time')
    venue_id = request.args.get('venue_id')
    return ven_book_routs.venue_booking_exam_function(date, day, time, venue_id,)


@app.route('/venue_cal_single_day/<date>', methods=['GET'])
@login_required(roles=["teacher", "admin"])
def venue_cal_single_view(date):
    return ven_routs.venue_cal_single_day(date)


@app.route('/venue_add_lecture') # generell og ikke spesifisert booking
def venue_add_lecture():
    # Retrieve the date from the query parameter, default to today if not provided
    date = request.args.get('date', default=datetime.now().strftime('%Y-%m-%d'))

    return render_template('admin/lecture/add_lecture_one.html', default_date=date)


@app.route('/set_date', methods=['POST'])
def set_date():
    start_date = request.form.get('startDateTime')
    end_date = request.form.get('endDateTime')
    num_days = a_venue_calendar_routs.calculate_num_days(start_date, end_date)

    return redirect(url_for('venue_calendar', start_date=start_date, end_date=end_date, num_days=num_days))


@app.route("/StudentResources")
@login_required(roles=None)
def student_resources():
    return stud_rescr.get_resources()

# ----------------------------------------------------
# ---------------- ASSIGNMENT ------------------------
# ----------------------------------------------------

@app.route('/admin_assignment')
@login_required(roles=['teacher', 'admin'])
def admin_assignment():
    return ass_routs.admin_assignment_function()


@app.route("/template_assignment", methods=["GET", "POST"])
@login_required(roles=["teacher", "admin"])
def template_assignment():
    return ass_routs.template_assignment_function()


@app.route("/get_assignments")
@login_required(roles=["teacher", "admin"])
def get_assignments():
    return ass_routs.get_assignments()


@app.route('/get_success')
def get_success():
    return render_template('admin/assignment/get_success.html')


@app.route("/implementation_assignment/delete/<int:assignment_id>")
@login_required(roles=["teacher", "admin"])
def see_assignments(assignment_id):
    # return exImp_routs.examImp_delete(exam_id)
    return redirect(f"/Assignment/{assignment_id}")


@app.route("/conf_assignment", methods=["GET", "POST"])
@login_required(roles=["teacher", "admin"])
def conf_assignment():
    # print("Recieved data:", request.form)
    return ass_routs.conf_assignment_function()



@app.route("/Assignment/<int:id>", methods=["GET", "POST"])
@login_required(roles=None)
def assignment_id(id):
    """Results (assignment.link) from DELETE / PUT"""
    # print(f"\n\t ➡️ Request method: {request.method}, ID: {id}")
    return ass_routs.assignment_id_function(id)



@app.route("/api/assignment/<int:id>")
@login_required(roles=None)
def api_assignment_id(id):
    """Results (assignment.link) from POST"""
    return api_1.api_assignment_id_function(id)

@app.route("/Assignment")
@login_required(roles=None)
def assignment():
    return ass_routs.assignment_getAll_function()


# ----------------------------------------------------

@app.route('/admin_assignment/select/<action>', methods=['GET'])
@login_required(roles=['teacher', 'admin'])
def select_assignment(action):
    assignments = ass_routs.assignment_getAll_function()
    return render_template('admin/assignment/select_assignment.html', assignments=assignments, action=action)


"""
@app.route('/confirmation_page/<int:id>/<action>')
@login_required(roles=['teacher', 'admin'])
def confirmation_page(id, action):
    # Fetch details of the assignment to show on confirmation
    assignment_details = ass_routs.assignment_id_function(id)
    return render_template('admin/assignment/deleteOrUpdateConf.html', assignment=assignment_details, action=action)

"""
@app.route('/admin_assignment/update/<int:id>', methods=['GET', 'POST'])
@login_required(roles=['teacher', 'admin'])
def update_assignment(id):
    app.logger.debug(f"Update endpoint hit with ID: {id}")
    if request.method == 'POST':
        return ass_routs.assignment_update_function(id)

    return render_template('admin/assignment/update_assignment.html', id=id)


@app.route('/admin_assignment/delete/<int:id>', methods=['GET', 'POST'])
@login_required(roles=['teacher', 'admin'])
def delete_assignment(id):
    app.logger.debug(f"Delete endpoint hit with ID: {id}")
    if request.method == 'POST':
        return ass_routs.assignment_delete_function(id)

    return render_template('admin/assignment/delete_assignment.html', id=id)


# ----------------------------------------------------
# ---------------- LECTURE ---------------------------
# ----------------------------------------------------


@app.route("/Lecture/<int:id>", methods=["get", "post"])
@login_required(roles=None)
def lecture_id(id):
    return lec_routs.lecture_id_function(id)

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

@app.route("/search_lecture")
@login_required(roles=["teacher", "admin"])
def search_lecture():
    return adm_routs.search_lecture_function()

@app.route("/search_lecture_result", methods=["POST"])
@login_required(roles=None)
def search_lecture_result():
    return lec_routs.lecture_search_result_function()

@app.route("/lecture/multiple", methods=["GET", "POST"])
@login_required(roles=["teacher", "admin"])
def lecture_multiple():
    return lec_routs.lecture_multiple_function()

@app.route("/add_lecture_multiple")
@login_required(roles=["teacher", "admin"])
def lecture_add_multiple():
    return lec_routs.lecture_add_multiple_function()

@app.route("/alert_see_unseen")
@login_required(roles=None)
def alert_see_unseen():
    return alert_routs.alert_see_unseen_function()

# ----------------------------------------------------
# ---------------- EXAM ------------------------------
# ----------------------------------------------------

@app.route("/admin_exam")
@login_required(roles=["teacher", "admin"])
def admin_exam():
    return exam_routs.admin_exam_function()

@app.route("/template_exam", methods=["GET", "POST"])
@login_required(roles=["teacher", "admin"])
def template_exam():
    return exam_routs.template_exam_function()

@app.route("/conf_exam", methods=["POST"])
@login_required(roles=["teacher", "admin"])
def conf_exam():
    return exam_routs.conf_exam_function()

@app.route("/Exam/<int:id>", methods=["GET", "POST"])
@login_required(roles=None)
def exam_id(id):
    return exam_routs.exam_id_function(id)

@app.route("/Exam")
@login_required(roles=None)
def exam():
    return exam_routs.exam_getAll_function()

@app.route("/ExamImplementation/<int:id>")
@login_required(roles=None)
def examImplementation_id(id):
    return exImp_routs.examImplementation_id_function(id)

@app.route("/ExamImplementation", methods=["GET", "POST"])
@login_required(roles=None)
def examImplementation():
    return exImp_routs.examImplementation_function()

@app.route("/ExamImplementation/Exam/<int:exam_id>", methods=["GET", "POST"])
@login_required(roles=None)
def examImplementation_ExamId(exam_id):
    return exImp_routs.examImplementation_ExamId_function(exam_id)


@app.route("/implementation_exam")
@login_required(roles=["teacher", "admin"])
def implementation_exam():
    return exImp_routs.examImp_start()

# DENNE BØR ENDRES TIL DEN I L 253, DVS DENNE FJERNES, OG URL-HENVISNINGENE I HTML ENDRES ACCORDINGLY: examImp_start.html - eller bare redirecte
@app.route("/implementation_exam/delete/<int:exam_id>")
@login_required(roles=["teacher", "admin"])
def implementation_exam_see(exam_id):
    # return exImp_routs.examImp_delete(exam_id)
    return redirect(f"/ExamImplementation/Exam/{exam_id}")

@app.route("/implementation_exam/register/<int:exam_id>")
@login_required(roles=["teacher", "admin"])
def implementation_exam_register(exam_id):
    return exImp_routs.examImp_register(exam_id)

@app.route("/implementation_exam/group/<int:exam_id>")
@login_required(roles=["teacher", "admin"])
def implementation_exam_group(exam_id):
    return exImp_routs.examImp_group(exam_id)

@app.route("/ExamGroup/<int:exam_id>", methods=["GET", "POST"])
@login_required(roles=["teacher", "admin"])
def exam_group(exam_id):
    return exImp_routs.exam_group(exam_id)

# ----------------------------------------------------
# ---------------- VENUE MANAGEMENT ------------------
# ----------------------------------------------------

@app.route("/Venue/<int:id>")
@login_required(roles=None)
def venue_id(id):
    return venue_routs.venue_id_function(id)

@app.route("/venue_admin")
@login_required(roles=["admin"])
def venue_admin():
    return venue_routs.venue_admin_function()

@app.route("/venue_register", methods=["GET", "POST"])
@login_required(roles=["admin"])
def venue_register():
    return venue_routs.venue_register_function()

@app.route("/venue_update/<int:id>", methods=["GET", "POST"])
@login_required(roles=["admin"])
def venue_update(id):
    return venue_routs.venue_update_function(id)

@app.route("/venue_delete/<int:id>")
@login_required(roles=["admin"])
def venue_delete(id):
    return venue_routs.venue_delete_function(id)

@app.route("/CourseImplementation/<int:id>")
@login_required(roles=None)
def courseImplementation_id(id):
    return courseImp_routs.courseImp_id_function(id)

@app.route("/Course/<int:id>")
@login_required(roles=None)
def course_id(id):
    return courseImp_routs.course_id_function(id)

# API ROUTS HERE!
@app.route("/api/venue", methods=["GET"])
@login_required(roles=None)
def api_get_venues():
    return api_1.api_get_venues_func()

# ----------------------------------------------------
# ---------------- ALERTS ----------------------------
# ----------------------------------------------------

@app.route("/api/alert/user")
@login_required(roles=None)
def api_update_unseen_alerts_user():
    pass
    # return api_1.api_update_unseen_alerts_user_func()

@app.route("/api/alert/user/<int:userId>")
@login_required(roles=None)
def api_get_alerts_user(userId):
    return api_1.api_get_alerts_user_func(userId)

@app.route("/api/alert/<int:alertId>")
@login_required(roles=None)
def api_update_alert_id(alertId):
    return api_1.api_update_alert_id_func(alertId)

@app.route("/api/exam/<int:id>")
@login_required(roles=None)
def api_exam_id(id):
    return api_1.api_exam_id_function(id)

# ERROR-HANDELERS HERE!
@app.errorhandler(404)
def page_not_found(error):
    return err_handl.page_not_found_function(error)

@app.errorhandler(500)
def internal_server_error(error):
    return err_handl.internal_server_error_function(error)

# ----------------------------------------------------
# ---------------- EKSTERNT --------------------------
# ----------------------------------------------------


@app.route('/student_resources/daily', methods=["GET"])
@login_required(roles=None, )
def get_daily_resource():
    url = "https://api.github.com/search/repositories"
    query = "backend+language:python"
    params = {
        "q": query,
        "sort": "stars",
        "order": "desc"
    }
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers, params=params)

    data = response.json()

    repositories = [{
        'name': repo['name'],
        'url': repo['html_url'],
        'description': repo['description'],
        'stars': repo['stargazers_count'],
    } for repo in data['items']]

    return jsonify(repositories)
