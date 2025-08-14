from flask import Blueprint
from flask_restful import Api
from api.modules.files.views import FileView

files_blu = Blueprint('files', __name__, url_prefix='/files')
api = Api(files_blu)
api.add_resource(FileView,'/', strict_slashes=False)