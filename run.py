from app import create_app, db
from flask_migrate import Migrate
from flask_migrate import upgrade

app = create_app()
migrate = Migrate(app, db)

with app.app_context():
    upgrade()  # ← هر بار برنامه ران میشه، دیتابیس خودکار آپدیت میشه ✅

if __name__ == '__main__':
    app.run(debug=True, port=8000)


# from app import create_app, db   # تغییر این خط
# from flask_migrate import Migrate, upgrade
#
# app = create_app()
# migrate = Migrate(app, db)
#
# with app.app_context():
#     upgrade()
#
# if __name__ == '__main__':
#     app.run(debug=True, port=8000)
