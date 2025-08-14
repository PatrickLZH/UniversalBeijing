import os
from flask import Flask, request, send_from_directory

app = Flask(__name__)
BASE_DOCUMENTS_DIR = os.path.abspath('documents')

@app.route('/documents/<directory>/<filename>', methods=['POST', 'PUT'])
def upload_document(directory, filename):
    """上传文件到 documents/<directory>/ 目录"""
    try:
        # 创建安全的目录路径
        safe_directory = os.path.join(BASE_DOCUMENTS_DIR, directory)
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return 'error'
            # 构建安全的文件路径
            file_path = os.path.join(safe_directory, filename)
            file.save(file_path)
            return 'success'
        elif request.data:
            # 处理二进制数据上传
            file_path = os.path.join(safe_directory, filename)
            with open(file_path, 'wb') as f:
                f.write(request.data)
            return 'success'
        else:
            return 'error'
    except Exception as e:
        return 'error'

@app.route('/documents/<directory>/<filename>', methods=['GET'])
def download_document(directory, filename):
    """下载文件"""
    try:
        # 构建完整路径并验证
        full_directory = os.path.join(BASE_DOCUMENTS_DIR, directory)
        print(f"下载文件: {filename}")
        print(f"文件路径: {full_directory}")
        
        # 使用 Flask 的安全路径处理
        response = send_from_directory(
            directory=full_directory,
            path=filename,
            as_attachment=True)
        print(f"响应: {response}")
        return response
    except FileNotFoundError:
        return 'error'
    except Exception as e:
        return 'error'

def main():
    app.run(debug=True, host='0.0.0.0', port=5010) 

if __name__ == '__main__':
    main()
    