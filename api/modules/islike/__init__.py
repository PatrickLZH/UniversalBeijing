from flask import Blueprint

islike_blu = Blueprint('islike', __name__, url_prefix='/islike')
                  
from . import views