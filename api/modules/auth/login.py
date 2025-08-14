import re
from flask_restful import Resource, request
# from datetime import datetime
# from flask import current_app
# from api.models.user import UserLogin
from api.utils.auth_helper import Auth
from api.utils.response_utils import error, HttpCode #, success

class LoginView(Resource):
    def post(self):
        receive = request.json    
        # 手机号校验
        mobile, mypassword = receive['mobile'], receive['mypassword']
        if not mobile:
            return error(code=HttpCode.auth_error, msg='手机号不能为空')
        if not re.fullmatch(r'1[3456789]\d{9}', mobile):
            return error(code=HttpCode.auth_error, msg='手机号格式不正确')
        # 密码校验
        if not mypassword:
            return error(code=HttpCode.auth_error, msg='密码不能为空')
        if not isinstance(mypassword, str):
            return error(code=HttpCode.auth_error, msg='密码必须为字符串')
        return Auth().authenticate(mobile, mypassword)