from flask_restful import Resource
from flask import request
from api.models.file import FileManage
from api.utils.response_utils import error, HttpCode, success
from api.utils.auth_helper import auth_identify
import os
from pathlib import Path
import datetime

# 定义基础文档目录
BASE_DOCUMENTS_DIR = 'documents'
# 确保基础目录存在
Path(BASE_DOCUMENTS_DIR).mkdir(parents=True, exist_ok=True)

class FileView(Resource):
    @auth_identify
    def get(self):
        """
        获取所有文件列表
        """
        file_manage = FileManage.query.filter(FileManage.operate_type == 1).all()
        base_url = request.host_url.rstrip('/')
        files_data = []
        for file_mng in file_manage:
            file_dict = file_mng.to_dict()
            file_dict['url'] = f"{base_url}/documents/{file_mng.directory}/{file_mng.file_name}"
            files_data.append(file_dict)
        return success(msg='获取成功' ,data=files_data)

    @auth_identify
    def post(self):
        """
        添加文件
        """
        try:
            # 获取form-data中的字段
            manage_id = None
            file_name = request.form.get('file_name')
            directory = request.form.get('directory')
            # 获取上传的文件
            uploaded_file = request.files.get('file')
            # 检查文件是否已存在
            fm = FileManage.query.filter(FileManage.file_name == file_name,
                                         FileManage.operate_type == 1).first()
            if fm:
                return error(code=HttpCode.param_error, msg="要添加的文件已存在")
            # 保存文件到指定目录（这里需要根据您的实际文件存储逻辑进行调整）
            # 示例：保存到服务器的指定路径
            file_path = os.path.join(os.path.abspath(BASE_DOCUMENTS_DIR), directory)
            os.makedirs(file_path, exist_ok=True)
            full_file_path = os.path.join(file_path, file_name)
            uploaded_file.save(full_file_path)
            # 保存文件信息到数据库
            file_manage = FileManage()
            file_manage.add(FileManage(manage_id=manage_id,
                            file_name=file_name,
                            directory=directory,
                            operate_type=1))
            return success(msg='文件上传成功', data={
                                                # 'manage_id':manage_id,
                                                  'file_name':file_name,
                                                  'directory':directory,
                                                  'operate_type':1})   
        except Exception as e:
            return error(HttpCode.server_error, f'文件上传失败: {str(e)}')
        
    @auth_identify
    def delete(self):
        """
        删除指定文件
        """
        try:
            receive = request.json
            manage_id = receive['manage_id']
            file_name = receive['file_name']
            directory = receive['directory']
            fm = FileManage.query.filter(FileManage.manage_id == manage_id,
                                        FileManage.operate_type == 1).first()
            if not fm:
                return error(code=HttpCode.param_error, msg='要删除的文件不存在')
            fm.operate_type = 0
            fm.update()
            # 物理删除文件
            file_path = os.path.join(os.path.abspath(BASE_DOCUMENTS_DIR), directory)
            full_file_path = os.path.join(file_path, file_name)
            if os.path.exists(full_file_path):
                # 生成带时间戳的新文件名
                name, ext = os.path.splitext(file_name)
                timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                new_file_name = f"{name}_{timestamp}{ext}"
                TRASH_FOLDER = 'delete'
                trash_path = os.path.join(os.path.abspath(BASE_DOCUMENTS_DIR), TRASH_FOLDER)
                os.makedirs(trash_path, exist_ok=True)
                # 将重命名后的文件移动到目标文件夹
                moved_file_path = os.path.join(trash_path, new_file_name)
                os.rename(full_file_path, moved_file_path)

            # 添加URL到返回数据
            base_url = request.host_url.rstrip('/')
            file_url = f"{base_url}/documents/{directory}/{file_name}"
            return success(msg='删除文件成功', data={'manage_id': manage_id,
                                                  'file_name': file_name,
                                                  'directory': directory,
                                                  'operate_type': 0,
                                                  'url': file_url})
        except Exception as e:
            return error(HttpCode.server_error, f'删除文件失败: {str(e)}')