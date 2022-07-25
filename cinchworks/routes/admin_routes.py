from json import JSONEncoder
from unicodedata import category
from xml.dom import ValidationErr
from flask import render_template, redirect, request, session, flash, jsonify
from werkzeug.security import check_password_hash
from .. import app, db
from ..models import Admin, Customer, Services, Vendor, Booking, Vendor_services, Service_category
from ..custom_functions import adminvalidation


@app.route('/admin/login/', methods=['POST', 'GET'])
def admin_login():
    if request.method == 'GET':
        return render_template('admin/admin_login.html')
    else:
        email= request.form.get('email')
        pswd= request.form.get('pswd')
        a= Admin.query.filter(Admin.admin_email == email).first()
        if a != None:
            if check_password_hash(a.admin_password,pswd):
                session['admin_id']= a.admin_id
                return redirect('/admin')
            else:
                flash("Invalid credentials")
                return redirect('/admin/login/')
        else:
            flash("Invalid credentials")
            return redirect('/admin/login/')



@app.route('/adminori/')
@adminvalidation
def admin_ori():
    return render_template("admin/admin_page.html")


@app.route('/admin/')
@adminvalidation
def admin_dashboard():
    adid= session.get('admin_id')
    a= Admin.query.get(adid)
    tc= Customer.query.count()
    ac= Customer.query.filter(Customer.cus_status == "active").count()
    sc= Customer.query.filter(Customer.cus_status == "suspended").count()
    tv= Vendor.query.count()
    av= Vendor.query.filter(Vendor.ven_status == "active").count()
    sv= Vendor.query.filter(Vendor.ven_status == "suspended").count()
    tb= Booking.query.count()
    pb= Booking.query.filter(Booking.confirmation_status == "pending").count()
    ab= Booking.query.filter(Booking.confirmation_status == "active").count()
    cb= Booking.query.filter(Booking.confirmation_status == "cancelled").count()
    eb= Booking.query.filter(Booking.confirmation_status == "expired").count()
    return render_template("admin/admin_home.html", a=a, tc=tc, ac=ac, sc=sc, tv=tv, av=av, sv=sv, tb=tb, pb=pb, ab=ab, cb=cb, eb=eb)


@app.route('/admin/logout/')
def admin_logout():
    session.pop('admin_id')
    return redirect('/admin/login')





#This deals with things concerning customer in the admin
@app.route('/admin/customers/')
@adminvalidation
def admin_manage_customers():
    adid= session.get('admin_id')
    a= Admin.query.get(adid)
    c= Customer.query.all()
    return render_template('admin/admin_customer.html', a=a, c=c)


@app.route('/admin/ajax/getcusinfo/')
@adminvalidation
def admin_ajax_getcustomerinfo():
    custid= request.args.get('custid')
    c= Customer.query.filter(Customer.cus_id == custid).first()
    cbook= Booking.query.filter(Booking.b_customer == custid).all()

    fname= c.cus_fname
    lname= c.cus_lname
    phone1= c.cus_phone1
    phone2= c.cus_phone2
    email= c.cus_email
    address= c.cus_address
    city= c.cus_city
    lga= c.customer_lga.lga_name
    state= c.customer_state.state_name
    username= c.cus_username
    regis= c.cus_regdate

    if cbook != []:
        nhtml= ""
        counter= 0
        for i in cbook:
            counter= counter + 1
            nhtml= nhtml + f'<tr class= "user_booking_table" onclick="admin_getcusbookinfo({i.booking_id})"><td>{counter}</td><td class= "hidesm">{i.booking_id}</td><td>{i.ven_info.ven_busname}</td><td>{i.service_info.service.service_name}</td><td class= "hidesm">{i.booking_date}</td></tr>'
        
        return jsonify(status=1, nhtml=nhtml, fname=fname, lname=lname, phone1=phone1, phone2=phone2, email=email, address=address, city=city, lga=lga, state=state, username=username, regis=regis, custid=custid)
    else:
        return jsonify(status=2, message="No booking information", fname=fname, lname=lname, phone1=phone1, phone2=phone2, email=email, address=address, city=city, lga=lga, state=state, username=username, regis=regis, custid=custid)


