from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate

app= Flask(__name__)
app.config.from_pyfile('config.py')
db= SQLAlchemy(app)
migrate= Migrate(app, db)
csrf= CSRFProtect(app)

from . import models
from .routes import admin_routes, customer_routes, routes, vendor_routes