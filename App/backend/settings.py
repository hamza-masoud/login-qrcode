import os
import pytz
from App import app
from datetime import datetime as dt

app.secret_key = "data_convert"
app.config.app_url = "http://127.0.0.1:5000/"
# app.config.app_url = "http://127.0.0.1:5000/"


basedir = os.path.abspath(os.path.dirname(__file__))
QR_img_path = os.path.join(os.getcwd(), "App", "frontend", "static", "imgs", "QRimg")

download_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'QRimgs'))

app.config.file_name_length = 5

db_path = os.path.join(basedir, 'projectDB.db')

db_uri = 'sqlite:///{}'.format(db_path)
# app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres: // vhfzhvczitammi: 9bdfbef60d72378a2bb676b1f9be6b72bedb00131e20f831d13404301b8bd481@ec2-63-32-173-118.eu-west-1.compute.amazonaws.com: 5432/dd3i3a936je4up'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['UPLOAD_FOLDER'] = 'QRimgs'


def timezone():
    d_naive = dt.utcnow()
    timezone = pytz.timezone("Asia/Gaza")
    d_aware = timezone.localize(d_naive)

    return d_aware
