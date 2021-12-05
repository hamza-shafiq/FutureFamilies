from pathlib import Path
from flask import Blueprint

PATH = str(Path(__file__).resolve().parents[2]) + '\\templates\\'

bp = Blueprint('home', __name__, template_folder=PATH)

from app.routes.home import routes
