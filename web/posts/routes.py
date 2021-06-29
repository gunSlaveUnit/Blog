from flask import Blueprint, flash, redirect, url_for, render_template, abort, request
from flask_login import login_required, current_user

from services import db
from web.posts.forms import PostForm
from web.posts.models import Post

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def make_new_post():
    new_post = PostForm()
    if new_post.validate_on_submit():
        post = Post(title=new_post.title.data, content=new_post.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created', 'success')
        return redirect(url_for('base.home'))
    return render_template('new_post.html', title='New Post',
                           form=new_post)


@posts.route("/post/<post_uuid>")
def show_post(post_uuid):
    post_to_show = Post.query.get_or_404(post_uuid)
    return render_template('post.html', title=post_to_show.title, post=post_to_show)


@posts.route("/post/<post_uuid>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_uuid):
    post = Post.query.get_or_404(post_uuid)
    if post.author != current_user:
        abort(403)
    form_with_new_post_data = PostForm()
    if form_with_new_post_data.validate_on_submit():
        post.title = form_with_new_post_data.title.data
        post.content = form_with_new_post_data.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.show_post', post_uuid=post.uuid))
    elif request.method == 'GET':
        form_with_new_post_data.title.data = post.title
        form_with_new_post_data.content.data = post.content
    return render_template('new_post.html', title='Update Post',
                           form=form_with_new_post_data)


@posts.route("/post/<post_uuid>/delete", methods=['GET', 'POST'])
@login_required
def delete_post(post_uuid):
    post = Post.query.get_or_404(post_uuid)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted', 'success')
    return redirect(url_for('base.home'))
