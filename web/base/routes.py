from flask import render_template, Blueprint, request

from services import cache
from web.posts.models import Post

base = Blueprint('base', __name__)


@base.route('/')
@cache.cached(timeout=60)
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', title='Home', posts=posts)
