from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from flask_cors import CORS, cross_origin
import sqlite3
from db_utils import db_init, add_user, get_all_users, update_user_info, delete_user, get_password_hash_by_username, create_appointment, get_appointments_by_teacher, get_appointments_by_student, update_appointment_status, delete_appointment
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime, timedelta


app = Flask(__name__)
CORS(app)

# # 初始化数据库
# db_init()
@app.route('/', methods=['OPTIONS'])
@cross_origin()
def handle_options_request():
    response = jsonify({'message': 'This is the response to OPTIONS request'})
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    if not username or not password or not role:
        return jsonify({'message': 'Missing username, password, or role'}), 400

    try:
        add_user(username, password, role)
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/login', methods=['POST'])
@cross_origin()
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Missing username or password'}), 400

    conn = sqlite3.connect('school_appointment.db')
    c = conn.cursor()
    c.execute('SELECT user_id, password_hash, role FROM users WHERE username = ?', (username,))
    result = c.fetchone()
    conn.close()

    if result:
        user_id, password_hash, role = result
        if check_password_hash(password_hash, password):
            return jsonify({'message': 'Login successful', 'username': username, 'role': role, 'user_id': user_id}), 200
        else:
            return jsonify({'message': 'Invalid username or password'}), 401
    else:
        return jsonify({'message': 'Invalid username or password'}), 401


# 管理员 API 接口

@app.route('/admin/users', methods=['GET'])
def get_users():
    users = get_all_users()
    users_list = []

    for user in users:
        user_dict = {
            'user_id': user[0],
            'username': user[1],
            'password': user[2],
            'role': user[3]
        }
        users_list.append(user_dict)

    return jsonify(users_list), 200

@app.route('/admin/appointments', methods=['GET'])
def get_all_appointments():
    conn = sqlite3.connect('school_appointment.db')
    c = conn.cursor()
    c.execute('SELECT * FROM appointments')
    appointments = c.fetchall()
    conn.close()

    appointments_list = []
    for appointment in appointments:
        appointments_list.append({
            'appointment_id': appointment[0],
            'student_id': appointment[1],
            'teacher_id': appointment[2],
            'date': appointment[3],
            'start_time': appointment[4],
            'end_time': appointment[5],
            'status': appointment[6],
        })
    
    return jsonify(appointments_list), 200

