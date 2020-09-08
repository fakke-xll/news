from flask import Blueprint

bp = Blueprint('department',__name__,url_prefix='/department/')

from . import views