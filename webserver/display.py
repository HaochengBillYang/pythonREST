from flask import Blueprint, render_template
from flask_login import login_required, current_user

display = Blueprint('display', __name__)

@display.route('/')
@login_required
def home():
    return render_template('home.html', user = current_user)
