from app.routes.animes_route import bp as bp_animes
from flask import Flask

def init_app(app: Flask):
    app.register_blueprint(bp_animes)