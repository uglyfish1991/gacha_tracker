from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

post_gres_uri = os.environ.get("post_gres_uri")

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_DATABASE_URI'] = post_gres_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .views import my_view
    app.register_blueprint(my_view)

    from .models import PullRecord
    with app.app_context():
        db.create_all()

    return app

    