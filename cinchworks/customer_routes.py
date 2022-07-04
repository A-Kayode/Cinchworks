from flask import render_template, make_response, redirect, session
from . import app

@app.route('/userhome/')
def user_home():
    namer= session.get('fname')
    return render_template('user_home.html', namer=namer)

@app.route('/logout/')
def logout():
    session.pop('user')
    session.pop('fname')
    return redirect('/')