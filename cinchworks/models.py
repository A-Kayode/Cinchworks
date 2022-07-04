from . import db

class Customers(db.Model):
    cus_id= db.Column(db.Integer(), primary_key=True, autoincrement=True)
    cus_fname= db.Column(db.String(255), nullable=False)
    cus_lname= db.Column(db.String(255), nullable=False)
    cus_phone1= db.Column(db.String(40))
    cus_phone2= db.Column(db.String(40))
    cus_email= db.Column(db.String(255), nullable=False)
    cus_address= db.Column(db.String(255))
    cus_city= db.Column(db.String(150))
    cus_state= db.Column(db.Integer())
    cus_username= db.Column(db.String(255), unique=True, nullable=False)
    cus_password= db.Column(db.String(100), nullable=False)
