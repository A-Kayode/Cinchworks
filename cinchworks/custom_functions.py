from functools import wraps
from flask import session, flash, redirect

# validation decorator
def cusvalidation(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('cust_id') != None:
            return func(*args, **kwargs)
        else:
            flash('You have to login first')
            return redirect('/login')
    return wrapper


def venvalidation(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('vend_id') != None:
            return func(*args, **kwargs)
        else:
            flash('You have to login first')
            return redirect('/login')
    return wrapper


def rewrite_duration(a,b):
    c,d= int(a),int(b)
    if c < 1:
        e = ""
    elif c == 1:
        e= f"{c} hour "
    else:
        e= f"{c} hours "
    
    if d < 1:
        f= ""
    elif d == 1:
        f= f"{d} minute"
    else:
        f= f"{d} minutes"

    return e + f


def calc_endtime(a,b):
    c,d= a.split(':')
    c,d= int(c), int(d)

    e,f= b.split(':')
    e,f= int(e), int(f)

    mn= f + d
    hr= c + e
    if mn > 59:
        extra= mn-60
        exhr= 1 + (extra//60)
        hr= hr + exhr
        mn= mn - (60 * exhr)

    i, j= str(hr),str(mn)
    if len(i) < 2:
        i= "0"+i
    if len(j) < 2:
        j= "0"+j
    
    return i+":"+j
