from flask import session, redirect
from datetime import datetime
from functools import wraps

# def login_required(func):
#     @wraps(func)
#     def is_logged_in(*args, **kwargs):
#         if "user" not in session or datetime.now() > session['token_expiration_dt']:
#             session.clear()
#             return redirect("/")
#         return func(*args, **kwargs)
#     return is_logged_in

def login_required(roles):
    @wraps(roles)
    def decorator(func):
        @wraps(func)
        def is_logged_in(*args, **kwargs):
            if "user" not in session or datetime.now() > session['token_expiration_dt']:
                session.clear()
                return redirect("/")
            if roles:
                if session["user"].role not in roles:
                    return redirect("/")
            return func(*args, **kwargs)
        return is_logged_in
    return decorator