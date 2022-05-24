from gettext import Catalog
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from .  import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user



auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    data = request.form
    if request.method == 'POST':
        usr = request.form.get('username')
        pwd = request.form.get('password')
        user = User.query.filter_by(username=usr).first()
        if user:
            if check_password_hash(user.password, pwd):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for("display.home"))
            else:
                flash('Incorrect password', category='error')
        else:
            flash('No such user', category='error')

    print(data)
    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        usr = request.form.get('username')
        pwd = request.form.get('password')
        pwd1 = request.form.get('password1')
        
        if pwd != pwd1:
            flash("check password", category='error')
        elif pwd == '':
            flash("null password", category='error')
        elif User.query.filter_by(username=usr).first():
            flash("user already exist", category='error')
        else:
            new_user = User(username = usr, password = generate_password_hash(pwd, method='sha1'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("account added", category = 'success')
            return redirect(url_for("display.home"))


    return render_template('sign_up.html', user=current_user)
