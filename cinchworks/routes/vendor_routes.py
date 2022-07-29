import os
import random
from datetime import datetime, date
from flask import render_template, make_response, redirect, session, request, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from .. import app, db
from ..custom_functions import venvalidation, rewrite_duration, convert_date
from ..models import *
from ..forms import Change_password


@app.route('/ven/home/')
@venvalidation
def vendor_home():
    vendid= session['vend_id']
    v= Vendor.query.get(vendid)
    vbdobj= db.session.execute(f"SELECT * FROM booking WHERE b_vendor = {vendid} and calender_date >= now() and confirmation_status = 'active' GROUP BY calender_date ORDER BY calender_date LIMIT 5")
    vbd= vbdobj.fetchall()
    vbst= Booking.query.filter(Booking.calender_date >= date.today(), Booking.b_vendor == vendid).order_by(Booking.calender_time).all()

    #make bookings for previous days expired
    exbk= Booking.query.filter(Booking.calender_date < date.today(), Booking.b_vendor == vendid).all()
    for i in exbk:
        i.confirmation_status = "expired"
    try:
        db.session.commit()
    except:
        db.session.rollback()
    
    #pending and active bookings on home page
    pbook= Booking.query.filter(Booking.confirmation_status == "pending", Booking.b_vendor == vendid).order_by(Booking.booking_date).limit(3).all()
    abook= Booking.query.filter(Booking.confirmation_status == "active", Booking.b_vendor == vendid).order_by(Booking.booking_date).limit(3).all()
    pcount= Booking.query.filter(Booking.confirmation_status == "pending", Booking.b_vendor == vendid).count()
    acount= Booking.query.filter(Booking.confirmation_status == "active", Booking.b_vendor == vendid).count()

    #calculating average rating
    revs= Reviews.query.filter(Reviews.r_vendor == vendid).all()
    
    if revs != []:
        total= 0
        for i in revs:
            total= total + i.review_score
        avgrat= f"{total/len(revs)}/10"
    else:
        avgrat= "No ratings yet"
    

    return render_template('vendor/ven_home.html', v=v, vbd=vbd, vbst=vbst, pbook=pbook, abook=abook, pcount=pcount, acount=acount, avgrat=avgrat)


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
    

@app.route('/ven/ajax/displaybooking/')
@venvalidation
def vendor_ajax_displaybooking():
    bookid= request.args.get('bookid')
    bk= Booking.query.get(bookid)
    if bk:
        cfname= bk.cus_info.cus_fname
        clname= bk.cus_info.cus_lname
        cph1= bk.cus_info.cus_phone1
        cph2= bk.cus_info.cus_phone2
        caddr= bk.cus_info.cus_address
        sname= bk.service_info.service.service_name
        sshort= bk.service_info.short_desc
        slong= bk.service_info.long_desc
        slocation= bk.service_location.name
        bdate= bk.calender_date.strftime("%a %b %d, %Y")
        btime= bk.calender_time.strftime("%H:%M")
        betime= bk.calender_endtime.strftime("%H:%M")
        bnotes= bk.notes
        ccity= bk.cus_info.cus_city
        if bk.cus_info.customer_lga.lga_name != None:
            clga= bk.cus_info.customer_lga.lga_name
        else:
            clga= ""
        if bk.cus_info.customer_state.state_name != None:
            cstate= bk.cus_info.customer_state.state_name
        else:
            cstate= ""

        return jsonify(status=1, cfname=cfname, clname=clname, cph1=cph1, cph2=cph2, caddr=caddr, sname=sname, sshort=sshort, slong=slong, slocation=slocation, bdate=bdate, btime=btime, betime=betime, bnotes=bnotes, ccity=ccity, clga=clga, cstate=cstate, message="Booking retrieved")
    else:
        return jsonify(status=0, message="Error, cannot retrieve booking")
    return jsonify(status=1, message="done")    

    





#Codes for vendor settings
@app.route('/ven/settings/')
@venvalidation
def ven_settings():
    vendid= session['vend_id']
    v= Vendor.query.get(vendid)
    s= State.query.all()
    cform= Change_password()
    cat= Service_category.query.all()
    ser= Services.query.all()
    venser= Vendor_services.query.filter(Vendor_services.vendor_id == vendid, Vendor_services.service_status != 'depreciated').all()
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
    workday= request.form.get('workdat')
    vs= Vendor_services(vendor_id=vendid, service_id=service, short_desc=shortdesc, long_desc=longdesc, service_price=price, average_duration=avgdur, min_duration=mindur, max_duration=maxdur, avgdur_text=avgtxt, mindur_text=mintxt, maxdur_text=maxtxt, service_status="active", workdays=workday)
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
        returntext= returntext + "<option value= ''>others</option>"

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


