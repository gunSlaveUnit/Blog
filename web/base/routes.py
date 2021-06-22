from flask import render_template, Blueprint

from web.posts.models import Post

base = Blueprint('base', __name__)


@base.route('/')
def home():
    posts = Post.query.all()
    return render_template('home.html', title='Home', posts = posts)
