from api import db
from api.models.base import BaseModels


class ChatMessage(BaseModels, db.Model):
    """消息记录表"""
    __tablename__ = "chat_message"

    msg_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='消息id')
    session_id = db.Column(db.Integer, comment='会话id')
    sender_type = db.Column(db.String(9), comment='发送方类型(user/assistant)')
    session_summary = db.Column(db.Text, comment='会话摘要')
    content = db.Column(db.Text, comment='消息内容')
    reference = db.Column(db.Text, comment='参考信息（如果sender_type为assistant）')
    first_token_time_ms = db.Column(db.Integer, comment='首个token用时（毫秒）')
    islike = db.Column(db.SmallInteger, default=0, comment='是否点赞（0:无反馈，1:点赞，-1:点踩）')
    feedback = db.Column(db.Text, comment='反馈信息（如果islike为-1）')

    def to_dict(self):
        return {
            "msg_id": self.msg_id,
            "session_id": self.session_id,
            "sender_type": self.sender_type,
            "session_summary": self.session_summary,
            "content": self.content,
            "reference": self.reference,
            "first_token_time_ms": self.first_token_time_ms,
            "islike": self.islike,
            "feedback": self.feedback,
        }


class SessionInfo(BaseModels, db.Model):
    """会话信息表"""
    __tablename__ = "session_info"
    session_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='会话id')
    session_summary = db.Column(db.Text, comment='会话摘要')
    user_id = db.Column(db.Integer, comment='用户id')

    def to_dict(self):
        return {
            "session_id": self.session_id,
            "session_summary": self.session_summary,
            "user_id": self.user_id,
        }