@app.route('/admin/ajax/getbookcusinfo/')
@adminvalidation
def admin_ajax_getcustomerbookinginfo():
    bkid= request.args.get('bookid')
    b= Booking.query.get(bkid)

    fname= b.ven_info.ven_fname
    lname= b.ven_info.ven_lname
    busname= b.ven_info.ven_busname
    service= b.service_info.service.service_name
    bookdate= b.booking_date
    datebook= b.calender_date
    tbook= b.calender_time.strftime('%H:%M')
    tebook= b.calender_endtime.strftime('%H:%M')
    location= b.service_location.name
    status= b.confirmation_status.name
    sdesc= b.service_info.short_desc
    ldesc= b.service_info.long_desc

    return jsonify(fname=fname, lname=lname, busname=busname, service=service, bookdate=bookdate, datebook=datebook, tbook=tbook, tebook=tebook, location=location, status=status, bkid=bkid, sdesc=sdesc, ldesc=ldesc)


@app.route('/admin/ajax/customersearch/')
@adminvalidation
def admin_ajax_customersearch():
    valu= request.args.get('custosearch')
    cs= Customer.query.filter((Customer.cus_username.like(f'%{valu}%')) | (Customer.cus_fname.like(f'%{valu}%')) | (Customer.cus_lname.like(f'%{valu}%')) | (Customer.cus_id == valu) | (Customer.cus_status == valu)).all()

    if cs != []:
        nhtml= ""
        counter= 0
        for i in cs:
            counter = counter + 1
            nhtml= nhtml + f'<tr class= "user_table" onclick= "admin_getcusinfo({i.cus_id})"><td>{counter}</td><td class= "hidesm">{i.cus_id}</td><td class= "hidesm">{i.cus_fname}</td><td class= "hidesm">{i.cus_lname}</td><td>{i.cus_username}</td><td>{i.cus_status.name}</td></tr>'
        
        return jsonify(status=1, nhtml=nhtml)
    else:
        return jsonify(status=0, message="No customer matches search parameter", val=valu)


@app.route('/admin/ajax/customerbooksearch/')
@adminvalidation
def admin_ajax_customerbooksearch():
    val= request.args.get('cusbooksearch')
    custid= request.args.get('custid')
    bs= Booking.query.filter(Booking.b_customer == custid, ((Booking.ven_info.has(Vendor.ven_busname.like(f'%{val}%'))) | (Booking.service_info.has(Vendor_services.service.has(Services.service_name.like(f'%{val}%')))) | (Booking.booking_id == val))).all()

    if bs != []:
        nhtml= ""
        counter= 0
        for i in bs:
            counter= counter + 1
            nhtml= nhtml + f'<tr class= "user_booking_table" onclick="admin_getcusbookinfo({i.booking_id})"><td>{counter}</td><td class= "hidesm">{i.booking_id}</td><td>{i.ven_info.ven_busname}</td><td>{i.service_info.service.service_name}</td><td class= "hidesm">{i.booking_date}</td></tr>'
        
        return jsonify(status=1, nhtml=nhtml)
    else:
        return jsonify(status=0, message="No booking matches search parameter", val=val)  







#This deals with things concerning vendors in the admin
@app.route('/admin/vendors/')
@adminvalidation
def admin_manage_vendors():
    adid= session.get('admin_id')
    a= Admin.query.get(adid)
    v= Vendor.query.all()
    return render_template('admin/admin_vendor.html', a=a, v=v)


