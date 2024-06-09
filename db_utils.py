import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def db_init():
    conn = sqlite3.connect('school_appointment.db')
    c = conn.cursor()

    # 创建用户表
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('admin', 'teacher', 'student'))
        )
    ''')

    # 创建教师信息表
    c.execute('''
        CREATE TABLE IF NOT EXISTS teachers (
            teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            name TEXT NOT NULL,
            gender TEXT,
            title TEXT,
            department TEXT,
            office_number TEXT,
            phone TEXT,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')

    # 创建学生信息表
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            name TEXT NOT NULL,
            gender TEXT,
            student_number TEXT,
            class TEXT,
            phone TEXT,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')

    # 创建教师空闲时间表
    c.execute('''
        CREATE TABLE IF NOT EXISTS teacher_availability (
            availability_id INTEGER PRIMARY KEY AUTOINCREMENT,
            teacher_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            is_booked BOOLEAN NOT NULL DEFAULT 0,
            FOREIGN KEY (teacher_id) REFERENCES teachers (teacher_id)
        )
    ''')

    # 创建预约表
    c.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            teacher_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('pending', 'approved', 'rejected', 'canceled')),
            FOREIGN KEY (student_id) REFERENCES students (student_id),
            FOREIGN KEY (teacher_id) REFERENCES teachers (teacher_id)
        )
    ''')

    conn.commit()
    conn.close()


def generate_test_users():
    conn = sqlite3.connect('school_appointment.db')
    c = conn.cursor()

    # 清空用户表中的数据
    c.execute('DELETE FROM users')

    users = [
        ('admin', 'admin123', 'admin'),
        ('teacher1', 'teacher123', 'teacher'),
        ('teacher2', 'teacher123', 'teacher'),
        ('student1', 'student123', 'student'),
        ('student2', 'student123', 'student')
    ]

    for username, password, role in users:
        password_hash = generate_password_hash(password)
        c.execute('INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)', (username, password_hash, role))

    conn.commit()
    conn.close()


def add_user(username, password, role):
    conn = sqlite3.connect('school_appointment.db')
    c = conn.cursor()
    password_hash = generate_password_hash(password)
    c.execute('INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)', (username, password_hash, role))
    conn.commit()
    conn.close()

def get_all_users():
    conn = sqlite3.connect('school_appointment.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users')
    users = c.fetchall()
    conn.close()
    return users

def get_all_teachers():
    conn = sqlite3.connect('school_appointment.db')
    c = conn.cursor()
    c.execute('SELECT * FROM teachers')
    teachers = c.fetchall()
    conn.close()
    return teachers

def get_appointments_by_teacher(teacher_id):
    conn = sqlite3.connect('school_appointment.db')
    c = conn.cursor()
    c.execute('SELECT * FROM appointments WHERE teacher_id = ?', (teacher_id,))
    appointments = c.fetchall()
    conn.close()
    return appointments

def get_password_hash_by_username(username):
    conn = sqlite3.connect('school_appointment.db')
    c = conn.cursor()
    c.execute('SELECT password_hash FROM users WHERE username = ?', (username,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def delete_user(user_id):
    conn = sqlite3.connect('school_appointment.db')
    c = conn.cursor()
    # 删除用户表中的记录
    c.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
    # 同时删除教师和学生表中相关记录
    c.execute('DELETE FROM teachers WHERE user_id = ?', (user_id,))
    c.execute('DELETE FROM students WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()

def update_user_info(user_id, username=None, password=None, role=None):
    conn = sqlite3.connect('school_appointment.db')
    c = conn.cursor()
    if username:
        c.execute('UPDATE users SET username = ? WHERE user_id = ?', (username, user_id))
    if password:
        password_hash = generate_password_hash(password)
        c.execute('UPDATE users SET password_hash = ? WHERE user_id = ?', (password_hash, user_id))
    if role:
        c.execute('UPDATE users SET role = ? WHERE user_id = ?', (role, user_id))
    conn.commit()
    conn.close()

def get_appointments_by_student(student_id):
    conn = sqlite3.connect('school_appointment.db')
    c = conn.cursor()
    c.execute('SELECT * FROM appointments WHERE student_id = ?', (student_id,))
    appointments = c.fetchall()
    conn.close()
    return appointments

def create_appointment(student_id, teacher_id, date, start_time, end_time):
    conn = sqlite3.connect('school_appointment.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO appointments (student_id, teacher_id, date, start_time, end_time, status)
        VALUES (?, ?, ?, ?, ?, 'pending')
    ''', (student_id, teacher_id, date, start_time, end_time))
    conn.commit()
    conn.close()

def update_appointment_status(appointment_id, status):
    conn = sqlite3.connect('school_appointment.db')
    c = conn.cursor()
    if status not in ['approved', 'rejected', 'canceled']:
        raise ValueError("Invalid status")
    c.execute('UPDATE appointments SET status = ? WHERE appointment_id = ?', (status, appointment_id))
    conn.commit()
    conn.close()

    if status == 'approved':
        # 同时更新教师的空闲时间表
        c.execute('''
            UPDATE teacher_availability
            SET is_booked = 1
            WHERE teacher_id = (
                SELECT teacher_id
                FROM appointments
                WHERE appointment_id = ?
            )
            AND date = (
                SELECT date
                FROM appointments
                WHERE appointment_id = ?
            )
            AND start_time = (
                SELECT start_time
                FROM appointments
                WHERE appointment_id = ?
            )
            AND end_time = (
                SELECT end_time
                FROM appointments
                WHERE appointment_id = ?
            )
        ''', (appointment_id, appointment_id, appointment_id, appointment_id))
        conn.commit()
    conn.close()

def delete_appointment(appointment_id):
    conn = sqlite3.connect('school_appointment.db')
    c = conn.cursor()
    c.execute('DELETE FROM appointments WHERE appointment_id = ?', (appointment_id,))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    db_init()
    generate_test_users()
    print("Database initialized and test users generated.")

    # # 测试新增用户
    # add_user('student3', 'student123', 'student')
    # print("New user added.")

    # 测试获取所有用户
    users = get_all_users()
    print("All users:", users)

    # # 测试获取所有教师
    # teachers = get_all_teachers()
    # print("All teachers:", teachers)

    # # 测试按照教师ID获取所有预约
    # appointments = get_appointments_by_teacher(1)
    # print("Appointments for teacher 1:", appointments)

    # # 测试根据用户名获取密码哈希
    # password_hash = get_password_hash_by_username('admin')
    # print("Password hash for admin:", password_hash)

    # # 测试删除用户
    # delete_user(1)
    # print("User with ID 1 deleted.")

    # # 测试更新用户信息
    # update_user_info(2, username='new_teacher1', password='newpassword123', role='teacher')
    # print("User with ID 2 updated.")

    # # 测试根据学生ID获取所有预约
    # student_appointments = get_appointments_by_student(1)
    # print("Appointments for student 1:", student_appointments)

    # # 测试创建预约
    # create_appointment(1, 2, '2024-06-10', '10:00', '11:00')
    # print("Appointment created for student 1 with teacher 2.")

    # # 测试更新预约状态为 approved
    # update_appointment_status(1, 'approved')
    # print("Appointment with ID 1 approved.")

    # # 测试更新预约状态为 rejected
    # update_appointment_status(1, 'rejected')
    # print("Appointment with ID 1 rejected.")

    # # 测试更新预约状态为 canceled
    # update_appointment_status(1, 'canceled')
    # print("Appointment with ID 1 canceled.")

    # # 测试删除预约
    # delete_appointment(1)
    # print("Appointment with ID 1 deleted.")
