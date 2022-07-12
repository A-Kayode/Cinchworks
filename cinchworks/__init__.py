from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

app= Flask(__name__)
app.config.from_pyfile('config.py')
db= SQLAlchemy(app)
csrf= CSRFProtect(app)

from . import models
from .routes import admin_routes, customer_routes, routes, vendor_routes