@app.route('/admin/ajax/getveninfo/')
@adminvalidation
def admin_ajax_getveninfo():
    vendid= request.args.get('vendid')
    v= Vendor.query.filter(Vendor.ven_id == vendid).first()
    cbook= Booking.query.filter(Booking.b_customer == vendid).all()

    fname= v.ven_fname
    lname= v.ven_lname
    busname= v.ven_busname
    phone1= v.ven_phone1
    phone2= v.ven_phone2
    email= v.ven_email
    address= v.ven_address
    city= v.ven_city
    if v.ven_lga == None:
        lga= ""
    else:
        lga= v.vendor_lga.lga_name
    if v.ven_state == None:
        state= ""
    else:
        state= v.vendor_state.state_name
    username= v.ven_username
    regis= v.ven_regdate

    if cbook != []:
        nhtml= ""
        counter= 0
        for i in cbook:
            counter= counter + 1
            nhtml= nhtml + f'<tr class= "user_booking_table" onclick="admin_getvenbookinfo({i.booking_id})"><td>{counter}</td><td>{i.booking_id}</td><td>{i.cus_info.cus_fname} {i.cus_info.cus_lname}</td><td>{i.service_info.service.service_name}</td><td class= "hidesm">{i.booking_date}</td></tr>'
        
        return jsonify(status=1, nhtml=nhtml, fname=fname, lname=lname, phone1=phone1, phone2=phone2, email=email, address=address, city=city, lga=lga, state=state, username=username, regis=regis, vendid=vendid, busname=busname)
    else:
        return jsonify(status=2, message="No booking information", fname=fname, lname=lname, phone1=phone1, phone2=phone2, email=email, address=address, city=city, lga=lga, state=state, username=username, regis=regis, vendid=vendid, busname=busname)


@app.route('/admin/ajax/getbookveninfo/')
@adminvalidation
def admin_ajax_getvendorbookinginfo():
    bkid= request.args.get('bookid')
    b= Booking.query.get(bkid)

    fname= b.cus_info.cus_fname
    lname= b.cus_info.cus_lname
    service= b.service_info.service.service_name
    bookdate= b.booking_date
    datebook= b.calender_date
    tbook= b.calender_time.strftime('%H:%M')
    tebook= b.calender_endtime.strftime('%H:%M')
    location= b.service_location.name
    status= b.confirmation_status.name
    sdesc= b.service_info.short_desc
    ldesc= b.service_info.long_desc


    return jsonify(fname=fname, lname=lname, service=service, bookdate=bookdate, datebook=datebook, tbook=tbook, tebook=tebook, location=location, status=status, bkid=bkid, sdesc=sdesc, ldesc=ldesc)


@app.route('/admin/ajax/vendorsearch/')
@adminvalidation
def admin_ajax_vendorsearch():
    valu= request.args.get('ventosearch')
    vs= Vendor.query.filter((Vendor.ven_username.like(f'%{valu}%')) | (Vendor.ven_fname.like(f'%{valu}%')) | (Vendor.ven_lname.like(f'%{valu}%')) | (Vendor.ven_id == valu) | (Vendor.ven_status == valu)).all()

    if vs != []:
        nhtml= ""
        counter= 0
        for i in vs:
            counter = counter + 1
            nhtml= nhtml + f'<tr class= "user_table" onclick= "admin_getveninfo({i.ven_id}); admin_getvenservices({i.ven_id});"><td>{counter}</td><td class= "hidesm">{i.ven_id}</td><td class= "hidesm">{i.ven_fname} {i.ven_lname}</td><td class= "hidesm">{i.ven_busname}</td><td>{i.ven_username}</td><td>{i.ven_status.name}</td></tr>'
        
        return jsonify(status=1, nhtml=nhtml)
    else:
        return jsonify(status=0, message="No customer matches search parameter", val=valu)


@app.route('/admin/ajax/vendorbooksearch/')
@adminvalidation
def admin_ajax_vendorbooksearch():
    val= request.args.get('venbooksearch')
    vendid= request.args.get('vendid')
    bs= Booking.query.filter(Booking.b_vendor == vendid, ((Booking.cus_info.has(Customer.cus_fname.like(f'%{val}%'))) | (Booking.cus_info.has(Customer.cus_lname.like(f'%{val}%'))) | (Booking.service_info.has(Vendor_services.service.has(Services.service_name.like(f'%{val}%')))) | (Booking.booking_id == val))).all()

    if bs != []:
        nhtml= ""
        counter= 0
        for i in bs:
            counter= counter + 1
            nhtml= nhtml + f'<tr class= "user_booking_table" onclick="admin_getvenbookinfo({i.booking_id})"><td>{counter}</td><td>{i.booking_id}</td><td>{i.cus_info.cus_fname} {i.cus_info.cus_lname}</td><td>{i.service_info.service.service_name}</td><td class= "hidesm">{i.booking_date}</td></tr>'
        
        return jsonify(status=1, nhtml=nhtml)
    else:
        return jsonify(status=0, message="No booking matches search parameter", val=val)  


