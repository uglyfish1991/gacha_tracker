from flask import Flask, Blueprint, render_template, request, redirect, url_for
from .models import PullRecord
from . import db
from datetime import date
# import matplotlib
# matplotlib.use("Agg")
# import matplotlib.pyplot as plt


my_view = Blueprint("my_view", __name__)

@my_view.route("/")
def home():
    form_type = request.args.get('form_type', None)
    return render_template("index.html",  form_type = form_type)

@my_view.route("/form_select", methods=["POST"])
def form_select():
    print(f"{request.form.get('games_names')}")
    if request.form.get("games_names") == "wor":
        form_type = "wor"
    else:
        form_type="other"
    return render_template("form.html", form_type=form_type)

@my_view.route("/records")
def view_records():
        record_collection = PullRecord.query.all()
        return render_template("record.html", record_collection = record_collection,)


# @my_view.route("/form_select", methods=["POST"])
# def form_select():
#     print(f"{request.form.get('games_names')}")
#     if request.form.get("games_names") == "wor":
#         form_type = "wor"
#     else:
#         form_type="other"
#     return redirect(url_for("my_view.home", form_type=form_type))

@my_view.route("/add_wor", methods = ["POST"])
def add_wor():
    new_record = PullRecord(
        timestamp = date.fromisoformat(request.form.get('summon_date')),
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