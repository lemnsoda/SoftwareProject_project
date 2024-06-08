from flask import Flask, request, jsonify, session
from tis_1 import Admin, Teacher, Student, initDB, close_db, get_db
from flask_cors import CORS
import logging

# 设置日志级别
# logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# 启用CORS
CORS(app)

initDB()

admin = Admin()

# @app.before_request
# def log_request_info():
#     app.logger.debug('Request Path: %s', request.path)


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = data['password']
    role = data['role']
    information_dict = data['information']
    admin.register(username, password, role, information_dict)
    return jsonify({"message": "Registration successful"}), 201

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data['username']
        password = data['password']

        result = admin.login(username, password)
        app.logger.debug(f"Login result: {result}")

        if result:
            session['cookie_role'] = result['cookie_role']
            return jsonify({"message": "Login successful", "cookie_role": result['cookie_role'], "role": result['role']}), 200
        else:
            return jsonify({"message": "Invalid username or password"}), 401
    except Exception as e:
        return jsonify({"message": "An error occurred during login"}), 500



@app.route('/getUnactiveUsers', methods=['GET'])
def get_unactive_users():
    if 'cookie_role' not in session:
        return jsonify({"message": "Unauthorized"}), 401
    result = admin.getUnactiveUsers()
    if result:
        return jsonify({"unactive_users": result}), 200
    else:
        return jsonify({"message": "No unactive users found"}), 404

@app.route('/activateUser', methods=['POST'])
def activate_user():
    if 'cookie_role' not in session:
        return jsonify({"message": "Unauthorized"}), 401
    data = request.json
    uuid = data['uuid']
    admin.activeUser(uuid)
    return jsonify({"message": "User activated successfully"}), 200

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('cookie_role', None)
    return jsonify({"message": "Logged out successfully"}), 200

# 调试用接口, 用于查看数据库中的用户信息
@app.route('/debug/users', methods=['GET'])
def debug_users():
    db = get_db()
    c = db.cursor()
    c.execute("SELECT * FROM user")
    users = c.fetchall()
    return jsonify(users), 200

# 在每个请求结束时关闭数据库连接
@app.teardown_appcontext
def teardown_db(exception):
    close_db(exception)

if __name__ == '__main__':
    app.run(debug=True)
