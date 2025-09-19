from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
from flask_mail import Mail

# ساخت یک نمونه واحد از db و mail
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()


@login_manager.user_loader
def load_user(user_id):
    from clinic_reservation.app.models import Admin as User
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # مقداردهی افزونه‌ها
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)

    # اینجا ایمپورت می‌کنیم تا بعد از init_app باشه
    from clinic_reservation.app import models
    from clinic_reservation.app.routes.public import bp as public_bp
    from clinic_reservation.app.routes.admin import bp as admin_bp

    # ثبت blueprintها
    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp)

    return app
#
#


# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from flask_login import LoginManager
# from config import Config   # تغییر این خط
# from flask_mail import Mail
#
# db = SQLAlchemy()
# migrate = Migrate()
# login_manager = LoginManager()
# mail = Mail()
#
# @login_manager.user_loader
# def load_user(user_id):
#     from app.models import Admin as User   # تغییر این خط
#     return User.query.get(int(user_id))
#
# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(Config)
#
#     db.init_app(app)
#     migrate.init_app(app, db)
#     login_manager.init_app(app)
#     mail.init_app(app)
#
#     from app import models   # تغییر این خط
#     from app.routes.public import bp as public_bp   # تغییر این خط
#     from app.routes.admin import bp as admin_bp     # تغییر این خط
#
#     app.register_blueprint(public_bp)
#     app.register_blueprint(admin_bp)
#
#     return app
