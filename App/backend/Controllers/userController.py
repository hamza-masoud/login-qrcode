from flask import render_template, redirect, request, session
from App import app
from App.backend.securityClass import chick_the_request
from App.backend.models import db, User, Rooms, signIn
from App.backend.securityClass import time_comparison, readQrcode
import base64
import os


class userController:

    def login(self):
        if request.method == 'POST':
            if chick_the_request(["username", "password"]):
                username = request.form['username']
                password = request.form['password']
                userfromdb = User.query.filter_by(username=username).first()
                if userfromdb:
                    if userfromdb.password == password:
                        session['user_id'] = userfromdb.id
                        session['username'] = username
                        session['password'] = password
                        return render_template("pages/user/logIn.html")

                    else:
                        return render_template("pages/user/signIn.html",
                                               message="the username or password is incorrect")
                else:
                    return render_template("pages/user/signIn.html", message="the username or password is incorrect")

            return render_template("pages/user/signIn.html", message="the username or password is incorrect")

        elif request.method == 'GET':
            if check_user_login():
                return render_template("pages/user/logIn.html")
            else:
                return render_template("pages/user/signIn.html")

    def signin(self):
        if request.method == 'POST':
            if check_user_login():
                if chick_the_request(['img-text']):
                    imgstring = request.form['img-text']
                    imgdata = base64.b64decode(imgstring.split(",")[1])
                    filename = 'test.jpg'
                    with open(filename, 'wb') as f:
                        f.write(imgdata)
                    QRNcode = readQrcode('test.jpg')
                    os.remove('test.jpg')
                    roomid = Rooms.query.filter_by(random_id=QRNcode).first()
                    if roomid:
                        if time_comparison(roomid.timeFinished, roomid.timeStart):
                            checksignin = signIn.query.filter_by(user_id=session['user_id']).all()
                            for once in checksignin:
                                if once.room_id == roomid.random_id:
                                    return render_template("pages/user/result_login.html", exist=True)
                            loginUser = signIn(user_id=session['user_id'], room_id=roomid.random_id)
                            try:
                                db.session.add(loginUser)
                                db.session.commit()
                            except:
                                return "error connect with db"
                            return render_template("pages/user/result_login.html")
                        return render_template("pages/user/logIn.html", timeout=True)
                    return render_template("pages/user/logIn.html", error=True)
                return render_template("pages/user/logIn.html", error=True)
        return redirect(app.config.app_url)

    def create_user(self):
        if request.method == 'GET':
            return render_template("pages/user/signUp.html")

        else:
            if chick_the_request(['name', 'username', 'password']):
                name = request.form['name']
                username = request.form['username']
                password = request.form['password']

                user = User.query.filter_by(username=username).first()
                if user:
                    return render_template("pages/user/signUp.html", message="the username is already exist")

                else:
                    new_user = User(name=name, username=username, password=password)
                    try:
                        db.session.add(new_user)
                        db.session.commit()
                    except:
                        return "error in connect with db"
                    x = User.query.filter_by(username=username).first()
                    session['user_id'] = x.id
                    session['username'] = username
                    session['password'] = password
                    return render_template("pages/user/logIn.html")

            else:
                return render_template('pages/user/signUp.html', message="error in your request")


def check_user_login():
    if 'username' and 'password' and 'user_id' in session:

        user = User.query.filter_by(id=session['user_id']).first()
        if user:
            if str(user.username) == str(session['username']):
                if user.password == session['password']:
                    return True
    return False
