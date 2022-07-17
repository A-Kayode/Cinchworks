from flask import render_template, make_response, redirect, request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .. import app,db
from ..models import Customer, Vendor, Vendor_services, Services
from ..forms import Signup

@app.errorhandler(404)
def error404(error):
    content= make_response(render_template('general/error_404.html'),404)
    return content


@app.errorhandler(500)
def error500(error):
    content= make_response(render_template('general/error_500.html'),500)
    return content


@app.route('/')
def home_page():
    if session.get('cust_id') != None:
        return redirect('/cus/home')
    elif session.get('vend_id') != None:
        return redirect('/ven/home')
    else:
        return render_template("general/index.html")


@app.route('/login/', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        return render_template("general/login.html")
    else:
        username= request.form.get('username')
        password= request.form.get('pswd')
        if request.form.get('user_type') == "customer":
            c= Customer.query.filter(Customer.cus_username == username).first()
            if c != None:
                if check_password_hash(c.cus_password, password):
                    session['cust_id']= c.cus_id
                    return  redirect('/cus/home')
                else:
                    flash("Invalid Credentials")
                    return redirect('/login')
            else:
                flash("Invalid Credentials")
                return redirect('/login')
        elif request.form.get('user_type') == "vendor":
            v= Vendor.query.filter(Vendor.ven_username == username).first()
            if v != None:
                if check_password_hash(v.ven_password, password):
                    session['vend_id']= v.ven_id
                    return  redirect('/ven/home')
                else:
                    flash("Invalid Credentials")
                    return redirect('/login')
            else:
                flash("Invalid Credentials")
                return redirect('/login')


@app.route('/signup/', methods=['POST', 'GET'])
def signup_page():
    sform= Signup()
    if request.method == 'GET':
        return render_template("general/signup.html", sform=sform)
    else:
        username= request.form.get('username')
        fname= request.form.get('fname')
        lname= request.form.get('lname')
        email= request.form.get('email')
        password= request.form.get('pswd')
        hashed_password= generate_password_hash(password)
        if sform.validate_on_submit():
            if request.form.get('user_type') == "customer":
                c= Customer(cus_fname=fname, cus_lname=lname, cus_email=email, cus_username=username, cus_password=hashed_password)
                db.session.add(c)
                db.session.commit()
                custid= c.cus_id
                session['cust_id']= custid
                return redirect('/cus/home')
            elif request.form.get('user_type') == "vendor":
                v= Vendor(ven_fname=fname, ven_lname=lname, ven_email=email, ven_username=username, ven_password=hashed_password)
                db.session.add(v)
                db.session.commit()
                vendid= v.ven_id
                session['vend_id']= vendid
                return redirect('/ven/home')
        else:
            return render_template("general/signup.html", sform=sform)


@app.route('/contactus')
def contact_us():
    return render_template('general/contact_us.html')




#This contains the general code that is used in combination with the vendor search feature
@app.route('/vendorsearch/')
def vendor_search():
    vsearch= request.args.get('vendor_search')
    vs= Vendor_services.query.filter((Vendor_services.short_desc.like(f'%{vsearch}%')) | (Vendor_services.service.has(Services.service_name == vsearch))).all()
    vb= Vendor.query.filter(Vendor.ven_busname.like(f'%{vsearch}%')).all()
    if session.get('cust_id') != None:
        custid= session['cust_id']
        c= Customer.query.get(custid)
        return render_template('general/search.html', c=c, vs=vs, vb=vb)
    else:
        return render_template('general/search.html', vs=vs, vb=vb)


@app.route('/ajax/searchoption/')
def ajax_searchoption():
    sinput= request.args.get('sinput')
    posval1= Services.query.filter(Services.service_name.like(f'%{sinput}%')).all()
    posval2= Vendor.query.filter(Vendor.ven_busname.like(f'%{sinput}%'))

    optiontext= ""
    for i in posval1:
        optiontext= optiontext + f"<option value= '{i.service_name}'>"
    for j in posval2:
        optiontext= optiontext + f"<option value= '{j.ven_busname}'>"

    return optiontext





@app.route('/logout/')
def logout():
    if session.get('cust_id') != None:
        session.pop('cust_id')
    if session.get('vend_id') != None:
        session.pop('vend_id')
    return redirect('/')