from flask import Flask, Blueprint, render_template, request, redirect, url_for
from .models import PullRecord
from . import db
from .game_info import wor_info, genshin_info, omni_info
from datetime import date
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sqlalchemy import func

my_view = Blueprint("my_view", __name__)

def count_from_last_five_star(game):
     counter = 0
     for record in PullRecord.query.filter_by(game_name=game).order_by(PullRecord.id.desc()).all():
          counter +=1
          if record.character_rarity == 5:
               return counter
          
def draw_example_graph(game):

#----------------------------------------------------------------------------------------------------------------------------------------------
#! Explaination for future me! 

        #     # Query the database session to get the count of records for each character rarity
        #* rarity_counts = db.session.query(
        #     # Select the character_rarity field from the PullRecord model (the rarity of the character)
        #*     PullRecord.character_rarity, 

        #    # Count the number of records with each unique rarity
        #*     func.count(PullRecord.id).label('count')  
        #     # `func.count(PullRecord.id)` is used to count how many records match a particular rarity. 
        #     # We label the count as 'count' to make it easier to reference in the result set.
        #* ).filter_by(
        #     # Filter the records to include only those that match the given game name
        #*     game_name=game  
        #     # The `filter_by(game_name=game)` ensures that only records from the specified `game_name` are included in the count.
        #* ).group_by(
        #     # Group the records by the `character_rarity` field to calculate the count for each rarity
        #*     PullRecord.character_rarity  
        #     # This groups the result set by the `character_rarity`, so that the count is calculated per rarity value.
        #* ).all()
        # # `all()` retrieves all the results and returns them as a list of tuples where each tuple is (rarity, count).

#---------------------------------------------------------------------------------------------------------------------------------------------------
    rarity_counts = db.session.query(PullRecord.character_rarity, func.count(PullRecord.id).label('count')).filter_by(game_name=game).group_by(PullRecord.character_rarity).all()
    plt.style.use('ggplot')
    rarities = [item[0] for item in rarity_counts]
    counts = [item[1] for item in rarity_counts]
    bar_colours = ["green", "blue", "purple", "gold"]
    plt.bar(rarities, counts, color = bar_colours)
    plt.xlabel('Character Rarity')
    plt.xticks(rarities)
    plt.ylabel('Count')
    plt.title(f'Count of Characters by Rarity for {game}')
    plt.savefig(f'website/static/images/rarity_frequency_plot.png', dpi=250)
    plt.clf()


@my_view.route("/")
def home():
    form_type = request.args.get('form_type', None)
    return render_template("index.html",  form_type = form_type)

@my_view.route("/form_select", methods=["POST"])
def form_select():
    print(f"{request.form.get('games_names')}")
    if request.form.get("games_names") == "wor":
        form_type = "wor"
        game_stats = wor_info
    elif request.form.get("games_names") == "genshin":
         form_type = "genshin"
         game_stats = genshin_info
    elif request.form.get("games_names") == "omni":
         form_type = "omni"
         game_stats = omni_info
    else:
        form_type="other"
    record_collection = PullRecord.query.filter_by(game_name=game_stats["game_name"]).order_by(PullRecord.id.desc()).limit(10).all()
    last_five_star = count_from_last_five_star(game_stats["game_name"])
    draw_example_graph(game_stats["game_name"])
    return render_template("form.html", form_type=form_type, game_stats = game_stats, record_collection=record_collection, last_five_star = last_five_star)

@my_view.route("/records", endpoint='view_records')
def view_records():
        record_collection = PullRecord.query.all()
        record_collection.reverse()
        return render_template("record.html", record_collection = record_collection)

@my_view.route("/records/<specific_game>")
def view_specific_records(specific_game):
        print(specific_game)
        record_collection = PullRecord.query.filter_by(game_name=specific_game).all()
        record_collection.reverse()
        return render_template("record.html", record_collection = record_collection)

@my_view.route("/add_record", methods = ["POST"])
def add_wor():
    new_record = PullRecord(
        timestamp = date.fromisoformat(request.form.get('summon_date')),
        game_name = request.form.get("game_name"),
        currency_used = request.form.get("currency_used"),
        summon_type = request.form.get("summon_type"),
        character_name = request.form.get("character_name"),
        character_rarity = request.form.get("rarity"),
        character_faction = request.form.get("faction"),
        second_faction = request.form.get("second_faction"),
        lord_hero = True if request.form.get("field_three") == "yes" else False,
        owned_before = True if PullRecord.query.filter_by(character_name=request.form.get("character_name")).first() else False
    )
    db.session.add(new_record)
    db.session.commit()
    return redirect(url_for("my_view.home"))

@my_view.route("/filter_rarity", methods = ["POST"])
def filter_rarity():
    rarity_selected = request.form.get('rarity')
    if rarity_selected == "all":
         record_collection = PullRecord.query.all()
    else:
        record_collection = PullRecord.query.filter_by(character_rarity=rarity_selected).all()
    record_collection.reverse()
    return render_template("record.html", record_collection = record_collection)



@my_view.route("/delete/<record_id>")
def delete(record_id):
    record = PullRecord.query.filter_by(id=record_id).first()
    db.session.delete(record)
    db.session.commit()
    return redirect(url_for("my_view.view_records"))