from flask import Blueprint

bp = Blueprint('superadmin',__name__,url_prefix='/sp/')

from . import views