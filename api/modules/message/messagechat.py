from flask_restful import Resource
from flask import Response, current_app, request
from api.models.chat import ChatMessage, SessionInfo
from api.utils.response_utils import error, HttpCode, success
from api.utils.session_summary import get_summary
from rag_main import get_answer
from api.utils.auth_helper import auth_identify
import time

class MessageView(Resource):
    @auth_identify
    def post(self):
        receive = request.json    
        user_id, session_id, content = \
        receive['user_id'], receive['session_id'], receive['content']
        try:
            if not session_id:
                session_info = SessionInfo()
                session_info.add(SessionInfo(session_id=session_id,
                                             session_summary='新会话',
                                             user_id=user_id))
        
            session_id_new = SessionInfo.query.filter(SessionInfo.user_id==user_id) \
                .order_by(SessionInfo.session_id.desc()).first().session_id
            
            # 查询历史消息
            history_messages = ChatMessage.query \
                .filter(ChatMessage.session_id == session_id_new) \
                .order_by(ChatMessage.create_time.asc()) \
                .all()
            # 构建历史上下文
            history = []
            for msg in history_messages:
                if msg.sender_type == 'user':
                    history.append({'role': 'user', 'content': msg.content})
                elif msg.sender_type == 'assistant':
                    history.append({'role': 'assistant', 'content': msg.content})
            # 保留最近5轮对话（10 条消息）
            if len(history) > 10:
                history = history[-10:]

            chat_message = ChatMessage()
            chat_message.add(ChatMessage(session_id=session_id_new,
                            sender_type="user",
                            content=content))
        except Exception as e:
            return error(code=HttpCode.db_error, msg="消息保存失败")

        # 保存当前 app 实例
        app = current_app._get_current_object()

        # 开始流式回复
        def generate():
            with app.app_context():
                success_json = {
                    "code": HttpCode.ok,
                    "msg": "消息获取成功",
                    "data": {'user_id': user_id, 'session_id': session_id_new}
                }
                yield f"data: {success_json}\n\n"

            start_time = time.time()
            full_response = ""
            for i,chunk in enumerate(get_answer(content,
                                                start_time=start_time,
                                                history=history)):
 
                if not chunk.startswith("[END]"):
                    json_data = {
                        "code": HttpCode.ok,
                        "msg": "消息获取成功",
                        "data": {"content":chunk}
                    }
                    yield f"data: {json_data}\n\n"
                
                if i == 0:
                    elapsed = int((time.time()-start_time)*1000)
                # 收集完整响应用于后续处理
                if not chunk.startswith("[END]"):
                    full_response += chunk
            print("full_response:", full_response)
            session_summary = None
            full_session_summary = None
            two_messages = [{"role": "user", "content": content},
                       {"role": "assistant", "content": full_response}]
            # print("session_id=",session_id,"two_messages=",two_messages)
            if not session_id and len(two_messages) == 2:
                full_session_summary = get_summary(two_messages)
                print("full_session_summary:", full_session_summary)
                if full_session_summary:
                    if "**" in full_session_summary:
                        session_summary = full_session_summary.split("**")[1]
                    elif "# " in full_session_summary: 
                        session_summary = full_session_summary.split("# ")[1]
                    else:
                        session_summary = full_session_summary
                print("session_summary:", session_summary)
                # print("session_id_new:", session_id_new)
                # 在应用上下文中执行数据库操作
                with app.app_context():
                    si = SessionInfo.query.filter(SessionInfo.session_id == session_id_new).first()
                    si.session_summary = session_summary
                    si.update()
            # 结束标记也使用JSON格式
            end_json = {
                "code": HttpCode.ok,
                "msg": "消息结束",
                "data": {"session_summary": session_summary,
                         "first_token_time_ms": elapsed}
                        }
            yield f"data: {end_json}\n\n"

            # 在应用上下文中保存数据
            with app.app_context():
                try:
                    # print(f'session_id={session_id_new},first_token_time_ms={elapsed}')
                    chat_message_response = ChatMessage()
                    chat_message_response.add(ChatMessage(
                                    session_id=session_id_new,
                                    sender_type="assistant",
                                    session_summary=session_summary,
                                    content=full_response,
                                    first_token_time_ms=elapsed))
                    msg_id = ChatMessage.query.filter(ChatMessage.session_id==session_id_new) \
                    .order_by(ChatMessage.msg_id.desc()).first().msg_id
                    msg_id_json = {
                        "code": HttpCode.ok,
                        "msg": "AI回复保存成功",
                        "data": {"msg_id": msg_id}
                            }
                    yield f"data: {msg_id_json}\n\n"
                except Exception as e:
                    return error(code=HttpCode.db_error, msg="AI回复保存失败")
        return Response(generate(), mimetype='text/event-stream')
    

class MessageSession(Resource):
    @auth_identify
    def post(self):
        """
        获取指定session_id的所有聊天记录
        """
        receive = request.json
        session_id = receive['session_id']
        messages = ChatMessage.query \
            .filter(ChatMessage.session_id == session_id) \
            .order_by(ChatMessage.create_time.asc()) \
            .all()
        if not messages:
            return error(code=HttpCode.param_error, msg="该会话无聊天记录")
        return success(msg='获取成功' ,data=[msg.to_dict() for msg in messages])
    

class MessageAll(Resource):
    @auth_identify
    def post(self):
        """
        获取指定user_id的所有聊天记录
        """
        receive = request.json
        user_id = receive['user_id']
        session_info = SessionInfo.query \
            .filter(SessionInfo.user_id == user_id) \
            .order_by(SessionInfo.create_time.asc()) \
            .all()
        if not session_info:
            return error(code=HttpCode.param_error, msg="该用户无聊天记录")
        return success(msg='获取成功',data=[session.to_dict() for session in session_info])