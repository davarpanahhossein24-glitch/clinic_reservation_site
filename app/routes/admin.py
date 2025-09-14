from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, session
from clinic_reservation.app.models import Reservation
from clinic_reservation.app import db

bp = Blueprint('admin', __name__, url_prefix='/admin')

# ✅ صفحه ورود ادمین
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # اعتبارسنجی نام کاربری و رمز عبور
        if username == current_app.config['ADMIN_USERNAME'] and password == current_app.config['ADMIN_PASSWORD']:
            session['admin_logged_in'] = True
            flash("ورود موفقیت‌آمیز بود ✅", "success")
            return redirect(url_for("admin.dashboard"))
        else:
            flash("نام کاربری یا رمز عبور اشتباه است ❌", "danger")
    return render_template("admin/login.html")

# ✅ نمایش داشبورد فقط برای ادمین
@bp.route("/dashboard")
def dashboard():
    if not session.get('admin_logged_in'):
        flash("لطفاً ابتدا وارد شوید ❗", "warning")
        return redirect(url_for("admin.login"))

    q = request.args.get("q", "").strip()
    status = request.args.get("status", "")
    sort = request.args.get("sort", "date_desc")

    query = Reservation.query

    if q:
        query = query.filter(
            (Reservation.name.ilike(f"%{q}%")) |
            (Reservation.email.ilike(f"%{q}%")) |
            (Reservation.phone.ilike(f"%{q}%")) |
            (Reservation.service.ilike(f"%{q}%"))
        )

    if status:
        query = query.filter_by(status=status)

    if sort == "date_asc":
        query = query.order_by(Reservation.date.asc())
    elif sort == "name_asc":
        query = query.order_by(Reservation.name.asc())
    elif sort == "name_desc":
        query = query.order_by(Reservation.name.desc())
    else:
        query = query.order_by(Reservation.date.desc())

    reservations = query.all()
    return render_template("admin/dashboard.html", reservations=reservations)

# ✅ خروج ادمین
@bp.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    flash("با موفقیت خارج شدید ✅", "info")
    return redirect(url_for('admin.login'))

# ✅ تأیید رزرو
@bp.route('/confirm_reservation/<int:id>', methods=['POST', 'GET'])
def confirm_reservation(id):
    if not session.get('admin_logged_in'):
        flash("لطفاً ابتدا وارد شوید ❗", "warning")
        return redirect(url_for("admin.login"))

    reservation = Reservation.query.get_or_404(id)
    reservation.status = "confirmed"
    db.session.commit()
    flash("رزرو با موفقیت تأیید شد ✅", "success")
    return redirect(url_for("admin.dashboard"))

# ✅ لغو رزرو
@bp.route('/cancel_reservation/<int:id>', methods=['POST', 'GET'])
def cancel_reservation(id):
    if not session.get('admin_logged_in'):
        flash("لطفاً ابتدا وارد شوید ❗", "warning")
        return redirect(url_for("admin.login"))

    reservation = Reservation.query.get_or_404(id)
    reservation.status = "canceled"
    db.session.commit()
    flash("رزرو با موفقیت لغو شد ❌", "info")
    return redirect(url_for("admin.dashboard"))
