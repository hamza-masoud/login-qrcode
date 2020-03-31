from flask import session, redirect, render_template
from App import app
from App.backend.Controllers.userController import userController
from App.backend.Controllers.adminController import adminController


@app.route('/', methods=['POST', 'GET'])
def main(): return userController().login()


@app.route('/create-user/', methods=['POST', 'GET'])
def new_user():
    return userController().create_user()


@app.route('/sign-in/', methods=['POST', 'GET'])
def signin():
    return userController().signin()


# ================____========||----\========
# ==============/     \=======||     \=======
# =============/       \======||      \======
# ============/         \=====||       \=====
# ===========/___________\====||        )====
# ==========/-------------\===||       /=====
# =========/               \==||      /======
# ========/                 \=||-----/=======

@app.route('/create-admin/', methods=['POST', 'GET'])
def new_admin():
    return adminController().create_admin()


@app.route('/admin/', methods=['POST', 'GET'])
def loginadmin():
    return adminController().loginadmin()


@app.route('/create-room/', methods=['POST', 'GET'])
def create_admin():
    return adminController().create_room()


@app.route('/admin/<string:roomid>')
def showRoom(roomid):
    return adminController().showRoom(roomid)


@app.route('/logout/')
def clearSession():
    session.clear()
    return redirect(app.config.app_url)


@app.errorhandler(404)
def error(e): return render_template("pages/error_page.html", message=e)
