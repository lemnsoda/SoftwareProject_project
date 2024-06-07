#教师信息管理系统
#能够通过系统查看教师的空闲状态并且对教师进行预约，
#教师可以通过系统修改和设置自己的空闲时间段，并且能够拒绝或接受学生的预约情况
#管理员可以在后台添加和删除教师
import sqlite3

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
    int status 0/1/2 0:待审核 1:已接受 2:已拒绝
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


'''
生成随机不重复的uuid
'''
def generateUUID():
    conn = sqlite3.connect('TeacherInformationSystem.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM user")
    count = c.fetchone()[0]
    conn.close()
    return count + 1 + 100000
'''
插入注册信息
username: 用户名
password: 密码
role: 角色 学生 1/教师 2/管理员 0
'''
def resgister(username, password, role):
    uuid = generateUUID()
    conn = sqlite3.connect('TeacherInformationSystem.db')
    c = conn.cursor()
    c.execute("INSERT INTO user (uuid, username, password, role, if_active) VALUES (?, ?, ?, ?, 0)", (uuid, username, password, role))
    conn.commit()
    conn.close()
'''
username: 用户名
password: 密码
result: 若成功登录，返回uuid，否则返回none
'''
def login(username, password):
    conn = sqlite3.connect('TeacherInformationSystem.db')
    c = conn.cursor()
    c.execute("SELECT * FROM user WHERE username = ? AND password = ?", (username, password))
    result = c.fetchone()
    conn.close()
    #判断是否被激活
    if result != None or result[4] == 0:
        return None
    return result[0]
'''
#获取注册但未被审核的用户信息
result: 查询结果，如果查询成功，则返回(uuid, username, password, role, if_active)，否则返回None
'''
def getUnactiveUsers():
    conn = sqlite3.connect('TeacherInformationSystem.db')
    c = conn.cursor()
    c.execute("SELECT * FROM user WHERE if_active = 0")
    result = c.fetchall()
    conn.close()
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