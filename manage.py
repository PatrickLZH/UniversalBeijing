from api import db, create_app
from flask_migrate import Migrate
from flask_cors import CORS
from api.models.user import UserInfo,UserLogin
from api.models.chat import SessionInfo,ChatMessage
from api.models.file import FileManage
from datetime import datetime
import os
import sys

# 设置编码环境变量解决Windows控制台编码问题
os.environ['PYTHONIOENCODING'] = 'utf-8'

# 如果在Windows系统上运行，设置控制台编码
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        # 如果reconfigure不可用，则设置环境变量
        pass

# 指定环境为开发环境
app = create_app('dev')
CORS(app, supports_credentials=True)
Migrate(app, db)


'''
@app.route('/add')
def add_data():
    u = UserInfo()
    new_user1 = UserInfo(user_id=1, user_name='张三', mobile='13712345678', is_admin=1, create_time=datetime.now(), status=1)
    new_user2 = UserInfo(user_id=2, user_name='李四', mobile='13723456789', is_admin=0, create_time=datetime.now(), status=1)
    u.add(new_user1)
    u.add(new_user2)

    u = UserLogin()
    new_user1 = UserLogin(login_id=1, user_id=1, mobile='13712345678', mypassword='abcd',last_login=datetime.now(), create_time=datetime.now(), status=1)
    new_user2 = UserLogin(login_id=2, user_id=2, mobile='13723456789', mypassword='abcd',last_login=datetime.now(), create_time=datetime.now(), status=1)
    u.add(new_user1)
    u.add(new_user2)
# '''

'''
@app.route('/delete')
def delete_data():
    delete_user = UserInfo.query.get(3)
    delete_user.delete()
@app.route('/update')
def update_data():
    u = UserInfo()
    update_user = u.query.get(3)
    update_user.status = 1
    u.update()
'''

'''
@app.route('/query1')
def query_data1():
    user_list = UserInfo.query.all()
    result = []
    for user in user_list:
        result.append(user.to_dict())
    return {'users': result}
@app.route('/query2')
def query_data2():
    user = UserInfo.query.get(3)
    return {'users': user.to_dict()}
@app.route('/query3')
def query_data3():
    first_user = UserInfo.query.first()
    return {'users': first_user.to_dict()}
@app.route('/query4')
def query_data4():
    user_list = UserInfo.query.filter(UserInfo.signature == '理想').all()
    result = []
    for user in user_list:
        result.append(user.to_dict())
    return {'users': result}
@app.route('/query5')
def query_data5():
    user_list = UserInfo.query.filter_by(signature='理想').all()
    result = []
    for user in user_list:
        result.append(user.to_dict())
    return {'users': result}
'''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5010)