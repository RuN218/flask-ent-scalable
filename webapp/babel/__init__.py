from flask import request, current_app, has_request_context, session
from flask_babel import Babel

babel = Babel()


@babel.localeselector
def get_locale():
    if has_request_context():
        locale = session.get('locale')
    if locale:
        return locale
    session['locale'] = 'en'
    return session['locale']

    # return request.accept_languages.best_match(current_app.config["LANGUAGES"])


def create_module(app, **kwargs):
    babel.init_app(app)

    from .controllers import babel_blueprint
    app.register_blueprint(babel_blueprint)
