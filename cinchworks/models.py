import enum
from datetime import datetime
from sqlalchemy import ForeignKey, func, Enum
from . import db

class Location(enum.Enum):
    vendor_address= "vendor shop"
    customer_address= "customer home"

class Status(enum.Enum):
    active= "confirmed booking"
    pending= "unconfirmed booking"
    cancelled= "cancelled booking"
    completed= "completed booking"
    rejected= "rejected booking"


class Customer(db.Model):
    cus_id= db.Column(db.Integer(), primary_key=True, autoincrement=True)
    cus_fname= db.Column(db.String(255), nullable=False)
    cus_lname= db.Column(db.String(255), nullable=False)
    cus_phone1= db.Column(db.String(40))
    cus_phone2= db.Column(db.String(40))
    cus_email= db.Column(db.String(255), nullable=False)
    cus_address= db.Column(db.String(255))
    cus_city= db.Column(db.String(150))
    cus_lga= db.Column(db.Integer(), db.ForeignKey('lga.lga_id'))
    cus_state= db.Column(db.Integer(), db.ForeignKey('state.state_id'))
    cus_username= db.Column(db.String(255), unique=True, nullable=False)
    cus_password= db.Column(db.String(255), nullable=False)
    cus_profilepic= db.Column(db.String(255))
    cus_regdate= db.Column(db.DateTime(), nullable=False, default=func.now(), onupdate=func.now())

    customer_state= db.relationship('State', backref='customer_info')
    customer_lga= db.relationship('Lga', backref='customers')

class Vendor(db.Model):
    ven_id= db.Column(db.Integer(), primary_key=True, autoincrement=True)
    ven_fname= db.Column(db.String(255), nullable=False)
    ven_lname= db.Column(db.String(255), nullable=False)
    ven_busname= db.Column(db.String(255), unique=True)
    ven_phone1= db.Column(db.String(40), unique=True)
    ven_phone2= db.Column(db.String(40), unique=True)
    ven_email= db.Column(db.String(255), unique=True, nullable=False)
    ven_address= db.Column(db.String(255))
    ven_city= db.Column(db.String(150))
    ven_lga= db.Column(db.Integer(), db.ForeignKey('lga.lga_id'))
    ven_state= db.Column(db.Integer(), db.ForeignKey('state.state_id'))
    ven_username= db.Column(db.String(255), unique=True, nullable=False)
    ven_password= db.Column(db.String(255), nullable=False)
    ven_shortdesc= db.Column(db.String(255))
    ven_openingtime= db.Column(db.Time())
    ven_closingtime= db.Column(db.Time())
    ven_bannerpic= db.Column(db.String(255))
    ven_profilepic= db.Column(db.String(255))
    ven_regdate= db.Column(db.DateTime(), nullable=False, default=func.now(), onupdate=func.now())

    vendor_state= db.relationship('State', backref='vendor_info')
    vendor_lga= db.relationship('Lga', backref='vendors')


class State(db.Model):
    state_id= db.Column(db.Integer(), primary_key=True, autoincrement=True)
    state_name= db.Column(db.String(75), nullable=False)


class Lga(db.Model):
    lga_id= db.Column(db.Integer(), primary_key=True, autoincrement=True)
    state_id= db.Column(db.Integer(), db.ForeignKey('state.state_id'), nullable=False)
    lga_name= db.Column(db.String(50), nullable=False)

    lga_state= db.relationship('State', backref='local_govt')

class Reviews(db.Model):
    review_id= db.Column(db.Integer(), primary_key=True, autoincrement=True)
    r_customer= db.Column(db.Integer(), db.ForeignKey('customer.cus_id'), nullable=False)
    r_vendor= db.Column(db.Integer(), db.ForeignKey('vendor.ven_id'), nullable=False)
    review_date= db.Column(db.Date(), default=func.now(), onupdate=func.now())
    review_score= db.Column(db.Integer(), nullable=False)
    review_desc= db.Column(db.Text(), nullable=False)

    cus_info= db.relationship('Customer', backref='cus_reviews')
    ven_info= db.relationship('Vendor', backref='ven_reviews')


class Vendor_services(db.Model):
    ven_service_id= db.Column(db.Integer(), primary_key=True, autoincrement=True)
    vendor_id= db.Column(db.Integer(), db.ForeignKey('vendor.ven_id'))
    service_id= db.Column(db.Integer(), db.ForeignKey('services.service_id'))
    short_desc= db.Column(db.String(255), nullable=False, default="Input short description here")
    long_desc= db.Column(db.Text())
    service_price= db.Column(db.Float(), nullable=False, default='0.00')
    average_duration= db.Column(db.String(100))
    min_duration= db.Column(db.String(100))
    max_duration= db.Column(db.String(100))
    avgdur_text= db.Column(db.String(100))
    mindur_text= db.Column(db.String(100))
    maxdur_text= db.Column(db.String(100))

    ven_info= db.relationship('Vendor', backref='ven_services')
    service= db.relationship('Services', backref= 'service_vendors')


class Services(db.Model):
    service_id= db.Column(db.Integer(), primary_key=True, autoincrement=True)
    service_name= db.Column(db.String(150), nullable=False)
    ser_category= db.Column(db.Integer(), db.ForeignKey('service_category.category_id'), nullable=False)

    category= db.relationship('Service_category', backref='services')


class Service_category(db.Model):
    category_id= db.Column(db.Integer(), primary_key=True, autoincrement=True)
    category_name= db.Column(db.String(150), nullable=False)


class Booking(db.Model):
    booking_id= db.Column(db.Integer(), primary_key=True, autoincrement=True)
    b_vendor= db.Column(db.Integer(), db.ForeignKey('vendor.ven_id'), nullable=False)
    b_customer= db.Column(db.Integer, db.ForeignKey('customer.cus_id'), nullable=False)
    b_venservice= db.Column(db.Integer, db.ForeignKey('vendor_services.ven_service_id'), nullable=False)
    booking_date= db.Column(db.DateTime(), nullable=False, default=func.now(), onupdate=func.now())
    service_location= db.Column(db.Enum(Location), nullable=False)
    confirmation_status= db.Column(db.Enum(Status), nullable=False)
    calender_date= db.Column(db.Date(), nullable=False)
    calender_time= db.Column(db.Time(), nullable=False)
    calender_endtime= db.Column(db.Time(), nullable=False)
    notes= db.Column(db.Text())

    ven_info= db.relationship('Vendor', backref='ven_bookings')
    cus_info= db.relationship('Customer', backref='cus_bookings')
    service_info= db.relationship('Vendor_services', backref='service_bookings')


class Calender(db.Model):
    calen_id= db.Column(db.Integer(), primary_key=True, autoincrement=True)
    c_offday= db.Column(db.Integer(), db.ForeignKey('offday.off_id'))
    c_booking= db.Column(db.Integer(), db.ForeignKey('booking.booking_id'))

    booking= db.relationship('Booking', backref='calender')
    offday= db.relationship('Offday', backref='calender')


class Offday(db.Model):
    off_id= db.Column(db.Integer(), primary_key=True, autoincrement=True)
    off_ven= db.Column(db.Integer(), db.ForeignKey('vendor.ven_id'))
    start_date= db.Column(db.Date())
    end_date= db.Column(db.Time())

    ven_info= db.relationship('Vendor', backref='ven_offdays')
