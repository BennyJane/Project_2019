#!/usr/bin/env python
# # -*- coding:utf-8 -*-
from flask import Flask, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
# import pymysql
import os

base_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__,
            static_folder='static',
            template_folder="templates",
            static_url_path="/1212"
            )

# app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:root@localhost/main'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'FLogin.sqlite')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class User(db.Model):
    # 定义表名
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(18), unique=True, )
    password = db.Column(db.String(18))
    type = db.Column(db.String(2))
    sid = db.Column(db.Integer, db.ForeignKey("Student.sid"))
    tid = db.Column(db.Integer, db.ForeignKey("Teacher.tid"))


class Major(db.Model):
    __tablename__ = "Major"
    mid = db.Column(db.Integer, autoincrement=True, primary_key=True)
    mname = db.Column(db.String(255))
    sid = db.relationship('Student', backref='Major', lazy='dynamic')
    tid = db.relationship('Teacher', backref='Major', lazy='dynamic')
    cid = db.relationship('Course', backref='Major', lazy='dynamic')
    clid = db.relationship('Class', backref='Major', lazy='dynamic')


class Student(db.Model):
    # 定义表名
    __tablename__ = "Student"
    sid = db.Column(db.Integer, autoincrement=True, primary_key=True)
    sname = db.Column(db.String(18))
    samount = db.Column(db.Integer, default=1)
    major = db.Column(db.String(64), db.ForeignKey("Major.mname"))
    a_sid = db.relationship('Attendance', backref='Student', lazy='dynamic')
    teacher = db.relationship('Teacher', backref="Student", lazy="dynamic")
    login = db.relationship('User', backref="Student", lazy="dynamic")
    course = db.relationship('Course', backref="Student", lazy="dynamic")


class Teacher(db.Model):
    __tablename__ = "Teacher"
    tid = db.Column(db.Integer, autoincrement=True, primary_key=True)
    tname = db.Column(db.String(18), unique=True)
    annocement = db.Column(db.String(260))
    major = db.Column(db.String(64), db.ForeignKey("Major.mname"))
    teacher = db.relationship('Attendance', backref='Teacher', lazy='dynamic')
    sid = db.Column(db.Integer, db.ForeignKey("Student.sid"))
    login = db.relationship('User', backref="Teacher", lazy="dynamic")
    course = db.relationship('Course', backref="Teacher", lazy="dynamic")


class Course(db.Model):
    __tablename__ = "Course"
    cid = db.Column(db.Integer, autoincrement=True, primary_key=True)
    cname = db.Column(db.String(18))
    camount = db.Column(db.Integer)
    day = db.Column(db.String(10))
    time = db.Column(db.String(20))
    major = db.Column(db.String(64), db.ForeignKey("Major.mname"))
    classid = db.Column(db.String(18), db.ForeignKey("Class.clid"))
    timetableid = db.Column(db.Integer, db.ForeignKey("Timetable.tiid"))
    sid = db.Column(db.Integer, db.ForeignKey("Student.sid"))
    tid = db.Column(db.Integer, db.ForeignKey("Teacher.tid"))


class Class(db.Model):
    __tablename__ = "Class"
    clid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    clname = db.Column(db.String(30))
    cltime = db.Column(db.String(20))
    clamount = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    major = db.Column(db.String(64), db.ForeignKey("Major.mname"))
    cid = db.relationship('Course', backref="Class", lazy="dynamic")


class Timetable(db.Model):
    __tablename__ = "Timetable"
    tiid = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(20))
    time = db.Column(db.String(20))
    cid = db.relationship('Course', backref="Timetable", lazy="dynamic")


class Attendance(db.Model):
    __tablename__ = "Attendance"
    aid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.String(18))
    attendance = db.Column(db.String(18))
    reason = db.Column(db.String(18))
    teacher = db.Column(db.String(18), db.ForeignKey("Teacher.tname"))
    sid = db.Column(db.Integer, db.ForeignKey("Student.sid"))


db.drop_all()
db.create_all()

db.session.add_all([
    Major(mname="CST"),
    Major(mname="DS"),
    Student(sid="1001", sname="Mark", major="CST"),
    Student(sid="1002", sname="TY", major="CST"),
    Teacher(tid="2001", tname="WW", major="DS", annocement="Yes"),
    Teacher(tid="2002", tname="YY", major="CST", annocement="No"),
    Course(cname="Database", camount="50", major="CST", day="Monday", time="8:00-8:50"),
    Attendance(sid="1001", date="2020-5-23", attendance="Present", reason=""),
    Attendance(sid="1001", date="2020-5-24", attendance="Present", reason=""),
    Attendance(sid="1002", date="2020-5-24", attendance="Present", reason="")
])
db.session.commit()


def regisetr(username, password, type):
    # 注册
    usr = User(username=username, password=password, type=type)
    try:
        db.session.add(usr)
        db.session.commit()
        return 1
    except:
        return 0


