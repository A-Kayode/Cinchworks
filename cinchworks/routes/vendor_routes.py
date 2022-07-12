from datetime import datetime
from flask import render_template, make_response, redirect, session, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .. import app, db
from ..custom_functions import venvalidation, rewrite_duration
from ..models import Vendor, State, Services, Service_category, Vendor_services, Booking
from ..forms import Change_password


@app.route('/ven/home/')
@venvalidation
def vendor_home():
    vendid= session['vend_id']
    v= Vendor.query.get(vendid)
    return render_template('vendor/ven_home.html', v=v)


@app.route('/ven/bookings/')
@venvalidation
def vendor_bookings():
    vendid= session['vend_id']
    v= Vendor.query.get(vendid)
    pbook= Booking.query.filter(Booking.confirmation_status == "pending", Booking.b_vendor == vendid).all()
    abook= Booking.query.filter(Booking.confirmation_status == "active", Booking.b_vendor == vendid).all()
    return render_template('vendor/ven_booking.html', v=v, pbook=pbook, abook=abook)


@app.route('/ven/settings/')
@venvalidation
def ven_settings():
    vendid= session['vend_id']
    v= Vendor.query.get(vendid)
    s= State.query.all()
    cform= Change_password()
    cat= Service_category.query.all()
    ser= Services.query.all()
    venser= Vendor_services.query.filter(Vendor_services.vendor_id == vendid).all()
    return render_template('vendor/ven_settings.html', v=v, s=s, cform=cform, cat=cat, ser=ser, venser=venser)


@app.route('/ven/settings/editinfo', methods= ['POST'])
@venvalidation
def ven_edit_info():
    vendid= session['vend_id']
    v= Vendor.query.get(vendid)
    fname= request.form.get('fname')
    lname= request.form.get('lname')
    bname= request.form.get('bname')
    phone1= request.form.get('phone1')
    phone2= request.form.get('phone2')
    address= request.form.get('address')
    city= request.form.get('city')
    state= request.form.get('state')
    busdesc= request.form.get('busdesc')
    v.ven_fname= fname
    v.ven_lname= lname
    v.ven_phone1= phone1
    v.ven_phone2= phone2
    v.ven_address= address
    v.ven_city= city
    v.ven_state= state
    v.ven_busname= bname
    v.ven_shortdesc= busdesc
    db.session.commit()
    flash("Update Sucessful", 'success')
    return redirect('/ven/settings')


@app.route('/ven/settings/changepswd/', methods=['POST'])
@venvalidation
def ven_change_password():
    vendid= session['vend_id']
    v= Vendor.query.get(vendid)
    cform= Change_password()
    old_pass= request.form.get('opswd')
    if check_password_hash(v.ven_password, old_pass):
        if cform.validate_on_submit():
            new_pass= request.form.get('npswd')
            v.ven_password= generate_password_hash(new_pass)
            db.session.commit()
            flash("Password Changed Successfully", 'success')
            return redirect('/cus/settings')
        else:
            return render_template('vendor/ven_settings.html', v=v, cform=cform)
    else:
        flash('Password Change Unsuccessful', 'failure')
        return redirect('/ven/settings')


@app.route('/ven/settings/addservice/', methods=['POST'])
@venvalidation
def add_service():
    vendid= session['vend_id']
    category= request.form.get('category')
    service= request.form.get('service')

    if service == 'others':
        othservice = request.form.get('othservice')
        ser= Services(service_name=othservice, ser_category=category)
        db.session.add(ser)
        db.session.commit()
        service= ser.service_id

    shortdesc= request.form.get('shortdesc')
    longdesc= request.form.get('longdesc')
    price= request.form.get('price')
    avgdur= request.form.get('avgdur')
    avgtxt= rewrite_duration(*avgdur.split(':'))
    mindur= request.form.get('mindur')
    mintxt= rewrite_duration(*mindur.split(':'))
    maxdur= request.form.get('maxdur')
    maxtxt= rewrite_duration(*maxdur.split(':'))
    vs= Vendor_services(vendor_id=vendid, service_id=service, short_desc=shortdesc, long_desc=longdesc, service_price=price, average_duration=avgdur, min_duration=mindur, max_duration=maxdur, avgdur_text=avgtxt, mindur_text=mintxt, maxdur_text=maxtxt)
    db.session.add(vs)
    db.session.commit()
    flash("Service Added", "service")
    return redirect('/ven/settings#add_service')


@app.route('//ven/booking/confirmbooking/<int:bookid>/')
@venvalidation
def confirm_booking(bookid):
    bookrec= Booking.query.get(bookid)
    bookrec.confirmation_status= "active"
    db.session.commit()
    flash("Booking Confirmed")
    return redirect('/ven/bookings')


@app.route('/ven/bookinghistory/rejectbooking/<int:bookid>')
@venvalidation
def reject_booking(bookid):
    bookrec= Booking.query.get(bookid)
    bookrec.confirmation_status= "rejected"
    db.session.commit()
    flash("booking rejected")
    return redirect('/ven/bookings')