import time
import datetime
import jwt
from flask import current_app
from api import redis_store
from api.models.user import UserLogin
from api.utils.response_utils import error, HttpCode, success
from config.config import Config
from functools import wraps
from flask import current_app, g, request



class Auth(object):
    @staticmethod
    def encode_auth_token(user_id, login_time):
        """
        生成认证Token
        :param user_id: int
        :param login_time: int(timestamp)
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.now() + datetime.timedelta(days=1),
                'iat': datetime.datetime.now(),
                'iss': 'Patrick',
                'data': {
                    'id': user_id,
                    'login_time': login_time
                }
            }
            return jwt.encode(
                payload,
                Config.SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def decode_auth_token(auth_token):
        """
        验证Token
        :param auth_token:
        :return: integer|string
        """
        try:
            # 取消过期时间验证
            payload = jwt.decode(auth_token, Config.SECRET_KEY, algorithms=['HS256'],
                                 options={'verify_exp': True,'verify_iat': False})
            if 'data' in payload and 'id' in payload['data']:
                return dict(code=HttpCode.ok, payload=payload)
            else:
                raise dict(code=HttpCode.auth_error, msg=jwt.InvalidTokenError)
        except jwt.ExpiredSignatureError:
            return dict(code=HttpCode.auth_error, msg='Token过期')
        except jwt.InvalidTokenError:
            return dict(code=HttpCode.auth_error, msg='无效Token')

    def authenticate(self, mobile, mypassword):
        """
        用户登录，登录成功返回token，写将登录时间写入数据库；登录失败返回失败原因
        :param mypassword:
        :return: json
        """
        # 用户登录，将登录时间写入数据库，登陆成功返回成功信息，登录失败返回失败原因
        try:
            user_login = UserLogin.query.filter(UserLogin.mobile == mobile).first()
        except Exception as e:
            current_app.logger.error(e)
            return error(code=HttpCode.db_error, msg='查询手机号异常')
        if not user_login:
            return error(code=HttpCode.auth_error, msg='用户不存在')
        elif user_login.mypassword != mypassword:
            return error(code=HttpCode.auth_error, msg='登录密码输入错误')
        else:
            login_time = int(time.time())
            try:
                user_login.last_login = datetime.datetime.now()
                user_login.last_login_stamp = login_time
                user_login.update()
            except Exception as e:
                current_app.logger.error(e)
                return error(code=HttpCode.db_error, msg='登录时间更新失败')
            token = self.encode_auth_token(user_login.user_id, login_time)  # bytes
            if not token:
                return error(code=HttpCode.auth_error, msg='Token生成失败')
            user_id = user_login.user_id

            # 存储到redis中
            try:
                redis_store.ping()
                print("Redis 连接成功")
            except Exception as e:
                print("Redis 连接失败:", e)
            try:
                redis_store.set("jwt_token:%s" % user_id, token, Config.JWT_TOKEN_REDIS_EXPIRES)
                # print(f"Token 已写入 Redis: jwt_token:{user_id}")
            except Exception as e:
                current_app.logger.error(e)
                return error(code=HttpCode.db_error, msg="token保存redis失败")
            return success(msg='用户登录成功', data={"token": token, "user_id": user_id, "mobile": mobile})

    def identify(self, request):
        """
        用户鉴权
        :return: list
        """
        auth_header = request.headers.get('Authorization', None)
        if auth_header:
            auth_token_arr = auth_header.split(" ")
            if not auth_token_arr or len(auth_token_arr) != 2:
            # or auth_token_arr[0] != 'JWT'
                return dict(code=HttpCode.auth_error, msg='请求未携带认证信息，认证失败')
            else:
                auth_token = auth_token_arr[1]
                payload_dict = self.decode_auth_token(auth_token)
                # print('**********payload_dict', payload_dict)
                if 'payload' in payload_dict and payload_dict.get('code') == 200:
                    payload = payload_dict.get('payload')
                    user_id = payload.get('data').get('id')
                    login_time = payload.get('data').get('login_time')
                    # print('👉👉   解析出的时间戳', login_time)
                    user = UserLogin.query.filter(UserLogin.user_id==user_id).first()
                    if not user:  # 未在请求中找到对应的用户
                        return dict(code=HttpCode.auth_error, msg='用户不存在，查无此用户')
                    else:
                        # 通过user取出redis中的token
                        try:
                            # print(user_id)
                            redis_jwt_token = redis_store.get("jwt_token:%s" % user_id)
                            # print('👈redis', redis_jwt_token)
                        except Exception as e:
                            current_app.logger.error(e)
                            return dict(code=HttpCode.db_error, msg="redis查询token失败")
                        if not redis_jwt_token or redis_jwt_token != auth_token:
                            # print('👉👉   解析出来的token', auth_token)
                            return dict(code=HttpCode.auth_error, msg="jwt-token失效")
                        # print(type(user.last_login_stamp), type(login_time))
                        # print(user.last_login_stamp, login_time)
                        if user.last_login_stamp == login_time:

                            return dict(code=HttpCode.ok, msg='用户认证成功', data={"user_id": user.user_id})
                        else:
                            return dict(code=HttpCode.auth_error, msg='用户认证失败，需要再次登录')
                else:
                    return dict(code=HttpCode.auth_error, msg=payload_dict.get('msg') or '用户认证失败，携带认证参数不合法')
        else:
            return dict(code=HttpCode.auth_error, msg='用户认证失败,请求未携带对应认证信息')



def auth_identify(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        response = Auth().identify(request)
        if response.get('code') == 200:
            user_id = response.get('data')['user_id']
            # 查询用户对象
            user = None
            if user_id:
                try:
                    from api.models.user import UserInfo
                    user = UserInfo.query.get(user_id)
                except Exception as e:
                    current_app.logger.error(e)
            # 使用g对象保存
            g.user = user

            return view_func(*args, **kwargs)

        else:
            return error(HttpCode.auth_error, response.get('msg'))

    return wrapper