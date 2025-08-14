from flask import request, send_from_directory
from api.utils.response_utils import error, HttpCode, success
import os
from pathlib import Path
from . import documents_blu # 从 __init__.py 导入已创建的蓝图
# from api.utils.auth_helper import auth_identify

# 定义基础文档目录
BASE_DOCUMENTS_DIR = 'documents'
# 确保基础目录存在
Path(BASE_DOCUMENTS_DIR).mkdir(parents=True, exist_ok=True)

@documents_blu.route('/<directory>/<filename>', methods=['POST', 'PUT'])
# @auth_identify
def upload_document(directory, filename):
    """上传文件到 documents/<directory>/ 目录"""
    try:
        # 创建安全的目录路径
        safe_directory = os.path.join(BASE_DOCUMENTS_DIR, directory)
        Path(safe_directory).mkdir(parents=True, exist_ok=True)
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return error(HttpCode.param_error, '没有选择文件')
            # 构建安全的文件路径
            file_path = os.path.join(safe_directory, filename)
            file.save(file_path)
            return success(msg='文件上传成功', data={'path': file_path})
        elif request.data:
            # 处理二进制数据上传
            file_path = os.path.join(safe_directory, filename)
            with open(file_path, 'wb') as f:
                f.write(request.data)
            return success(msg='文件上传成功', data={'path': file_path})
        else:
            return error(HttpCode.param_error, '没有提供文件')
    except Exception as e:
        return error(HttpCode.server_error, str(e))

@documents_blu.route('/<directory>/<filename>', methods=['GET'])
# @auth_identify
def download_document(directory, filename):
    """下载文件"""
    try:
        # 构建完整路径并验证
        base_path = os.path.abspath(BASE_DOCUMENTS_DIR)  # 获取绝对路径
        full_directory = os.path.join(base_path, directory)
        print(f"下载文件: {filename}")
        print(f"文件路径: {full_directory}")
        
        # 使用 Flask 的安全路径处理
        response = send_from_directory(
            directory=full_directory,
            path=filename,
            as_attachment=True)
        print(f"响应: {response}")
        return response
        # return success(msg='文件下载成功', data={'directory':directory,
        #                                         'filename': filename})
    
    except FileNotFoundError:
        return error(HttpCode.param_error, '文件未找到')
    except Exception as e:
        return error(HttpCode.server_error, str(e))