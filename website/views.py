from flask import Flask, Blueprint, render_template, request, redirect, url_for
from .models import PullRecord
from . import db
# import matplotlib
# matplotlib.use("Agg")
# import matplotlib.pyplot as plt


my_view = Blueprint("my_view", __name__)

@my_view.route("/")
def home():
    form_type = request.args.get('form_type', None)
    return render_template("index.html", form_type=form_type)

@my_view.route("/form_select", methods=["POST"])
def form_select():
    if request.form.get("games_names") == "wor":
        form_type = "wor"
    else:
        form_type="other"
    return redirect(url_for("my_view.home", form_type=form_type))