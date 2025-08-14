from flask import Blueprint
from flask_restful import Api
from api.modules.message.messagechat import MessageView, MessageSession, MessageAll

message_blu = Blueprint('message', __name__, url_prefix='/message')
api = Api(message_blu)
api.add_resource(MessageView,'/', strict_slashes=False)
api.add_resource(MessageSession,'/session')
api.add_resource(MessageAll,'/all')