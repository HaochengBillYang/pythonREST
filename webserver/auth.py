from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html', text='Work in Progress')

@auth.route('/logout')
def logout():
    return render_template('logout.html')

@auth.route('/sign-up')
def sing_up():
    return render_template('sign_up.html')