@app.route('/admin/users/<int:user_id>', methods=['PUT'])
def modify_user(user_id):
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    try:
        update_user_info(user_id, username, password, role)
        return jsonify({'message': 'User information updated successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/admin/users/<int:user_id>', methods=['DELETE'])
def remove_user(user_id):
    try:
        delete_user(user_id)
        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user_info(user_id):
    conn = sqlite3.connect('school_appointment.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = c.fetchone()

    if user:
        user_info = {
            'user_id': user[0],
            'username': user[1],
            'role': user[3]
        }

        if user[3] == 'teacher':
            c.execute('SELECT * FROM teachers WHERE user_id = ?', (user_id,))
            teacher = c.fetchone()
            if teacher:
                user_info.update({
                    'name': teacher[2],
                    'gender': teacher[3],
                    'title': teacher[4],
                    'department': teacher[5],
                    'office_number': teacher[6],
                    'phone': teacher[7]
                })
        elif user[3] == 'student':
            c.execute('SELECT * FROM students WHERE user_id = ?', (user_id,))
            student = c.fetchone()
            if student:
                user_info.update({
                    'name': student[2],
                    'gender': student[3],
                    'student_number': student[4],
                    'class': student[5],
                    'phone': student[6]
                })

        conn.close()
        return jsonify(user_info), 200

    conn.close()
    return jsonify({'message': 'User not found'}), 404

@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user_info(user_id):
    data = request.get_json()
    print(f"Received data from frontend: {data}")  # 打印接收到的数据

    username = data.get('username')
    role = data.get('role')

    # 添加日志打印以调试
    print(f"Updating user {user_id} with username: {username}, role: {role}")

    if not username or not role:
        return jsonify({'message': 'Username and role are required'}), 400

    conn = sqlite3.connect('school_appointment.db')
    c = conn.cursor()

    try:
        c.execute('UPDATE users SET username = ?, role = ? WHERE user_id = ?', (username, role, user_id))

        if role == 'teacher':
            name = data.get('name')
            gender = data.get('gender')
            title = data.get('title')
            department = data.get('department')
            office_number = data.get('office_number')
            phone = data.get('phone')
            c.execute('''
                INSERT INTO teachers (user_id, name, gender, title, department, office_number, phone)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                name = excluded.name,
                gender = excluded.gender,
                title = excluded.title,
                department = excluded.department,
                office_number = excluded.office_number,
                phone = excluded.phone
            ''', (user_id, name, gender, title, department, office_number, phone))

        elif role == 'student':
            name = data.get('name')
            gender = data.get('gender')
            student_number = data.get('student_number')
            class_ = data.get('class')
            phone = data.get('phone')
            c.execute('''
                INSERT INTO students (user_id, name, gender, student_number, class, phone)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                name = excluded.name,
                gender = excluded.gender,
                student_number = excluded.student_number,
                class = excluded.class,
                phone = excluded.phone
            ''', (user_id, name, gender, student_number, class_, phone))

        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        print(f"Database error: {e}")
        return jsonify({'message': 'An error occurred while updating user information'}), 500
    finally:
        conn.close()

    return jsonify({'message': 'User information updated successfully'}), 200


@app.route('/teacher/timetable/<int:user_id>', methods=['GET'])
def get_teacher_timetable(user_id):
    conn = sqlite3.connect('school_appointment.db')
    c = conn.cursor()
    c.execute('SELECT availability_id, date, start_time, end_time FROM teacher_availability WHERE teacher_id = ?', (user_id,))
    timetable = c.fetchall()
    conn.close()
    # 确保返回的数据格式为 JSON
    return jsonify([{
        'id': row[0],
        'date': row[1],
        'start_time': row[2],
        'end_time': row[3]
    } for row in timetable]), 200

@app.route('/teacher/timetable', methods=['POST'])
def add_teacher_timetable():
    data = request.get_json()
    teacher_id = data.get('teacher_id')
    date = data.get('date')
    start_time = data.get('start_time')
    end_time = data.get('end_time')

    conn = sqlite3.connect('school_appointment.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO teacher_availability (teacher_id, date, start_time, end_time)
        VALUES (?, ?, ?, ?)
    ''', (teacher_id, date, start_time, end_time))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Time slot added successfully'}), 201

@app.route('/teacher/timetable/<int:id>', methods=['DELETE'])
def delete_teacher_timetable(id):
    conn = sqlite3.connect('school_appointment.db')
    c = conn.cursor()
    c.execute('DELETE FROM teacher_availability WHERE availability_id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Time slot deleted successfully'}), 200

@app.route('/teacher/appointments/<int:user_id>', methods=['GET'])
def get_teacher_appointments(user_id):
    conn = sqlite3.connect('school_appointment.db')
    c = conn.cursor()
    c.execute('''
        SELECT a.appointment_id, s.name AS student_name, a.date, a.start_time, a.end_time, a.status
        FROM appointments a
        JOIN students s ON a.student_id = s.student_id
        WHERE a.teacher_id = ?
    ''', (user_id,))
    appointments = c.fetchall()
    conn.close()
    return jsonify(appointments), 200

@app.route('/teacher/appointments/<int:id>', methods=['PUT'])
def update_appointment_status(id):
    data = request.get_json()
    status = data.get('status')

    conn = sqlite3.connect('school_appointment.db')
    c = conn.cursor()
    c.execute('UPDATE appointments SET status = ? WHERE appointment_id = ?', (status, id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Appointment status updated successfully'}), 200

@app.route('/teacher/timetable/default', methods=['POST'])
def set_default_timetable():
    conn = sqlite3.connect('school_appointment.db')
    c = conn.cursor()

    # 获取所有教师的 ID
    c.execute('SELECT user_id FROM users WHERE role = "teacher"')
    teachers = c.fetchall()

    # 获取当前日期和未来三天的日期
    today = datetime.now()
    dates = [(today + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1, 4)]

    # 定义默认的空闲时间段
    default_times = [
        ('08:00', '09:00'),
        ('09:00', '10:00'),
        ('10:00', '11:00'),
        ('14:00', '15:00'),
        ('15:00', '16:00'),
        ('16:00', '17:00')
    ]

    # 为每个教师分配未来三天的默认空闲时间
    for teacher in teachers:
        teacher_id = teacher[0]
        for date in dates:
            for start_time, end_time in default_times:
                c.execute('''
                    INSERT INTO teacher_availability (teacher_id, date, start_time, end_time)
                    VALUES (?, ?, ?, ?)
                ''', (teacher_id, date, start_time, end_time))

    conn.commit()
    conn.close()

    return jsonify({'message': 'Default timetable set successfully for all teachers'}), 201
# 学生 API 接口

@app.route('/student/availability/<int:teacher_id>', methods=['GET'])
def get_teacher_availability(teacher_id):
    conn = sqlite3.connect('school_appointment.db')
    c = conn.cursor()
    c.execute('SELECT * FROM teacher_availability WHERE teacher_id = ?', (teacher_id,))
    availability = c.fetchall()
    conn.close()

    return jsonify(availability), 200

@app.route('/student/appointments', methods=['POST'])
def book_appointment():
    data = request.get_json()
    student_id = data.get('student_id')
    teacher_id = data.get('teacher_id')
    date = data.get('date')
    start_time = data.get('start_time')
    end_time = data.get('end_time')

    try:
        create_appointment(student_id, teacher_id, date, start_time, end_time)
        return jsonify({'message': 'Appointment booked successfully'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/student/appointments/<int:student_id>', methods=['GET'])
def get_student_appointments(student_id):
    appointments = get_appointments_by_student(student_id)
    return jsonify(appointments), 200

if __name__ == '__main__':
    app.run(debug=True)
    