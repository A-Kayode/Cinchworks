from flask import render_template, make_response, redirect, request, session
from . import app,db
from .models import Customers

@app.route('/')
def home_page():
    if session.get('user') != None:
        return redirect('/userhome')
    else:
        return render_template("index.html")

@app.route('/admin/')
def admin_page():
    return f"{session.get('user')}"
    # return render_template("admin_page.html")

@app.route('/login/')
def login_page():
    return render_template("login.html")

@app.route('/signup/', methods=['POST', 'GET'])
def signup_page():
    if request.method == 'GET':
        return render_template("signup.html")
    else:
        username= request.form.get('username')
        fname= request.form.get('fname')
        lname= request.form.get('lname')
        email= request.form.get('email')
        password= request.form.get('pswd')
        c= Customers(cus_fname=fname, cus_lname=lname, cus_email=email, cus_username=username, cus_password= password)
        db.session.add(c)
        db.session.commit()
        session['user']= username
        session['fname']= fname
        return redirect('/userhome')


        

@app.errorhandler(404)
def error404(error):
    content= make_response(render_template('error_404.html'),404)
    return content

@app.errorhandler(500)
def error500(error):
    content= make_response(render_template('error_500.html'),500)
    return content