import logging
import os
from redis import StrictRedis
import sys

class Config:
    # ES_PASSWORD = '8Hjlfr0sb7RZFW2L*LuA'
    DEBUG = True
    LEVEL_LOG = logging.INFO
    
    SECRET_KEY = 'a3#x@L9!zQmKp2$vXq8L'
    
    # SQL_HOST = "rm-uf6z891lon6dxuqblqo.mysql.rds.aliyuncs.com"
    # SQL_USERNAME = "ubr123"
    # SQL_PASSWORD = "ubr321"
    # SQL_PORT = "3306"
    # SQL_DB = "ubr_rag"
    SQL_HOST = '127.0.0.1'
    SQL_USERNAME = 'root'
    SQL_PASSWORD = '1234'
    SQL_PORT = 3306
    SQL_DB = 'my_project'
    JSON_AS_ASCII = False
    # 数据库的配置
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{SQL_USERNAME}:{SQL_PASSWORD}@{SQL_HOST}:{SQL_PORT}/{SQL_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6380

    # 指定session使用什么来存储
    SESSION_TYPE = 'redis'
    # 指定session数据存储在后端的位置
    SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    # jwttoken-Redis有效期， 单位：秒
    JWT_TOKEN_REDIS_EXPIRES = 60 * 60 * 24

class DevConfig(Config):
    pass

class ProConfig(Config):
    pass
    # LEVEL_LOG = logging.ERROR
    # DEBUG = False
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:1234@127.0.0.1:3306/my_project"

class TestConfig(Config):
    pass

config_dict = {
    'dev': DevConfig,
    'pro': ProConfig,
    'test': TestConfig,
}
