import sqlite3
import random
import string
from flask import g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('TeacherInformationSystem.db', check_same_thread=False)
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def initDB():
    conn = sqlite3.connect('TeacherInformationSystem.db', check_same_thread=False)
    c = conn.cursor()
    # 用户表
    c.execute('''CREATE TABLE IF NOT EXISTS user
           (uuid INTEGER PRIMARY KEY AUTOINCREMENT,
           username TEXT NOT NULL,
           password TEXT NOT NULL,
           role INTEGER NOT NULL,
           if_active INTEGER NOT NULL);''')
    
    # 教师表
    c.execute('''CREATE TABLE IF NOT EXISTS teacher
           (uuid INTEGER PRIMARY KEY AUTOINCREMENT,
           name TEXT NOT NULL,
           department TEXT NOT NULL,
           phone TEXT NOT NULL,
           email TEXT NOT NULL,
           office TEXT NOT NULL,
           introduction TEXT NOT NULL);''')
    
    # 学生表
    c.execute('''CREATE TABLE IF NOT EXISTS student
           (uuid INTEGER PRIMARY KEY AUTOINCREMENT,
           name TEXT NOT NULL,
           department TEXT NOT NULL,
           phone TEXT NOT NULL,
           email TEXT NOT NULL);''')
    
    # 教师空闲时间表
    c.execute('''CREATE TABLE IF NOT EXISTS teacher_time
           (teacher_uuid INTEGER,
           start_time TEXT NOT NULL,
           end_time TEXT NOT NULL,
           PRIMARY KEY (teacher_uuid, start_time, end_time));''')
    
    # 预约表
    c.execute('''CREATE TABLE IF NOT EXISTS appointment
           (number INTEGER PRIMARY KEY AUTOINCREMENT,
           student_uuid INTEGER NOT NULL,
           teacher_uuid INTEGER NOT NULL,
           start_time TEXT NOT NULL,
           end_time TEXT NOT NULL,
           status INTEGER NOT NULL,
           exception TEXT,
           application_time TEXT NOT NULL);''')
    
    # Cookie表
    c.execute('''CREATE TABLE IF NOT EXISTS cookie
           (uuid INTEGER PRIMARY KEY,
           cookie TEXT NOT NULL,
           role INTEGER NOT NULL);''')
    
    conn.commit()
    conn.close()

class Admin:
    def generateUUID(self):
        c = get_db().cursor()
        c.execute("SELECT COUNT(*) FROM user")
        count = c.fetchone()[0]
        return count + 1 + 100000
    
    def register(self, username, password, role, information_dict):
        db = get_db()
        c = db.cursor()
        uuid = self.generateUUID()
        # c.execute("INSERT INTO user (uuid, username, password, role, if_active) VALUES (?, ?, ?, ?, 0)", (uuid, username, password, role))
        c.execute("INSERT INTO user (uuid, username, password, role, if_active) VALUES (?, ?, ?, ?, 1)", (uuid, username, password, role))  # 将if_active设为1以自动激活用户 debug here
        if role == 1: # 学生
            c.execute("INSERT INTO student (uuid, name, department, phone, email) VALUES (?, ?, ?, ?, ?)", (uuid, information_dict['name'], information_dict['department'], information_dict['phone'], information_dict['email']))
        elif role == 2: # 教师
            c.execute("INSERT INTO teacher (uuid, name, department, phone, email, office, introduction) VALUES (?, ?, ?, ?, ?, ?, ?)", (uuid, information_dict['name'], information_dict['department'], information_dict['phone'], information_dict['email'], information_dict['office'], information_dict['introduction']))
            c.execute("INSERT INTO teacher_time (teacher_uuid, start_time, end_time) VALUES (?, '8:00', '20:00')", (uuid,))
        db.commit()
    
    def login(self, username, password):
        print("Login method called")  # 确认代码被执行
        c = get_db().cursor()
        c.execute("SELECT * FROM user WHERE username = ? AND password = ?", (username, password))
        result = c.fetchone()
        
        # 调试信息
        print(f"Login attempt for username: {username}")
        print(f"Query result: {result}")
        
        if result is None:
            print(f"Login failed for user: {username}. User not found or incorrect password.")
            return None
        
        if result[4] == 0:
            print(f"Login failed for user: {username}. User is not activated.")
            return None
        
        uuid = result[0]
        role = result[3]
        cookie = self.generateCookie()
        c.execute("INSERT OR REPLACE INTO cookie (uuid, cookie, role) VALUES (?, ?, ?)", (uuid, cookie, role))
        get_db().commit()
        return {"cookie_role": f"{cookie}{role}", "role": role}
    
    def getUnactiveUsers(self):
        c = get_db().cursor()
        c.execute("SELECT * FROM user WHERE if_active = 0")
        result = c.fetchall()
        return result if result else None
    
    def activeUser(self, uuid):
        c = get_db().cursor()
        c.execute("UPDATE user SET if_active = 1 WHERE uuid = ?", (uuid,))
        get_db().commit()
    
    @staticmethod
    def generateCookie():
        return ''.join(random.sample(string.ascii_letters + string.digits, 16))


    def __init__(self):
        self.conn = sqlite3.connect('TeacherInformationSystem.db', check_same_thread=False)
        self.c = self.conn.cursor()



