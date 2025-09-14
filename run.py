from clinic_reservation.app import create_app, db
from flask_migrate import Migrate
from flask_migrate import upgrade

app = create_app()
migrate = Migrate(app, db)

with app.app_context():
    upgrade()  # ← هر بار برنامه ران میشه، دیتابیس خودکار آپدیت میشه ✅

if __name__ == '__main__':
    app.run(debug=True, port=8000)