@app.route('/admin/ajax/getvenservices/')
@adminvalidation
def admin_ajax_getvendorservices():
    vendid= request.args.get('vendid')
    vser= Vendor_services.query.filter(Vendor_services.vendor_id == vendid).all()

    if vser != []:
        nhtml= ""
        counter= 0
        for i in vser:
            counter = counter + 1
            price= '{:,.2f}'.format(i.service_price)
            nhtml= nhtml + f'<tr class= "user_booking_table" onclick="admin_getvenserviceinfo({i.ven_service_id})"><td>{counter}</td><td>{i.service.service_name}</td><td>{i.service.category.category_name}</td><td>{price}</td></tr>'
        
        return jsonify(status=1, nhtml=nhtml)
    else:
        return jsonify(status=0, message="Vendor has no services")


@app.route('/admin/ajax/getvenserviceinfo/')
@adminvalidation
def admin_ajax_getvendorserviceinfo():
    vensevid= request.args.get('vensevid')
    vs= Vendor_services.query.get(vensevid)

    service= vs.service.service_name
    price= '{:,.2f}'.format(vs.service_price)
    avsmin= vs.mindur_text
    avsavg= vs.avgdur_text
    avsmax= vs.maxdur_text
    work= vs.workdays
    sstatus= vs.service_status
    sdesc= vs.short_desc
    ldesc= vs.long_desc

    return jsonify(status=1, serid=vensevid, service=service, price=price, avsmin=avsmin, avsavg=avsavg, avsmax=avsmax, work=work, sstatus=sstatus, sdesc=sdesc, ldesc=ldesc)


@app.route('/admin/ajax/cussuspendaccount/', methods=['POST', 'GET'])
@adminvalidation
def admin_ajax_cussuspendaccount():
    custid= request.form.get('custid')
    c= Customer.query.get(custid)

    if c != None:
        c.cus_status= "suspended"
        db.session.commit()
        return jsonify(status=1, message="Account suspended")
    else:
        return jsonify(status=0, message="Suspension unsuccessful")


@app.route('/admin/ajax/cusreactivateaccount/', methods=['POST', 'GET'])
@adminvalidation
def admin_ajax_cusreactivateaccount():
    custid= request.form.get('custid')
    c= Customer.query.get(custid)

    if c != None:
        c.cus_status= "active"
        db.session.commit()
        return jsonify(status=1, message="Account Reactivated")
    else:
        return jsonify(status=0, message="Reactivation unsuccessful")


@app.route('/admin/ajax/vensuspendaccount/', methods=['POST', 'GET'])
@adminvalidation
def admin_ajax_vensuspendaccount():
    vendid= request.form.get('vendid')
    v= Vendor.query.get(vendid)

    if v != None:
        v.ven_status= "suspended"
        db.session.commit()
        return jsonify(status=1, message="Account suspended")
    else:
        return jsonify(status=0, message="Suspension unsuccessful")


@app.route('/admin/ajax/venreactivateaccount/', methods=['POST', 'GET'])
@adminvalidation
def admin_ajax_venreactivateaccount():
    vendid= request.form.get('vendid')
    v= Vendor.query.get(vendid)

    if v != None:
        v.ven_status= "active"
        db.session.commit()
        return jsonify(status=1, message="Account Reactivated")
    else:
        return jsonify(status=0, message="Reactivation unsuccessful")






#admin services page area
@app.route('/admin/services/')
@adminvalidation
def admin_services():
    adid= session.get('admin_id')
    a= Admin.query.get(adid)
    cat= Service_category.query.all()
    ser= Services.query.all()

    return render_template('admin/admin_service.html', a=a, cat=cat, ser=ser)


