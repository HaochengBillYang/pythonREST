from flask import Blueprint, render_template

display = Blueprint('display', __name__)

@display.route('/')
def home():
    return render_template('home.html',bool1=True, bool2 = False)