class Teacher:
    def __init__(self):
        self.conn = sqlite3.connect('TeacherInformationSystem.db', check_same_thread=False)
        self.c = self.conn.cursor()
    
    def getInformation(self, cookie):
        self.c.execute("SELECT uuid FROM cookie WHERE cookie = ?", (cookie,))
        result = self.c.fetchone()
        if result is None:
            return None
        teacher_uuid = result[0]
        self.c.execute("SELECT * FROM teacher WHERE uuid = ?", (teacher_uuid,))
        result = self.c.fetchone()
        return result if result else None

    def setInformation(self, cookie, information_dict):
        self.c.execute("SELECT uuid FROM cookie WHERE cookie = ?", (cookie,))
        result = self.c.fetchone()
        if result is None or result[2] != 2:
            return None
        teacher_uuid = result[0]
        self.c.execute("UPDATE teacher SET name = ?, department = ?, phone = ?, email = ?, office = ?, introduction = ? WHERE uuid = ?", 
                       (information_dict['name'], information_dict['department'], information_dict['phone'], information_dict['email'], 
                        information_dict['office'], information_dict['introduction'], teacher_uuid))
        self.conn.commit()

    def getFreeTime(self, cookie):
        self.c.execute("SELECT uuid FROM cookie WHERE cookie = ?", (cookie,))
        result = self.c.fetchone()
        if result is None or result[2] != 2:
            return None
        teacher_uuid = result[0]
        self.c.execute("SELECT * FROM teacher_time WHERE teacher_uuid = ?", (teacher_uuid,))
        result = self.c.fetchall()
        return result if result else None

    def setFreeTime(self, cookie, start_time, end_time):
        self.c.execute("SELECT uuid FROM cookie WHERE cookie = ?", (cookie,))
        result = self.c.fetchone()
        if result is None or result[2] != 2:
            return None
        teacher_uuid = result[0]
        for i in range(len(start_time)):
            self.c.execute("UPDATE teacher_time SET start_time = ?, end_time = ? WHERE teacher_uuid = ?", (start_time[i], end_time[i], teacher_uuid))
        self.conn.commit()

    def getAppointment(self, cookie):
        self.c.execute("SELECT uuid FROM cookie WHERE cookie = ?", (cookie,))
        result = self.c.fetchone()
        if result is None or result[2] != 2:
            return None
        teacher_uuid = result[0]
        self.c.execute("SELECT * FROM appointment WHERE teacher_uuid = ?", (teacher_uuid,))
        result = self.c.fetchall()
        return result if result else None

    def acceptAppointment(self, cookie, appointnumber, exception):
        self.c.execute("SELECT uuid FROM cookie WHERE cookie = ?", (cookie,))
        result = self.c.fetchone()
        if result is None or result[2] != 2:
            return False
        teacher_uuid = result[0]
        self.c.execute("SELECT * FROM appointment WHERE number = ? AND teacher_uuid = ?", (appointnumber, teacher_uuid))
        result = self.c.fetchone()
        if result is None:
            return False
        self.c.execute("UPDATE appointment SET status = 1, exception = ? WHERE number = ? AND teacher_uuid = ?", (exception, appointnumber, teacher_uuid))
        self.conn.commit()

    def denyAppointment(self, cookie, appointnumber, exception):
        self.c.execute("SELECT uuid FROM cookie WHERE cookie = ?", (cookie,))
        result = self.c.fetchone()
        if result is None or result[2] != 2:
            return False
        teacher_uuid = result[0]
        self.c.execute("SELECT * FROM appointment WHERE number = ? AND teacher_uuid = ?", (appointnumber, teacher_uuid))
        result = self.c.fetchone()
        if result is None:
            return False
        self.c.execute("UPDATE appointment SET status = 2, exception = ? WHERE number = ? AND teacher_uuid = ?", (exception, appointnumber, teacher_uuid))
        self.conn.commit()

class Student:
    def __init__(self):
        self.conn = sqlite3.connect('TeacherInformationSystem.db', check_same_thread=False)
        self.c = self.conn.cursor()

    def getInformation(self, cookie):
        self.c.execute("SELECT uuid FROM cookie WHERE cookie = ?", (cookie,))
        result = self.c.fetchone()
        if result is None or result[2] != 1:
            return None
        student_uuid = result[0]
        self.c.execute("SELECT * FROM student WHERE uuid = ?", (student_uuid,))
        result = self.c.fetchone()
        return result if result else None

    def setInformation(self, cookie, information_dict):
        self.c.execute("SELECT uuid FROM cookie WHERE cookie = ?", (cookie,))
        result = self.c.fetchone()
        if result is None or result[2] != 1:
            return False
        student_uuid = result[0]
        self.c.execute("UPDATE student SET name = ?, department = ?, phone = ?, email = ? WHERE uuid = ?", 
                       (information_dict['name'], information_dict['department'], information_dict['phone'], information_dict['email'], student_uuid))
        self.conn.commit()
        return True

    def getAppointment(self, cookie):
        self.c.execute("SELECT uuid FROM cookie WHERE cookie = ?", (cookie,))
        result = self.c.fetchone()
        if result is None:
            return None
        student_uuid = result[0]
        self.c.execute("SELECT * FROM appointment WHERE student_uuid = ?", (student_uuid,))
        result = self.c.fetchall()
        return result if result else None

    def cancelAppointment(self, cookie, number):
        self.c.execute("SELECT uuid FROM cookie WHERE cookie = ?", (cookie,))
        result = self.c.fetchone()
        if result is None:
            return False
        student_uuid = result[0]
        self.c.execute("SELECT * FROM appointment WHERE number = ? AND student_uuid = ?", (number, student_uuid))
        result = self.c.fetchone()
        if result is None:
            return False
        self.c.execute("UPDATE appointment SET status = 3 WHERE number = ? AND student_uuid = ?", (number, student_uuid))
        self.conn.commit()
        return True

if __name__ == "__main__":
    initDB()
