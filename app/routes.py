from flask import Blueprint, render_template
from flask_login import login_required, current_user

routes_bp = Blueprint("routes", __name__)

@routes_bp.route("/")
# @login_required
def home():
    return render_template("app/home.html", user=current_user)

@routes_bp.route("/talks")
def talks():
    return render_template("app/talks.html", user=current_user)

@routes_bp.route("/settings")
def settings():
    return render_template("app/settings.html", user=current_user)