@app.route('/ven/ajax/deleteservice/', methods=['POST'])
@venvalidation
def ajax_vendor_deleteservice():
    venser_id = request.form.get('ven_service_id')
    vendid= request.form.get('vendid')
    booked= Booking.query.filter(Booking.b_venservice == venser_id, ((Booking.confirmation_status != 'pending') | (Booking.confirmation_status != 'rejected')) ).first()

    if booked:
        return jsonify(status=0, message="Service cannot be deleted because it has had at least one active booking. Depreciating the service is recommended.")
    else:
        venser= Vendor_services.query.get(venser_id)
        try:
            db.session.delete(venser)
            db.session.commit()

            vss= Vendor_services.query.filter(Vendor_services.vendor_id == vendid, Vendor_services.service_status != 'depreciated').all()
            services= ""
            counter= 0
            for i in vss:
                counter= counter + 1
                services= services + f"<tr><td>{counter}</td> <td>{i.service.service_name}</td> <td>{i.mindur_text}</td> <td>{i.avgdur_text}</td> <td>{i.maxdur_text}</td> <td>{i.service_price}</td> <td><button class= \"btn btn-sm btn-danger\" onclick= \"return delete_service({ i.ven_service_id }, { vendid });\">Delete</button> <button class= \"btn btn-sm btn-secondary\" onclick= \"return depreciate_service({ i.ven_service_id }, { vendid });\">Depreciate</button></td></tr>"

            return jsonify(status=1, message= "Service Deleted", nhtml=services)
        except:
            db.session.rollback()
            return jsonify(status=1, message="An error occured, service could not deleted.")


@app.route('/ven/ajax/depreciateservice/', methods=['POST', 'GET'])
@venvalidation
def vendor_ajax_depreciateservice():
    venser_id = request.form.get('ven_service_id')
    vendid= request.form.get('vendid')
    vss= Vendor_services.query.get(venser_id)
    try:
        vss.service_status= 'depreciated'
        db.session.commit()

        vss= Vendor_services.query.filter(Vendor_services.vendor_id == vendid, Vendor_services.service_status != 'depreciated').all()
        services= ""
        counter= 0
        for i in vss:
            counter= counter + 1
            services= services + f"<tr><td>{counter}</td> <td>{i.service.service_name}</td> <td>{i.mindur_text}</td> <td>{i.avgdur_text}</td> <td>{i.maxdur_text}</td> <td>{i.service_price}</td> <td><button class= \"btn btn-sm btn-danger\" onclick= \"return delete_service({ i.ven_service_id }, { vendid });\">Delete</button> <button class= \"btn btn-sm btn-secondary\" onclick= \"return depreciate_service({ i.ven_service_id }, { vendid });\">Depreciate</button></td></tr>"

        return jsonify(status=1, message="Service depreciated", nhtml=services)
    except:
        db.session.rollback()
        return jsonify(status=1, message="An error occured, service could not be depreciated.")


@app.route('/ven/ajax/addoffday/', methods=['POST'])
@venvalidation
def vendor_ajax_addoffday():
    s= request.form.get('sdate')
    e= request.form.get('edate')
    vendid= request.form.get('vendid')

    if s == "" or e == "":
        return jsonify(status=0, message="Please fill both start and end dates")
    else:
        sdate = convert_date(s)
        edate= convert_date(e)
        if sdate < date.today() or edate < date.today():
            return jsonify(status=0, message="You cannot backdate an offday")
        else:
            if edate < sdate:
                return jsonify(status=0, message="End date cannot be before start date")
            else:
                off= Offday(off_ven=vendid, start_date=sdate, end_date=edate)
                try:
                    db.session.add(off)
                    db.session.commit()
                    return jsonify(status=1, message="Offdays successfully set")
                except:
                    db.rollback()
                    return jsonify(status=0, message="An error occurred. Setting of offdays was unsucessful, please try again.")


@app.route('/ven/ajax/checkbusname/')
@venvalidation
def vendor_ajax_checkbusname():
    bname= request.args.get('bname')
    vendid= request.args.get('vendid')
    vb= Vendor.query.filter(Vendor.ven_busname == bname).count()

    if vb > 0:
        return jsonify(status=0, message="Business name already take")
    else:
        return jsonify(status=1, message="")








#codes for vendor booking
@app.route('/ven/bookings/')
@venvalidation
def vendor_bookings():
    vendid= session['vend_id']
    v= Vendor.query.get(vendid)
    pbook= Booking.query.filter(Booking.confirmation_status == "pending", Booking.b_vendor == vendid).all()
    abook= Booking.query.filter(Booking.confirmation_status == "active", Booking.b_vendor == vendid).all()
    hbook= Booking.query.filter(Booking.confirmation_status != "pending", Booking.confirmation_status != "active", Booking.b_vendor == vendid).order_by(Booking.booking_date).all()
    return render_template('vendor/ven_booking.html', v=v, pbook=pbook, abook=abook, hbook=hbook)


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