def login(username, password, type):
    usr = User()
    try:
        exists = usr.query.filter_by(username=username, password=password, type=type).first()
        return exists
    except:
        return 0


@app.route('/', methods=["GET", "POST"])
@app.route('/login', methods=["GET", "POST"])
def index():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        print(request.values)
        op = request.values.get("op")
        username = request.values.get("username")
        password = request.values.get("password")

        # 判断是否选择身份
        if op == "0":
            msg = {
                'info_notchose': 'Please select the correct login identity'
            }
            return render_template('login.html', **msg)
        else:
            data = login(username, password, op)
            if data == None or data == 0:
                print("login failed")
                msg = {
                    "up": "Username or password or id error！ "
                }
                return render_template('login.html', **msg)
            else:
                msg = {"data": data}
                if op == "1":
                    return render_template('teacher_main.html', **msg)
                if op == "2":
                    return render_template('Administrator Main.html', **msg)
                if op == "3":
                    return render_template('student_main.html', **msg)


@app.route("/re", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template('reg.html')
    else:
        print(request.values)
        op = request.values.get("op")
        username = request.values.get("username")
        password = request.values.get("password")
        if op == "0":
            data = {"re": "Registration failed, please select the correct identity!"}
            return render_template('reg.html', **data)
        f = regisetr(username, password, op)
        if f == 1:
            data = {"succ": "Successfully register, click ok to jump to the home page to log in, please log in！"}
            return render_template('reg.html', **data)
        else:
            data = {"re": "Registration failed, username already exists"}
            return render_template('reg.html', **data)


@app.route('/Administrator_Main')
def Administrator_Main():
    return render_template('Administrator Main.html')


@app.route('/adm_addT&S')
def adm_addTS():
    return render_template('adm_addT&S.html')


@app.route('/adm_allmanage')
def adm_allmanage():
    return render_template('adm_allmanage.html')


@app.route('/adm_Assign')
def adm_Assign():
    if request.method == 'GET':
        return render_template('adm_Assign.html')
    if request.method == "POST":
        print(request.values)
        course_id = request.values.get("course_id")
        student_id = request.values.get("student_id")
        teacher_id = request.values.get("teacher_id")
        schedule_time = request.values.get('schedule_time')

        try:
            cou = Course(course_id=course_id, student_id=student_id, teacher_id=teacher_id, schedule_time=schedule_time)
            # f=is_created(major,course_id,course_name,number_of_student)
            db.session.add(cou)
            db.session.commit()
            return render_template('adm_Assign.html')

        except Exception as e:
            print(e)
            return render_template('adm_Assign.html')

    return render_template('adm_Assign.html')


@app.route('/adm_bulletin')
def adm_bulletin():
    return render_template('adm_bulletin.html')


@app.route('/adm_cancellation')
def adm_cancellation():
    return render_template('adm_cancellation.html')


@app.route('/adm_classmanage', methods=["GET", "POST"])
def adm_classmanage():
    print(request.values)
    op = request.values.get("op")
    username = request.values.get("username")
    password = request.values.get("password")
    data = login(username, password, op)
    msg = {"data": data}
    return render_template('adm_classmanage.html', **msg)


@app.route('/adm_createclass')
def adm_createclass():
    if request.method == 'GET':
        return render_template('adm_createclass.html')
    if request.method == "POST":
        print(request.values)
        major = request.values.get("major")
        course_id = request.values.get("ID")
        course_name = request.values.get("Name")
        number_of_student = request.values.get('Number')
        try:
            cla = Major(major=major, courser_id=course_id, courser_name=course_name,
                        number_of_student=number_of_student)
            # f=is_created(major,course_id,course_name,number_of_student)
            db.session.add(cla)
            db.session.commit()
            return render_template('adm_classmanage.html')

        except Exception as e:
            print(e)
            return render_template('adm_classmanage.html')


@app.route('/adm_delete')
def adm_delete():
    if request.method == 'GET':
        return render_template('adm_delete.html')
    if request.method == "POST":
        major = request.values.get("major")
        course_id = request.values.get("course_id")
        course_name = request.values.get("course_name")
        # number_of_student = request.values.get('number_of_student')

        try:
            major = Major()
            delete_major = major.query.filter_by(course_id=course_id).first()

            db.session.delete(delete_major)
            db.session.commit()

            return render_template('adm_delete.html')

        except Exception as e:
            print(e)
            return render_template('adm_delete.html')


@app.route('/adm_detail')
def adm_detail():
    if request.method == 'GET':
        return render_template('adm_detail.html')
    if request.method == "POST":
        op = request.values.get("op")
        major_name = request.values.get("major_name")

        if op == 1:
            id = request.values.get("teacher_id")
            tea = Teacher()
            data = tea.query.filter_by(teacher_id=id)
            return render_template('adm_detail.html', **data)

        if op == 3:
            id = request.values.get("student_id")
            stu = Student()
            data = stu.query.filter_by(student_id=id)
            return render_template('adm_detail.html', **data)

    return render_template('adm_detail.html')


@app.route('/adm_search')
def adm_search():
    return render_template('adm_search.html')


@app.route('/student_main')
def student_main():
    return render_template('student_main.html')


@app.route('/teacher_main')
def teacher_main():
    return render_template('teacher_main.html')


@app.route('/attendance')
# attentance
def attendance():
    if request.method == "GET":
        attendance = db.session.query(Student.sname, Student.sid).all()
        return render_template('attendance.html', attendance=attendance)


@app.route('/attendance2')
# attendance check
def attendance2():
    if request.method == "GET":
        return render_template('attendance2.html')
    if request.method == "POST":
        studentname = db.session.query(Student.sname).first()
        studentnumber = db.session.query(Student.sid).first()
        date = request.values.get("date")
        attendance = request.values.get("attendance")
        reason = request.values.get("reason")
        if date == None or date == 0:
            message = "Please choose date!"
            return render_template('attendance2.html', studentname=studentname, studentnumber=studentnumber,
                                   message=message)
        else:
            db.session.add(Attendance(date=date))
            db.session.commit()
        if attendance == None or attendance == 0:
            attendance = "Absent"
            db.session.add(Attendance(attendance=attendance))
            db.session.commit()
            return render_template('attendance2.html', studentname=studentname, studentnumber=studentnumber)
        else:
            attendance = "Present"
            db.session.add(Attendance(attendance=attendance))
            db.session.commit()
        if (reason == None or reason == 0) & Attendance.attendance == "Present":
            reason = "None"
            db.session.add(Attendance(reason=reason))
            db.session.commit()
            return render_template('attendance2.html', studentname=studentname, studentnumber=studentnumber)
        elif (reason == None or reason == 0) & Attendance.attendance == "Absent":
            message = "Please input the reaason!"
            return render_template('attendance2.html', studentname=studentname, studentnumber=studentnumber,
                                   message=message)
        else:
            db.session.add(Attendance(reason=reason))
            db.session.commit()
        return render_template('attendance2.html', studentname=studentname, studentnumber=studentnumber,
                               date=date, attendance=attendance, reason=reason)


@app.route('/bulletin')  # display the content in the bulletin
def bulletin():
    if request.method == "GET":
        return render_template('bulletin.html')
    else:
        if (Teacher.tid == User.id):
            bulletindisplay = db.session.query(Teacher.tid).join(User.username).filter(Teacher.annocement).all()
            bulletintext = request.args.get("bulletintext")
            db.session.add(Teacher(annocement=bulletintext))
            db.session.commit()
            return render_template('bulletin.html', bulletindisplay=bulletindisplay, bulletintext=bulletintext)


@app.route('/check')
def check():
    check = db.session.query(Student.sname, Student.sid)
    return render_template('check.html', check=check)


@app.route('/check2')
def check2():
    studentname = db.session.query(Student.sname).first()
    studentnumber = db.session.query(Student.sid).first()
    date = db.session.query(Attendance.date).first()
    attendance = db.session.query(Attendance.attendance).first()
    reason = db.session.query(Attendance.reason).first()
    return render_template('check2.html', studentname=studentname, studentnumber=studentnumber,
                           date=date, attendance=attendance, reason=reason)


@app.route('/course')
def course():
    course = db.session.query(Course.cname).all()
    return render_template('course.html', course=course)


@app.route('/course2')
def course2():
    course2 = request.form.get("course2")
    return render_template('course2.html', course2=course2)


@app.route('/student_attendance')  # display the content in the bulletin
def student_attendance():
    date = db.session.query(Attendance.date).filter(Attendance.sid == User.username).all()
    attendance = db.session.query(Attendance.attendance).filter(Attendance.sid == User.username).all()
    reason = db.session.query(Attendance.reason).filter(Attendance.sid == User.username).all()
    teacher = db.session.query(Attendance.teacher).filter(Attendance.sid == User.username).all()
    return render_template('student_attendance.html', date=date, attendance=attendance, reason=reason, teacher=teacher)


@app.route('/student_bulletin')  # display the content in the bulletin
def student_bulletin():
    s_bulletintext = db.session.query(Teacher.annocement).all()
    return render_template('student_bulletin.html', s_bulletintext=s_bulletintext)


@app.route('/student_course', methods=["GET"])  # display the content in the bulletin
def student_course():
    return render_template('student_course.html')


@app.route('/management')
def management():
    def management():
        return render_template('management.html')


@app.route('/adm_timetable')
def adm_timetable():
    return ''


class Config(object):
    pass


app.config.from_object(Config)

if __name__ == '__main__':
    # db.create_all()
    app.run(host="127.0.0.1", port=8022, debug=True)
