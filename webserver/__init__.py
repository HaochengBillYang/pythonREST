from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hcd'

    from .display import display
    from .auth import auth

    app.register_blueprint(display, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')

    return app


