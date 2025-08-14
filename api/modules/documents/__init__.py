from flask import Blueprint

documents_blu = Blueprint('documents', __name__, url_prefix='/documents')
from . import views
