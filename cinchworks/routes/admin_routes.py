from flask import render_template, redirect
from .. import app, db

@app.route('/admin/')
def admin_page():
    return render_template("admin/admin_page.html")