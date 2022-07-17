import os
import random
from datetime import datetime
from flask import render_template, make_response, redirect, session, request, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from .. import app, db
from ..custom_functions import venvalidation, rewrite_duration
from ..models import *
from ..forms import Change_password


@app.route('/ven/home/')
@venvalidation
def vendor_home():
    vendid= session['vend_id']
    v= Vendor.query.get(vendid)
    return render_template('vendor/ven_home.html', v=v)


@app.route('/ven/ajax/changepicture/', methods=['POST', 'GET'])
@venvalidation
def vendor_ajax_changepicture():
    bannerpic= request.files.get('bannerpic')
    profilepic= request.files.get('profilepic')
    
    if bannerpic != None:
        banpicname= bannerpic.filename
        tt, ext= os.path.splitext(banpicname)
        banpictest= "1" + ext
        bannerpic.save(f"cinchworks/static/uploads/images/{banpictest}")
    
    if profilepic != None:
        propicname= profilepic.filename
        hh, ext2= os.path.splitext(propicname)
        propictest= "2" + ext2
        profilepic.save(f"cinchworks/static/uploads/images/{propictest}")
    
    if bannerpic != None and profilepic != None:
        return jsonify(banner=banpictest, profile=propictest)
    elif bannerpic != None and profilepic == None:
        return jsonify(banner=banpictest)
    elif bannerpic == None and profilepic != None:
        return jsonify(profile=propictest)


@app.route('/ven/ajax/savepicture/', methods=['POST', 'GET'])
@venvalidation
def vendor_ajax_savepicture():
    bannerpic= request.files.get('bannerpic')
    profilepic= request.files.get('profilepic')
    vendid= request.form.get('vendid')
    vp= Vendor.query.get(vendid)
    
    if bannerpic.filename != "":
        banpicname= bannerpic.filename
        t, ext= os.path.splitext(banpicname)
        nn= random.random() * 10000000000000000
        banpicname= str(nn) + ext
        bannerpic.save(f"cinchworks/static/uploads/images/{banpicname}")
        vp.ven_bannerpic= banpicname
    
    if profilepic.filename != "":
        propicname= profilepic.filename
        r, ext2= os.path.splitext(propicname)
        hh= random.random() * 10000000000000000
        propicname= str(hh) + ext2
        profilepic.save(f"cinchworks/static/uploads/images/{propicname}")
        vp.ven_profilepic= propicname
    
    db.session.commit()
    
    if bannerpic != None and profilepic != None:
        return jsonify(banner=banpicname, profile=propicname)
    elif bannerpic != None and profilepic == None:
        return jsonify(banner=banpicname, profile="")
    elif bannerpic == None and profilepic != None:
        return jsonify(profile=propicname, banner="")
    
    

    





#Codes for vendor service
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
    lga= request.form.get('lga')
    busdesc= request.form.get('busdesc')
    v.ven_fname= fname
    v.ven_lname= lname
    v.ven_phone1= phone1
    v.ven_phone2= phone2
    v.ven_address= address
    v.ven_city= city
    v.ven_state= state
    v.ven_lga= lga
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


@app.route('/ven/ajax/chooseservice/', methods=['POST'])
@venvalidation
def ajax_vendor_chooseservice():
    catid= request.form.get('categoryid')
    catser= Services.query.filter(Services.ser_category == catid).all()

    returntext= "<option value= ''>Select Service</option>"
    for i in catser:
        returntext= returntext + f"<option value= '{i.service_id}'>{i.service_name}</option>"
    else:
        returntext= returntext + "<option value= 'others'>others</option>"

    return returntext


@app.route('/ven/ajax/selectlga/', methods= ['POST'])
@venvalidation
def ajax_vendor_selectlga():
    stateid= request.form.get('stateid')
    statelga= Lga.query.filter(Lga.state_id == stateid).all()

    returntext= "<option value= ''>Select LGA</option>"
    for i in statelga:
        returntext= returntext + f"<option value= '{i.lga_id}'>{i.lga_name}</option>"

    return returntext




#codes for vendor booking
@app.route('/ven/bookings/')
@venvalidation
def vendor_bookings():
    vendid= session['vend_id']
    v= Vendor.query.get(vendid)
    pbook= Booking.query.filter(Booking.confirmation_status == "pending", Booking.b_vendor == vendid).all()
    abook= Booking.query.filter(Booking.confirmation_status == "active", Booking.b_vendor == vendid).all()
    return render_template('vendor/ven_booking.html', v=v, pbook=pbook, abook=abook)


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