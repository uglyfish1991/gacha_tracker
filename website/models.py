from . import db
from datetime import datetime
from sqlalchemy import func

class PullRecord(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    game_name = db.Column(db.String(300), nullable = False)
    timestamp = db.Column(db.DateTime, nullable=False)
    currency_used = db.Column(db.String(300), nullable=False)
    summon_type = db.Column(db.String(300), nullable=False)
    character_name = db.Column(db.String(300), nullable=False)
    character_rarity = db.Column(db.String(300), nullable=False)
    character_faction = db.Column(db.String(300), nullable=False)
    second_faction = db.Column(db.String(300), nullable=False)
    lord_hero = db.Column(db.Boolean, default = False)
    owned_before = db.Column(db.Boolean, default = False)
