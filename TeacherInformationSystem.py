#教师信息管理系统
#能够通过系统查看教师的空闲状态并且对教师进行预约，
#教师可以通过系统修改和设置自己的空闲时间段，并且能够拒绝或接受学生的预约情况
#管理员可以在后台添加和删除教师
import sqlite3
import random
import string
#初始化数据库
'''
user表：存储用户信息
    int uuid(主键)
    string username
    string password
    int role 学生 1/教师 2/管理员 0
    int if_active 是否激活 1/0
teacher表：存储教师基本信息
    int uuid(主键)
    string name //教师姓名
    string department //院系
    string phone //手机
    string email //邮箱
    string office //办公地点
    string introduction //简介
student表：存储学生基本信息
    int uuid(主键)
    string name //学生姓名
    string department //院系
    string phone //手机
    string email //邮箱
teacher_time表：存储教师空闲时间段
    int teacher_uuid //教师uuid
    String start_time //默认为8:00
    String end_time //默认为20:00
appointment表：存储预约信息
    int student_uuid(外键)
    int teacher_uuid(外键)
    String start_time
    String end_time
    String application_time //申请时间
    int status 0/1/2 0:待审核 1:已接受 2:已拒绝
cookie表：存储uuid对应的cooike字段
    int uuid(主键)
    string cookie
    int role
'''
def initDB():
    conn = sqlite3.connect('TeacherInformationSystem.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE user
           (uuid INTEGER PRIMARY KEY AUTOINCREMENT,
           username TEXT NOT NULL,
           password TEXT NOT NULL,
           role INTEGER NOT NULL,
           if_active INTEGER NOT NULL);''')
    c.execute('''CREATE TABLE teacher
           (uuid INTEGER PRIMARY KEY AUTOINCREMENT,
           name TEXT NOT NULL,
           department TEXT NOT NULL,
           phone TEXT NOT NULL,
           email TEXT NOT NULL,
           office TEXT NOT NULL,
           introduction TEXT NOT NULL);''')
    c.execute('''CREATE TABLE student
           (uuid INTEGER PRIMARY KEY AUTOINCREMENT,
           name TEXT NOT NULL,
           department TEXT NOT NULL,
           phone TEXT NOT NULL,
           email TEXT NOT NULL);''')
    c.execute('''CREATE TABLE teacher_time
           (teacher_uuid INTEGER PRIMARY KEY,
           start_time TEXT NOT NULL,
           end_time TEXT NOT NULL);''')
    c.execute('''CREATE TABLE appointment
           (student_uuid INTEGER NOT NULL,
           teacher_uuid INTEGER NOT NULL,
           start_time TEXT NOT NULL,
           end_time TEXT NOT NULL,
           status INTEGER NOT NULL);''')
    conn.commit()
    conn.close()



class admin():
    def __init__(self):
        self.conn = sqlite3.connect('TeacherInformationSystem.db')
        self.c = self.conn.cursor()
    '''
    生成一个随机的cookie字段
    '''
    def generateCookie():
        return ''.join(random.sample(string.ascii_letters + string.digits, 16))

    '''
    生成随机不重复的uuid
    '''
    def generateUUID(self):
        self.c.execute("SELECT COUNT(*) FROM user")
        count = self.c.fetchone()[0]
        return count + 1 + 100000
    '''
    插入注册信息
    username: 用户名
    password: 密码
    role: 角色 学生 1/教师 2/管理员 0
    information_dict: 注册信息字典，包含name, department, phone, email, (office, introduction)
    '''
    def resgister(username, password, role, information_dict):
        uuid = admin.generateUUID()
        conn = sqlite3.connect('TeacherInformationSystem.db')
        c = conn.cursor()
        c.execute("INSERT INTO user (uuid, username, password, role, if_active) VALUES (?, ?, ?, ?, 0)", (uuid, username, password, role))
        if role == 1:#是学生
            c.execute("INSERT INTO student (uuid, name, department, phone, email) VALUES (?, ?, ?, ?, ?)", (uuid, information_dict['name'], information_dict['department'], information_dict['phone'], information_dict['email']))
        elif role == 2:#是教师
            c.execute("INSERT INTO teacher (uuid, name, department, phone, email, office, introduction) VALUES (?, ?, ?, ?, ?, ?, ?)", (uuid, information_dict['name'], information_dict['department'], information_dict['phone'], information_dict['email'], information_dict['office'], information_dict['introduction']))
            c.execute("INSERT INTO teacher_time (teacher_uuid, start_time, end_time) VALUES (?, '8:00', '20:00')", (uuid,))
        conn.commit()
        conn.close()
    '''
    username: 用户名
    password: 密码
    result: 若成功登录，返回uuid * 10 + role，这样可以通过uuid和role来确定用户身份，否则返回None
    '''
    def login(username, password):
        conn = sqlite3.connect('TeacherInformationSystem.db')
        c = conn.cursor()
        c.execute("SELECT * FROM user WHERE username = ? AND password = ?", (username, password))
        result = c.fetchone()
        #判断是否被激活
        if result == None or result[4] == 0:
            return None
        uuid = result[0]
        cookie = admin.generateCookie()
        c.execute("INSERT INTO cookie (uuid, cookie, role) VALUES (?, ?, ?)", (uuid, cookie, result[3]))
        conn.commit()
        conn.close()
        return cookie + str(result[3])
    '''
    #获取注册但未被审核的用户信息
    result: 查询结果，如果查询成功，，否则返回None
    '''
    def getUnactiveUsers(self):
        self.c.execute("SELECT * FROM user WHERE if_active = 0")
        result = self.c.fetchall()
        if result == None:
            return None
        #返回所有结果
        return result
    '''
    激活选中的用户
    todo:将选中的用户的if_active字段设置为1
    '''
    def activeUser(uuid):
        conn = sqlite3.connect('TeacherInformationSystem.db')
        c = conn.cursor()
        c.execute("UPDATE user SET if_active = 1 WHERE uuid = ?", (uuid,))
        conn.commit()
        conn.close()

class teacher():
    def __init__(self):
        self.conn = sqlite3.connect('TeacherInformationSystem.db')
        self.c = self.conn.cursor()
    '''
    获取教师的基本信息
    result: 查询结果，如果查询成功，返回查询结果，否则返回None
    '''
    def getInformation(self, cookie):
        self.c.execute("SELECT uuid FROM cookie WHERE cookie = ?", (cookie,))
        result = self.c.fetchone()
        if result is None:
            return None
        teacher_uuid = result[0]
        self.c.execute("SELECT * FROM teacher WHERE uuid = ?", (teacher_uuid,))
        result = self.c.fetchone()
        if result is None:
            return None
        return result

    '''
    修改教师的基本信息
    '''
    def setInformation(self,cookie, information_dict):
        self.c.execute("SELECT uuid FROM cookie WHERE cookie = ?", (cookie,))
        result = self.c.fetchone()
        if result is None:
            return None
        role = result[1]
        if role != 2:
            return None
        teacher_uuid = result[0]
        self.c.execute("UPDATE teacher SET name = ?, department = ?, phone = ?, email = ?, office = ?, introduction = ? WHERE uuid = ?", (information_dict['name'], information_dict['department'], information_dict['phone'], information_dict['email'], information_dict['office'], information_dict['introduction'], teacher_uuid))
        self.conn.commit()
        
    '''
    获取教师的空闲时间段
    result: 查询结果，如果查询成功，返回查询结果，否则返回None
    '''
    def getFreeTime(self, cookie):
        self.c.execute("SELECT uuid FROM cookie WHERE cookie = ?", (cookie,))
        result = self.c.fetchone()
        if result is None:
            return None
        if result[2] != 2:
            return None
        teacher_uuid = result[0]
        self.c.execute("SELECT * FROM teacher_time WHERE teacher_uuid = ?", (teacher_uuid,))
        result = self.c.fetchall()
        if result is None:
            return None
        return result
    '''
    设置教师的空闲时间段
    start_time: 开始时间列表
    end_time: 结束时间列表
    例子：start_time = ['8:00', '10:00'], end_time = ['9:00', '11:00']
    标识8:00-9:00和10:00-11:00两个时间段是空闲的
    '''
    def setFreeTime(self,cookie,start_time, end_time):
        self.c.execute("SELECT uuid FROM cookie WHERE cookie = ?", (cookie,))
        result = self.c.fetchone()
        if result is None:
            return None
        if result[2] != 2:
            return None
        teacher_uuid = result[0]
        for i in range(len(start_time)):
            self.c.execute("UPDATE teacher_time SET start_time = ?, end_time = ? WHERE teacher_uuid = ?", (start_time[i], end_time[i], teacher_uuid))
        self.conn.commit()

    '''
    获取教师的预约信息
    result: 查询结果，如果查询成功，返回查询结果，否则返回None
    '''
    def getAppointment(self, cookie):
        self.c.execute("SELECT uuid FROM cookie WHERE cookie = ?", (cookie,))
        result = self.c.fetchone()
        if result is None:
            return None
        if result[2] != 2:
            return None
        teacher_uuid = result[0]
        self.c.execute("SELECT * FROM appointment WHERE teacher_uuid = ?", (teacher_uuid,))
        result = self.c.fetchall()

        if result is None:
            return None
        return result

    '''
    接受或拒绝学生的预约
    student_uuid: 学生uuid
    status: 0/1/2 0:待审核 1:已接受 2:已拒绝
    '''
    def dealAppointment(self, cookie, student_uuid, status):
        self.c.execute("SELECT uuid FROM cookie WHERE cookie = ?", (cookie,))
        result = self.c.fetchone()
        if result is None:
            return None
        if result[2] != 2:
            return None
        teacher_uuid = result[0]
        self.c.execute("UPDATE appointment SET status = ? WHERE student_uuid = ? AND teacher_uuid = ?", (status, student_uuid, teacher_uuid))
        self.conn.commit()
