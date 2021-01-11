from flask import Flask
from flask_babel import Babel, lazy_gettext as _l
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
babel = Babel()
login_manager = LoginManager()


def create_app(config_env=''):  # funkcja faktory
    app = Flask(__name__)

    if not config_env:
        config_env = app.env
        # w app.env jest zmienna srodowiskowa zapisana, wiec  jak ustawimy FLASK_ENV to tutaj sie wpisze

    app.config.from_object(f'config.{config_env.capitalize()}Config')  # liczone od source roota wiec lczy od music
    #  jakby source root byl na app to trzeba dodać .. config
    db.init_app(app)
    babel.init_app(app)
    login_manager.init_app(app)

    login_manager.session_protection = 'strong'
    login_manager.login_view = 'auth.login'
    login_manager.login_message = _l('You need to be logged in to access this page.')
    # default information if user want to get to page
    # _l do multilangue _l jest lazy
    login_manager.login_message_category = 'danger'

    from app.auth.views import bp_auth
    app.register_blueprint(bp_auth, url_prefix='/auth')



    with app.app_context():
        from app.album.views import bp_album
        app.register_blueprint(bp_album, url_prefix='/album')
        from app.main.views import bp_main
        app.register_blueprint(bp_main)
        from app.tour.views import bp_tour
        app.register_blueprint(bp_tour, url_prefix='/bp_tour')
        from app.admin.views import bp_admin
        app.register_blueprint(bp_admin, url_prefix='/admin')

    # aby używać app w form (notatnik page 15) context manager

    Migrate(app, db)

    return app
