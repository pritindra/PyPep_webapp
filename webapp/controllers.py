from flask import request, render_template, jsonify, flash
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from .models import *


def flash_errors(form):
    """Generate flashes for errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'error')


# e.g. controllers
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400) # missing arguments
    if User.query.filter_by(username = username).first() is not None:
        abort(400) # existing user
    usr = User(username = username)
    usr.hash_password(password)
    db.session.add(usr)
    db.session.commit()


def login(username,password):
    if username in user and check_password_hash(user.get(username), password):
        return username