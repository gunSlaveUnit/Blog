from flask import Blueprint, render_template

from services import cache

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
@cache.cached(timeout=60)
def error_404(error):
    return render_template('errors/404.html'), 404


@errors.app_errorhandler(403)
@cache.cached(timeout=60)
def error_403(error):
    return render_template('errors/403.html'), 403


@errors.app_errorhandler(500)
@cache.cached(timeout=60)
def error_500(error):
    return render_template('errors/500.html'), 500
