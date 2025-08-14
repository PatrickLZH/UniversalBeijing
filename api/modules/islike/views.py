from api.modules.islike import islike_blu
from flask import request
from api.models.chat import ChatMessage
from api.utils.response_utils import error, HttpCode, success
from api.utils.auth_helper import auth_identify

@islike_blu.route('/', methods=['POST'])
@auth_identify
def update_message_like():
    receive = request.json
    msg_id, sender_type, islike, feedback \
    = receive['msg_id'], receive['sender_type'], receive['islike'], receive['feedback']
    if sender_type != 'assistant':
        return error(code=HttpCode.param_error, msg='参数错误')
    elif islike not in [1, -1]:
        return error(HttpCode.param_error, '操作类型错误')
    cm = ChatMessage.query.filter(ChatMessage.msg_id == msg_id).first()
    if not cm:
        return error(HttpCode.param_error, '消息不存在')
    cm.islike = islike
    cm.feedback = feedback
    cm.update()
    return success(msg='提交成功',
                   data={'msg_id':msg_id,
                        'islike':islike,
                        'feedback':feedback})