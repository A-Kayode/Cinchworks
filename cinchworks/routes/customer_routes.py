import os, random, math
from datetime import datetime, date
from flask import render_template, make_response, redirect, session, request, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from .. import app, db
from ..custom_functions import cusvalidation, calc_endtime, checkdate, convert_time, convert_date, venvalidation
from ..models import *
from ..forms import Change_password

@app.route('/cus/home/')
@cusvalidation
def customer_home():
    custid= session['cust_id']
    c= Customer.query.get(custid)
    bks= Booking.query.filter(Booking.b_customer == custid).order_by(Booking.booking_date).limit(5).all()
    cat= Service_category.query.all()
    ser= Services.query.all()
    cbdobj= db.session.execute(f"SELECT * FROM booking WHERE b_customer = {custid} and calender_date >= now() and confirmation_status = 'active' GROUP BY calender_date ORDER BY calender_date LIMIT 5")
    cbd= cbdobj.fetchall()
    cbst= Booking.query.filter(Booking.calender_date >= date.today(), Booking.b_customer == custid).order_by(Booking.calender_time).all()


    #This code will cater to what is needed for pagenation of the scheduler
    # allobj= db.session.execute(f"SELECT * FROM booking WHERE b_customer = {custid} and calender_date >= now() and confirmation_status = 'active' GROUP BY calender_date ORDER BY calender_date")
    # rec= allobj.fetchall()
    # allrec= len(rec)
    # totpage= math.ceil(allrec/5)
    # inipage= 1


    return render_template('customer/c_home.html', c=c, bks=bks, cat=cat, ser=ser, cbd=cbd, cbst=cbst)


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


@app.route('/cus/ajax/displaybooking/')
@cusvalidation
def customer_ajax_displaybooking():
    bookid= request.args.get('bookid')
    bk= Booking.query.get(bookid)
    if bk:
        vname= bk.ven_info.ven_busname
        vph1= bk.ven_info.ven_phone1
        vph2= bk.ven_info.ven_phone2
        vaddr= bk.ven_info.ven_address
        sname= bk.service_info.service.service_name
        sshort= bk.service_info.short_desc
        slong= bk.service_info.long_desc
        slocation= bk.service_location.name
        bdate= bk.calender_date.strftime("%a %b %d, %Y")
        btime= bk.calender_time.strftime("%H:%M")
        betime= bk.calender_endtime.strftime("%H:%M")
        bnotes= bk.notes
        vcity= bk.ven_info.ven_city
        if bk.ven_info.vendor_lga.lga_name != None:
            vlga= bk.ven_info.vendor_lga.lga_name
        else:
            vlga= ""
        if bk.ven_info.vendor_state.state_name != None:
            vstate= bk.ven_info.vendor_state.state_name
        else:
            vstate= ""

        return jsonify(status=1, vname=vname, vph1=vph1, vph2=vph2, vaddr=vaddr, sname=sname, sshort=sshort, slong=slong, slocation=slocation, bdate=bdate, btime=btime, betime=betime, bnotes=bnotes, vcity=vcity, vlga=vlga, vstate=vstate, message="Booking retrieved")
    else:
        return jsonify(status=0, message="Error, cannot retrieve booking")
    








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
    vs= Vendor_services.query.filter(Vendor_services.ven_info.has(Vendor.ven_id == vendid), Vendor_services.service_status != 'depreciated').all()
    voff= Offday.query.filter(Offday.off_ven == vendid, Offday.start_date >= date.today()).order_by(Offday.start_date).all()

    vbdobj= db.session.execute(f"SELECT * FROM booking WHERE b_vendor = {vendid} and calender_date >= now() and confirmation_status = 'active' GROUP BY calender_date ORDER BY calender_date LIMIT 5")
    vbd= vbdobj.fetchall()
    vbst= Booking.query.filter(Booking.calender_date >= date.today(), Booking.b_vendor == vendid).order_by(Booking.calender_time).all()
    venrev= Reviews.query.filter(Reviews.r_vendor == vendid).limit(4).all()

    
    #calculating vendor average rating
    #calculating average rating
    revs= Reviews.query.filter(Reviews.r_vendor == vendid).all()
    
    if revs != []:
        total= 0
        for i in revs:
            total= total + i.review_score
        avgrat= f"{total/len(revs)}/10"
    else:
        avgrat= "No ratings yet"

    
    if session.get('cust_id') != None:
        custid= session['cust_id']
        c= Customer.query.get(custid)
        cvrev= Reviews.query.filter(Reviews.r_customer == custid, Reviews.r_vendor == vendid).first()
        return render_template('customer/cus_vendor_page.html', c=c, v=v, vs=vs, vbd=vbd, vbst=vbst, voff=voff, cvrev=cvrev, venrev=venrev, avgrat=avgrat)
    else:
        return render_template('customer/cus_vendor_page.html', v=v, vs=vs, vbd=vbd, vbst=vbst, voff=voff, venrev=venrev, avgrat=avgrat)



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