@app.route('/admin/ajax/addcategory/', methods=['POST'])
@adminvalidation
def admin_ajax_addcategory():
    cater= request.form.get('cater')
    if cater != "":
        cr= Service_category(category_name=cater)
        db.session.add(cr)
        db.session.commit()

        ncr= Service_category.query.all()
        nhtml= ""
        nhtml2= '<option value= "">Select Category</option>'
        counter= 0
        for i in ncr:
            counter= counter + 1
            nhtml= nhtml + f'<tr><td>{ counter }</td><td>{ i.category_id }</td><td>{ i.category_name }</td></tr>'

            nhtml2= nhtml2 + f'<option value= "{i.category_id}">{i.category_name}</option>'
        
        return jsonify(status=1, message="Category successfully added", nhtml=nhtml, nhtml2=nhtml2)

    else:
        return jsonify(status=0, message="Please fill the input field.")


@app.route('/admin/ajax/addservice/', methods=['POST', 'GET'])
@adminvalidation
def admin_ajax_addservice():
    cat= request.form.get('catselect')
    sev= request.form.get('sever')
    
    if cat != "" and sev != "":
        cvs= Services(service_name=sev, ser_category=cat)
        db.session.add(cvs)
        db.session.commit()

        rcn= Services.query.all()
        nhtml= ""
        counter= 0
        for i in rcn:
            counter= counter + 1
            nhtml= nhtml + f'<tr><td>{ counter }</td><td>{ i.service_id }</td><td>{ i.service_name }</td><td>{ i.category.category_name }</td></tr>'

        return jsonify(status=1, message="Service Added Succesfully", nhtml=nhtml)
    else:
        return jsonify(status=0, message="Please fill all the fields before adding service")






#admin booking section
@app.route('/admin/bookings/')
@adminvalidation
def admin_booking():
    adid= session.get('admin_id')
    a= Admin.query.get(adid)
    book= Booking.query.all()
    return render_template('admin/admin_booking.html', book=book, a=a)


@app.route('/admin/ajax/showbookinginfo/')
@adminvalidation
def admin_ajax_showbookinginfo():
    bookid= request.args.get('bookid')
    bk= Booking.query.get(bookid)
    if bk != None:
        vendor= bk.ven_info.ven_busname
        cusfname= bk.cus_info.cus_fname
        cuslname= bk.cus_info.cus_lname
        service= bk.service_info.service.service_name
        slocation= bk.service_location.name
        dobook= bk.booking_date
        bdate= bk.calender_date.strftime('%a %B %d, %Y')
        tbook= bk.calender_time.strftime('%H:%M')
        tebook= bk.calender_endtime.strftime('%H:%M')
        bstatus= bk.confirmation_status.name
        sshort= bk.service_info.short_desc
        slong= bk.service_info.long_desc

        return jsonify(status=1, message="Retrieval successful", vendor=vendor, cusfname=cusfname, cuslname=cuslname, service=service, slocation=slocation, dobook=dobook, bdate=bdate, tbook=tbook, tebook=tebook, bstatus=bstatus, sshort=sshort, slong=slong, bookid=bookid)
    else:
        return jsonify(status=0, message="Unable to retrieve boobstatus=bstatus, king information")


@app.route('/admin/ajax/adminbookingsearch/')
@adminvalidation
def admin_ajax_bookingsearch():
    val= request.args.get('sbook')
    bk= Booking.query.filter((Booking.booking_id == val) | (Booking.cus_info.has(Customer.cus_fname.like(f'%{val}%'))) | (Booking.cus_info.has(Customer.cus_lname.like(f'%{val}%'))) | (Booking.ven_info.has(Vendor.ven_busname.like(f'%{val}%'))) | (Booking.calender_date == val) | (Booking.confirmation_status == val) | (Booking.service_info.has(Vendor_services.service.has(Services.service_name == val))))

    if bk != []:
        nhtml= ""
        counter= 0
        for i in bk:
            counter= counter + 1
            nhtml= nhtml + f'<tr onclick= "show_booking_information({i.booking_id});"><td>{counter}</td><td class= "hidesm">{ i.booking_id }</td><td>{ i.ven_info.ven_busname }</td><td>{ i.cus_info.cus_fname } { i.cus_info.cus_lname }</td><td class= "hidesm">{ i.service_info.service.service_name }</td><td class= "hidesm">{ i.calender_date }</td><td>{ i.confirmation_status.name }</td></tr>'
        
        return jsonify(status=1, message="Search successful", nhtml=nhtml)
    else:
        return jsonify(status=0, message="No record matches search parameter")