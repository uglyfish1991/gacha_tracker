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
    record_collection = PullRecord.query.all()
    return render_template("index.html", record_collection = record_collection, form_type = form_type)

@my_view.route("/form_select", methods=["POST"])
def form_select():
    if request.form.get("games_names") == "wor":
        form_type = "wor"
    else:
        form_type="other"
    return redirect(url_for("my_view.home", form_type=form_type))

@my_view.route("/add_wor", methods = ["POST"])
def add_wor():
    new_record = PullRecord(
        currency_used = request.form.get("currency_used"),
        summon_type = request.form.get("summon_type"),
        character_name = request.form.get("character_name"),
        character_rarity = request.form.get("rarity"),
        character_faction = request.form.get("faction"),
        second_faction = request.form.get("second_faction"),
        lord_hero = True if request.form.get("lord_hero") == "yes" else False,
        owned_before = True if PullRecord.query.filter_by(character_name=request.form.get("character_name")).first() else False
    )
    db.session.add(new_record)
    db.session.commit()
    return redirect(url_for("my_view.home"))