import os, random
from datetime import datetime
from flask import render_template, make_response, redirect, session, request, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from .. import app, db
from ..custom_functions import cusvalidation, calc_endtime
from ..models import Customer, State, Vendor, Vendor_services, Booking, Services, Lga, Service_category
from ..forms import Change_password

@app.route('/cus/home/')
@cusvalidation
def customer_home():
    custid= session['cust_id']
    c= Customer.query.get(custid)
    bks= Booking.query.order_by(Booking.booking_date.desc()).all()
    cat= Service_category.query.all()
    ser= Services.query.all()
    return render_template('customer/c_home.html', c=c, bks=bks, cat=cat, ser=ser)


@app.route('/cus/ajax/changepicture/', methods=['POST', 'GET'])
@cusvalidation
def customer_ajax_changepicture():
    profilepic= request.files.get('profilepic')
    if profilepic != None:
        propicname= profilepic.filename
        hh, ext2= os.path.splitext(propicname)
        propictest= "3" + ext2
        profilepic.save(f"cinchworks/static/uploads/images/{propictest}")
    
    if profilepic != None:
        return jsonify(profile=propictest)
    else:
        return jsonify(profile="")


@app.route('/cus/ajax/savepicture/', methods=['POST', 'GET'])
@cusvalidation
def customer_ajax_savepicture():
    profilepic= request.files.get('profilepic')
    custid= request.form.get('custid')
    cp= Customer.query.get(custid)
     
    if profilepic.filename != "":
        propicname= profilepic.filename
        r, ext2= os.path.splitext(propicname)
        hh= random.random() * 10000000000000000
        propicname= str(hh) + ext2
        profilepic.save(f"cinchworks/static/uploads/images/{propicname}")
        cp.cus_profilepic= propicname
    
    db.session.commit()
    if profilepic != None:
        return jsonify(profile=propicname)
    else:
        return jsonify(profile="")
    








#This contains code for all that happen on the customer setting page
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
    lga= request.form.get('lga')
    c.cus_fname= fname
    c.cus_lname= lname
    c.cus_phone1= phone1
    c.cus_phone2= phone2
    c.cus_address= address
    c.cus_city= city
    c.cus_state= state
    c.cus_lga= lga
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


@app.route('/cus/ajax/selectlga/', methods= ['POST'])
@cusvalidation
def ajax_customer_selectlga():
    stateid= request.form.get('stateid')
    statelga= Lga.query.filter(Lga.state_id == stateid).all()

    returntext= "<option value= ''>Select LGA</option>"
    for i in statelga:
        returntext= returntext + f"<option value= '{i.lga_id}'>{i.lga_name}</option>"

    return returntext




#This contains code for things that happen on the customer-vendor page
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


@app.route('/cus/ajax/chooseduration/', methods=['POST'])
@cusvalidation
def ajax_chooseduration():
    bservice= request.form.get('bservice')
    vendid= request.form.get('vendid')
    vss= Vendor_services.query.filter(Vendor_services.ven_service_id == bservice).first()
    
    duration= f"<option value= '{vss.min_duration}'>Minimum Duration</option><option value= '{vss.average_duration}'>Average Duration</option><option value= '{vss.max_duration}'>Maximum Duration</option>"

    return duration




#This contains code for what happens on the customer booking history page
@app.route('/cus/bookinghistory')
@cusvalidation
def customer_bookinghistory():
    custid= session['cust_id']
    c= Customer.query.get(custid)
    pbook= Booking.query.filter(Booking.confirmation_status == "pending", Booking.b_customer == custid).all()
    rcbook= Booking.query.filter(Booking.confirmation_status != "active", Booking.confirmation_status != "pending", Booking.b_customer == custid).all()
    cat= Service_category.query.all()
    ser= Services.query.all()
    return render_template('customer/cus_booking_history.html', c=c, pbook=pbook, rcbook=rcbook, cat=cat, ser=ser)


@app.route('/cus/bookinghistory/deleterejected/<int:bookid>/')
@cusvalidation
def delete_rejected(bookid):
    book= Booking.query.get(bookid)
    db.session.delete(book)
    db.session.commit()
    flash("Booking Deleted")
    return redirect('/cus/bookinghistory')