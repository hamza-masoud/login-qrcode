import pytz
from flask import request
from App import app
import random
import string
from datetime import datetime as dt
import datetime
from qrtools import qrtools
from PIL import Image


def chick_the_request(data):
    result = True
    for one in data:
        if one in request.form:
            if request.form[one] != '':
                pass
            else:
                return False
        else:
            return False
    return result


def random_filename():
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    ts = datetime.datetime.now().timestamp()
    random_key = ''.join(random.choice(letters) for i in range(app.config.file_name_length))
    return random_key + str(ts)


def check_file_from_html(file_from_html):
    if not request.files:
        return False
    if file_from_html not in request.files:
        error_message = "there is some error in the application, please replay your request"
        return error_message

    json_file = request.files[file_from_html]
    if json_file.filename == '':
        error_message = "there is some error in your request, please check that you uploaded a json file"
        return error_message

    return ""


def readQrcode(filename):
    qr = qrtools.QR()
    qr = qr.decode(Image.open(filename))

    if not qr.data:
        return ""
    else:
        return qr.data


def time_comparison(timeBefor, timeAfter):
    d_naive = dt.utcnow()
    timezone = pytz.timezone("Asia/Gaza")
    timenow = timezone.localize(d_naive)
    timenow = timenow + datetime.timedelta(hours=3)

    print(pytz.timezone("Asia/Gaza").localize(timeBefor))
    print(timenow)
    print(pytz.timezone("Asia/Gaza").localize(timeAfter))

    print(pytz.timezone("Asia/Gaza").localize(timeBefor) > timenow)
    # print(timenow)
    print(timenow > pytz.timezone("Asia/Gaza").localize(timeAfter))

    if pytz.timezone("Asia/Gaza").localize(timeBefor) > timenow > pytz.timezone("Asia/Gaza").localize(timeAfter):
        return True
    return False
