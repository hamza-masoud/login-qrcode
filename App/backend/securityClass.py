import pytz
from flask import request
from App import app
import random
import string
from datetime import datetime as dt
import datetime
import zxing


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
    reader = zxing.BarCodeReader()
    barcode = reader.decode(filename)
    if barcode:
        return barcode.raw
    else:
        return ""

def time_comparison(timeBefor, timeAfter):
    d_naive = dt.utcnow()
    timezone = pytz.timezone("Asia/Gaza")
    timenow = timezone.localize(d_naive)
    timenow = timenow + datetime.timedelta(hours=3)

    if pytz.timezone("Asia/Gaza").localize(timeBefor) > timenow > pytz.timezone("Asia/Gaza").localize(timeAfter):
        return True
    return False