@app.route('/cus/ajax/validatebookingdate/', methods=['POST', 'GET'])
@cusvalidation
def customer_ajax_validatebookingdate():
    bdate= request.form.get('bdater')
    vendid= request.form.get('vendid')
    if checkdate(bdate):
        vbdate= convert_date(bdate)
        offs= Offday.query.filter(Offday.off_ven == vendid).all()

        if offs != []:
            for i in offs:
                if vbdate >= i.start_date and vbdate <= i.end_date:
                    return jsonify(status=0, message="Cannot book this date, it has been set as an offday by the vendor")

        return jsonify(status=1, message="Date good")
    else:
        return jsonify(status=0, message="Date bad")


@app.route('/cus/ajax/validatebookingtime/', methods=['POST', 'GET'])
@cusvalidation
def customer_ajax_validatebookingtime():
    bdate= request.form.get('bdate')
    vendid= request.form.get('vendid')
    btime= request.form.get('btime')
    bduration= request.form.get('bduration')
    btimeobj= convert_time(btime)
    bentime= calc_endtime(btime, bduration)
    bentimeobj= convert_time(bentime)
    v= Vendor.query.get(vendid)
    vsb= Booking.query.filter(Booking.b_vendor == vendid, Booking.calender_date == bdate, Booking.confirmation_status == "active").all()

    if btimeobj < v.ven_openingtime:
        return jsonify(status=0, message="Vendor not open yet. Choose another time.")
    else:
        if btimeobj > v.ven_closingtime:
            return jsonify(status=0, message="Vendor closed. Choose another time")
        else:
            for i in vsb:
                if btimeobj >= i.calender_time and btimeobj < i.calender_endtime:
                    return jsonify(status=0, message="Time slot already booked. Check vendor schedule and choose another time")
            if bentimeobj > v.ven_closingtime:
                return jsonify(status=0, message="Invalid time. Service ends after vendor is closed. Check vendor schedule and choose another time.")
            

    return jsonify(status=1, message="done")


@app.route('/cus/ajax/addreview/', methods=['POST', 'GET'])
@cusvalidation
def customer_ajax_addreview():
    custid= request.form.get('custid')
    vendid= request.form.get('vendid')
    revscore= request.form.get('venrevscore')
    revtext= request.form.get('venrevtext')

    if revscore == "":
        return jsonify(status=0, message="Please select a score for the vendor.")
    else:
        if revtext == "":
            return jsonify(status=0, message="Please ensure you review the vendor before submitting")
        else:
            review= Reviews(r_customer=custid, r_vendor=vendid, review_score=revscore, review_desc=revtext)
            try:
                db.session.add(review)
                db.session.commit()
                return jsonify(status=1, message="Review submitted successfully")
            except:
                db.session.rollback()
                return jsonify(status=0, message="An error occured. Unable to submit review. Please try again later.")


