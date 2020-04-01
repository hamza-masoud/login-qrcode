import os
import pytz
from App import app
from datetime import datetime as dt

app.secret_key = "data_convert"
app.config.app_url = "https://login-qrcode.herokuapp.com/"
# app.config.app_url = "http://127.0.0.1:5000/"


basedir = os.path.abspath(os.path.dirname(__file__))

basedir = basedir.split(os.sep)
basedir.remove(basedir[0])
basedir = os.sep.join(basedir)

download_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'QRimgs'))

app.config.file_name_length = 5

db_path = os.path.join(basedir, 'projectDB.db')

db_uri = 'sqlite:///{}'.format(db_path)
# app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgres://ezssqjvyoievzv:6bfd14bad593f36b68cc3880156673f4e8310b9039f2e0d0c98fc2d09def741b@ec2-52-71-85-210.compute-1.amazonaws.com:5432/deo6bpel8ivas1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['UPLOAD_FOLDER'] = 'QRimgs'


def timezone():
    d_naive = dt.utcnow()
    timezone = pytz.timezone("Asia/Gaza")
    d_aware = timezone.localize(d_naive)

    return d_aware
