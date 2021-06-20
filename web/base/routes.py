from flask import render_template, Blueprint

base = Blueprint('base', __name__)


@base.route('/')
def home():
    return render_template('home.html', title='Home')
