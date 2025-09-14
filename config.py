import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'کلید_خیلی_رمزدار_و_طولانی'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'your_email@gmail.com'
    MAIL_PASSWORD = 'your_app_password'  # حتماً App Password
    MAIL_DEFAULT_SENDER = ('Clinic', 'your_email@gmail.com')

    ADMIN_USERNAME = 'admin'
    ADMIN_PASSWORD = '123456'
