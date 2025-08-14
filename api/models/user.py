from datetime import datetime
from api import db
from api.models.base import BaseModels

class UserInfo(BaseModels, db.Model):
    """用户信息表"""
    __tablename__ = "user_info"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='用户id')
    user_name = db.Column(db.String(100), nullable=False, comment='用户昵称')
    mobile = db.Column(db.String(16), unique=True, nullable=False, comment='手机号')
    is_admin = db.Column(db.SmallInteger, default=0, comment='是否是管理员')

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'user_name': self.user_name,
            'phone': self.phone,
            'is_admin': self.is_admin,
        }

class UserLogin(BaseModels, db.Model):
    """用户登陆表"""
    __tablename__ = "user_login"

    login_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='登录id')
    user_id = db.Column(db.Integer, comment='用户id')
    mobile = db.Column(db.String(16), unique=True, nullable=False, comment='手机号')
    mypassword = db.Column(db.String(16), nullable=False, comment='密码')
    last_login = db.Column(db.DateTime, default=datetime.now, comment='最后登录时间')
    last_login_stamp = db.Column(db.Integer,comment='最后登录时间戳')

    def to_dict(self):
        return {
            'login_id': self.login_id,
            'user_id': self.user_id,
            'mobile': self.mobile,
            'mypassword': self.mypassword,
            'last_login': self.last_login,
            'last_login_stamp': self.last_login_stamp,
        }