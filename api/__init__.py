from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
# from flask_session import Session
from api.utils.log_utils import setup_log
from config.config import config_dict

db = SQLAlchemy()
redis_store = None

def create_app(config_name):
    app = Flask(__name__)
    config = config_dict.get(config_name)
    app.secret_key = config.SECRET_KEY
    setup_log(log_file='logs/root.log', level=config.LEVEL_LOG)
    app.config.from_object(config)
#     Session(app)
    db.init_app(app)

    global redis_store
    # 创建redis的连接对象
    redis_store = StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)

    from api.modules.auth import auth_blu
    app.register_blueprint(auth_blu)

    from api.modules.files import files_blu
    app.register_blueprint(files_blu)

    from api.modules.message import message_blu
    app.register_blueprint(message_blu)

    from api.modules.islike import islike_blu
    app.register_blueprint(islike_blu)

    from api.modules.documents import documents_blu
    app.register_blueprint(documents_blu)

    return app
