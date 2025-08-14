from api import db
from api.models.base import BaseModels

class FileManage(BaseModels, db.Model):
    """文件管理表"""
    __tablename__ = "file_manage"
    manage_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='管理id')
    file_name = db.Column(db.String(255), nullable=False, comment='文件名')
    directory = db.Column(db.String(255), nullable=False, comment='所在目录')
    operate_type = db.Column(db.SmallInteger, default=1, comment='操作类型（1:添加, 0:删除）')
    is_chunked = db.Column(db.SmallInteger, default=0, comment='是否完成chunk划分（0:未完成, 1:已完成）(如果operate_type为1)')

    def to_dict(self):
        return {
            "manage_id": self.manage_id,
            "file_name": self.file_name,
            "directory": self.directory,
            "operate_type": self.operate_type,
            "is_chunked": self.is_chunked,
        }