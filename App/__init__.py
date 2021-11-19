from flask import Flask
import os

app = Flask(__name__,
            template_folder=os.path.join("frontend", "templates"),
            static_folder=os.path.join("frontend", "static"))

from App.backend.models import db, migrate


from App.backend import settings
from App.backend import route
