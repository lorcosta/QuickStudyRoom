from flask import render_template

from app.errors import errors


@errors.app_errorhandler(401)
def error_401(e):
    return render_template('errors/401.html', title='401 - Not allowed'), 401


@errors.app_errorhandler(404)
def error_404(e):
    return render_template('errors/404.html', title='404 - Not found'), 404


@errors.app_errorhandler(500)
def error_500(e):
    return render_template('errors/500.html', title='500 - Server error'), 500
