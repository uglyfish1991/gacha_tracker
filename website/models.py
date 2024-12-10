from . import db

class PullRecord(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    currency_used = db.Column(db.String(300), nullable=False)
    event_active = db.Column(db.Boolean, default = False)
    event_name = db.Column(db.String(300))
    character_name = db.Column(db.String(300), nullable=False)
    character_rarity = db.Column(db.String(300), nullable=False)
    character_faction = db.Column(db.String(300), nullable=False)
    owned_before = db.Column(db.Boolean, default = False)