@app.route('/cus/ajax/deletereview/')
@cusvalidation
def customer_ajax_deletereview():
    custid= request.args.get('custid')
    vendid= request.args.get('vendid')
    try:
        rev= Reviews.query.filter(Reviews.r_customer == custid, Reviews.r_vendor == vendid).first()
        db.session.delete(rev)
        db.session.commit()
        nhtml= f'<form id= "venreview"><h5>Write a review</h5><div class= "col-5 mb-2"><label>Score the Vendor</label><select id= "venrevscore" name= "venrevscore" class= "form-select"><option value= "">Select a Score</option><option value= "1">1</option><option value= "2">2</option><option value= "3">3</option><option value= "4">4</option><option value= "5">5</option><option value= "6">6</option><option value= "7">7</option><option value= "8">8</option><option value= "9">9</option><option value= "10">10</option></select></div><div class= "mb-2"><textarea class= "form-control" placeholder= "write your review here" name= "venrevtext" id= "venrevtext" style= "height: 10vh;"></textarea></div><div class= "text-end"><button class= "btn btn-primary" type= "button" onclick= "add_review({custid}, {vendid});">Submit</button></div></form><div class= "my-2" id= "revmessage"></div>'
        return jsonify(status=1, message="Review deleted successfully", nhtml=nhtml)
    except:
        db.session.rollback()
        return jsonify(status=0, message="An error occurred. Was unable to delete successfully. Please try again later.")


@app.route('/vendorreviews/<int:vendid>/')
def vendor_review(vendid):
    v= Vendor.query.get(vendid)
    venrev= Reviews.query.filter(Reviews.r_vendor == vendid).all()

    
    if session.get('cust_id') != None:
        custid= session['cust_id']
        c= Customer.query.get(custid)
        return render_template('general/vendor_reviews.html', c=c, v=v, venrev=venrev)
    elif session.get('vend_id') != None:
        return render_template('general/vendor_reviews.html', v=v, venrev=venrev)
    else:
        return render_template('general/vendor_reviews.html', v=v, venrev=venrev)


@app.route('/cus/ajax/getdate/')
def customer_ajax_getdate():
    vendid= request.args.get('vendid')
    bdate= request.args.get('bdate')
    
    if checkdate(bdate):
        vbdate= convert_date(bdate)
        offs= Offday.query.filter(Offday.off_ven == vendid).all()
        vb= Booking.query.filter(Booking.calender_date == bdate, Booking.b_vendor == vendid).order_by(Booking.calender_time).all()

        if offs != []:
            for i in offs:
                if vbdate >= i.start_date and vbdate <= i.end_date:
                    return jsonify(status=0, message="Cannot book this date, it has been set as an offday by the vendor")
        
        if vb != []:
            nhtml= ""
            for i in vb:
                stime= i.calender_time.strftime("%H:%M")
                etime= i.calender_endtime.strftime("%H:%M")
                nhtml= f'<div class= "mb-2 ps-3" style= "background-color: rgba(0,0,0,0.04);">{stime} - {etime}<p><b></b></p><p>Booked</p></div>'
            
            return jsonify(status=1, nhtml=nhtml)

        else:
            return jsonify(status=0, message="There are no bookings on this day")


    else:
        return jsonify(status=0, message="Your cannot search for bookings on past dates.")







#This contains code for what happens on the customer booking history page
@app.route('/cus/bookinghistory')
@cusvalidation
def customer_bookinghistory():
    custid= session['cust_id']
    c= Customer.query.get(custid)
    pbook= Booking.query.filter(Booking.confirmation_status == "pending", Booking.b_customer == custid).all()
    abook= Booking.query.filter(Booking.confirmation_status == "active", Booking.b_customer == custid).all()
    rcbook= Booking.query.filter(Booking.confirmation_status != "active", Booking.confirmation_status != "pending", Booking.b_customer == custid).all()
    cat= Service_category.query.all()
    ser= Services.query.all()
    return render_template('customer/cus_booking_history.html', c=c, pbook=pbook, rcbook=rcbook, cat=cat, ser=ser, abook=abook)


@app.route('/cus/bookinghistory/deleterejected/<int:bookid>/')
@cusvalidation
def delete_rejected(bookid):
    book= Booking.query.get(bookid)
    db.session.delete(book)
    db.session.commit()
    flash("Booking Deleted")
    return redirect('/cus/bookinghistory')


@app.route('/cus/bookinghistory/cancelpending/<int:bookid>/')
@cusvalidation
def cancel_pending(bookid):
    book= Booking.query.get(bookid)
    db.session.delete(book)
    db.session.commit()
    flash("Booking Cancelled")
    return redirect('/cus/bookinghistory')