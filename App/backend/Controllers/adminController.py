from flask import render_template, redirect, request, session
from App import app
from App.backend.securityClass import chick_the_request, random_filename
from App.backend.models import db, User, Rooms, Admin, signIn
import os
from App.backend.settings import basedir
import qrcode
from datetime import datetime


class adminController:

    def loginadmin(self):
        if request.method == 'GET':
            if check_admin_login():
                return self.showAdminPage()
            else:
                return render_template('pages/admin/loginAdmin.html')
        else:
            if chick_the_request(['username', 'password']):
                username = request.form['username']
                password = request.form['password']
                admin = Admin.query.filter_by(username=username).first()
                if admin:
                    if admin.password == password:
                        session['adminName'] = username
                        session['adminPW'] = password
                        session['admin_id'] = admin.id
                        return self.showAdminPage()
                    else:
                        return render_template('pages/admin/loginAdmin.html', message="error password")
                else:
                    return render_template('pages/admin/loginAdmin.html', message="error username")
            else:
                return render_template('pages/admin/loginAdmin.html', message="error in your request")

    def create_admin(self):
        if request.method == 'GET':
            return render_template("pages/admin/signupAdmin.html")
        else:
            if chick_the_request(['name', 'username', 'password']):
                name = request.form['name']
                username = request.form['username']
                password = request.form['password']

                user = Admin.query.filter_by(username=username).first()
                if user:
                    return render_template("pages/admin/signupAdmin.html", message="the username is already exist")
                else:
                    new_admin = Admin(name=name, username=username, password=password)
                    try:
                        db.session.add(new_admin)
                        db.session.commit()
                    except:
                        return "error to connect with db"
                    session['adminName'] = username
                    session['adminPW'] = password
                    username = Admin.query.filter_by(username=username).first()
                    session['admin_id'] = username.id
                    return self.showAdminPage()
            else:
                return render_template('pages/admin/signupAdmin.html', message="error in your request")

    def create_room(self):
        if request.method == 'POST':
            if check_admin_login():
                if chick_the_request(['roomName', 'time 1', 'time 2']):
                    adminid = session['admin_id']
                    name = request.form['roomName']
                    time1 = request.form['time 1']
                    time2 = request.form['time 2']
                    timeStart = datetime(
                        *[int(v) for v in time1.replace('T', '-').replace(':', '-').split('-')])
                    timeFinished = datetime(
                        *[int(v) for v in time2.replace('T', '-').replace(':', '-').split('-')])

                    roomid = random_filename()

                    new_room = Rooms(admin_id=adminid, name=name, random_id=roomid, timeStart=timeStart,
                                     timeFinished=timeFinished)
                    try:
                        db.session.add(new_room)
                        db.session.commit()

                    except:
                        return "error in connect with db"
                    create_QR(roomid)
                    return redirect(app.config.app_url + "admin/" + roomid)
                else:
                    return self.showAdminPage()
            else:
                return redirect(app.config.app_url + 'admin/')
        else:
            return redirect(app.config.app_url + 'admin/')

    def showAdminPage(self):
        if check_admin_login():
            hisRooms = Rooms.query.filter_by(admin_id=session['admin_id']).all()
            if not hisRooms:
                return render_template("pages/admin/adminPage.html", noRoom=True)
            return render_template("pages/admin/adminPage.html", roomslist=hisRooms)

    def showRoom(self, roomid):
        if check_admin_login():
            Room = Rooms.query.filter_by(admin_id=session['admin_id']).all()
            if not Room:
                return self.showAdminPage()
            users = []
            for room in Room:
                if roomid == room.random_id:

                    userloggedin = signIn.query.filter_by(room_id=roomid).all()
                    z = 0
                    for user in userloggedin:
                        name = User.query.filter_by(id=user.user_id).first()
                        users.append([z, name.name, name.username, user.time_login])
                        z += 1

                QR_url = os.path.join(basedir, "static", "imgs", "QRimg", roomid + ".png")
                if os.path.isfile(QR_url):
                    pass
                else:
                    create_QR(roomid)

                return render_template("pages/admin/admin_Room.html", room=room, users=users,
                                       imgurl=roomid + ".png")
        return redirect(app.config.app_url + "admin/")


def check_admin_login():
    if 'adminName' and 'adminPW' and 'admin_id' in session:
        admin_id = Admin.query.filter_by(id=session['admin_id']).first()
        if admin_id:
            if admin_id.username == session['adminName']:
                if admin_id.password == session['adminPW']:
                    return True
    return False


def create_QR(QR_code):
    qr = qrcode.make(QR_code)
    basedir = os.path.abspath(os.path.dirname(__file__))
    QR_url = os.path.join(basedir, "static", "imgs", "QRimg", QR_code + ".png")

    qr.save(QR_url)
    return QR_url
