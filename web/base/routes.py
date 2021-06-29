from flask import render_template, Blueprint, request

from services import cache
from web.posts.models import Post

base = Blueprint('base', __name__)


@base.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    posts = cache.get(f'posts_{page}')
    if posts is None:
        posts = Post.query.order_by(Post.date.desc()).paginate(page=page, per_page=5)
        cache.set(f'posts_{page}', posts)
    return render_template('home.html', title='Home', posts=posts)
