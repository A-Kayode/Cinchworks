from datetime import datetime
from flask import render_template, make_response, redirect, session, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .. import app, db
from ..custom_functions import cusvalidation, calc_endtime
from ..models import Customer, State, Vendor, Vendor_services, Booking
from ..forms import Change_password

@app.route('/cus/home/')
@cusvalidation
def customer_home():
    custid= session['cust_id']
    c= Customer.query.get(custid)
    return render_template('customer/c_home.html', c=c)


@app.route('/cus/bookinghistory')
@cusvalidation
def customer_bookinghistory():
    custid= session['cust_id']
    c= Customer.query.get(custid)
    pbook= Booking.query.filter(Booking.confirmation_status == "pending", Booking.b_customer == custid).all()
    return render_template('customer/cus_booking_history.html', c=c, pbook=pbook)


@app.route('/cus/settings')
@cusvalidation
def customer_settings():
    custid= session['cust_id']
    c= Customer.query.get(custid)
    s= State.query.all()
    cform= Change_password()
    return render_template('customer/cus_settings.html', c=c, s=s, cform=cform)


@app.route('/cus/settings/editinfo', methods= ['POST'])
@cusvalidation
def cus_edit_info():
    custid= session['cust_id']
    c= Customer.query.get(custid)
    fname= request.form.get('fname')
    lname= request.form.get('lname')
    phone1= request.form.get('phone1')
    phone2= request.form.get('phone2')
    address= request.form.get('address')
    city= request.form.get('city')
    state= request.form.get('state')
    c.cus_fname= fname
    c.cus_lname= lname
    c.cus_phone1= phone1
    c.cus_phone2= phone2
    c.cus_address= address
    c.cus_city= city
    c.cus_state= state
    db.session.commit()
    flash("Update Sucessful", 'success')
    return redirect('/cus/settings')


@app.route('/cus/settings/changepswd', methods=['POST'])
@cusvalidation
def cus_change_password():
    custid= session['cust_id']
    cform= Change_password()
    c= Customer.query.get(custid)
    old_pass= request.form.get('opswd')
    if check_password_hash(c.cus_password, old_pass):
        if cform.validate_on_submit():
            new_pass= request.form.get('npswd')
            c.cus_password= generate_password_hash(new_pass)
            db.session.commit()
            flash("Password Changed Successfully", 'success')
            return redirect('/cus/settings')
        else:
            return render_template('customer/cus_settings.html', c=c, cform=cform)
    else:
        flash('Password Change Unsuccessful', 'failure')
        return redirect('/cus/settings')


@app.route('/cus/vendorpage/<vendid>')
def vendor_page(vendid):
    v= Vendor.query.get(vendid)
    vs= Vendor_services.query.filter(Vendor_services.ven_info.has(Vendor.ven_id == vendid)).all()
    
    if session.get('cust_id') != None:
        custid= session['cust_id']
        c= Customer.query.get(custid)
        return render_template('customer/cus_vendor_page.html', c=c, v=v, vs=vs)
    else:
        return render_template('customer/cus_vendor_page.html', v=v, vs=vs)



@app.route('/cus/bookvendor/<int:vendid>', methods=['POST'])
@cusvalidation
def book_vendor(vendid):
    custid= session['cust_id']
    bservice= request.form.get('bservice')
    bdate= request.form.get('bdate')
    blocation= request.form.get('blocation')
    bcstime= request.form.get('btime')
    duration= request.form.get('duration')
    notes= request.form.get('notes')
    bcetime= calc_endtime(bcstime, duration)

    book= Booking(b_vendor=vendid, b_customer=custid, b_venservice=bservice, service_location=blocation, confirmation_status="pending", calender_date=bdate, calender_time=bcstime, calender_endtime=bcetime, notes=notes)
    db.session.add(book)
    db.session.commit()
    return redirect('/cus/bookinghistory')
