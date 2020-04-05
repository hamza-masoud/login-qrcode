from flask import Flask
import os

app = Flask(__name__,
            template_folder=os.path.join("frontend", "templates"),
            static_folder=os.path.join("backend", "Controllers", "static"))

from App.backend import settings
from App.backend import route
