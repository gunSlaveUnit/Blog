from flask import render_template

from web.base import base


@base.route('/')
def home():
    return render_template('')
