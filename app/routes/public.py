from flask import Blueprint, render_template, flash, redirect, url_for, current_app, request
from flask_mail import Message
from datetime import datetime
from clinic_reservation.app import db, mail
from clinic_reservation.app.forms import ReservationForm
from clinic_reservation.app.models import Reservation
import traceback
import logging

bp = Blueprint('public', __name__)

@bp.route('/')
def index():
    services = ['ویزیت عمومی', 'دندانپزشکی', 'فیزیوتراپی', 'مشاوره تغذیه']
    return render_template('index.html', services=services)

@bp.route('/reserve', methods=['GET', 'POST'])
def reserve():
    form = ReservationForm()
    today = datetime.now().date()

    if form.validate_on_submit():
        # چک کردن تداخل ساعت
        try:
            time_obj = datetime.strptime(form.time.data, '%H:%M').time()
        except ValueError:
            flash('فرمت ساعت انتخاب شده معتبر نیست.', 'danger')
            return render_template('reserve.html', form=form, now=today)

        conflict = Reservation.query.filter_by(date=form.date.data, time=time_obj).first()
        if conflict:
            flash('این ساعت قبلاً رزرو شده، لطفا زمان دیگری انتخاب کنید.', 'danger')
            return render_template('reserve.html', form=form, now=today)

        # ذخیره رزرو در دیتابیس
        reservation = Reservation(
            name=form.name.data,
            phone=form.phone.data,
            email=form.email.data,
            service=form.service.data,
            date=form.date.data,
            time=time_obj
        )
        db.session.add(reservation)
        db.session.commit()

        # ارسال ایمیل (با مدیریت امن خطا)
        mail_username = current_app.config.get('MAIL_USERNAME')
        mail_password = current_app.config.get('MAIL_PASSWORD')
        mail_sender = current_app.config.get('MAIL_DEFAULT_SENDER')

        if mail_username and mail_password:
            logging.basicConfig(level=logging.DEBUG)
            logger = logging.getLogger(__name__)
            try:
                msg = Message(
                    subject="Reservation Confirmation",  # موضوع انگلیسی
                    recipients=[reservation.email],
                    sender=mail_sender
                )

                msg.body = f"""
سلام {reservation.name} عزیز،

رزرو شما برای خدمت "{reservation.service}" در تاریخ {reservation.date} ساعت {form.time.data} با موفقیت ثبت شد.

متشکریم،
کلینیک ما
"""

                # ارسال ایمیل
                mail.send(msg)


            except Exception as e:

                # چاپ فقط رشته ساده بدون ایموجی یا فارسی

                logger.error("خطا در ارسال ایمیل: %s", str(e))
        else:
            print("⚠️ ایمیل و پسورد پیکربندی نشده، ایمیل ارسال نمی‌شود.")

        flash('رزرو با موفقیت ثبت شد! ایمیل تایید برای شما ارسال گردید.', 'success')
        return redirect(url_for('public.confirm', id=reservation.id))

    return render_template('reserve.html', form=form, now=today)

@bp.route('/confirm/<int:id>')
def confirm(id):
    reservation = Reservation.query.get_or_404(id)
    return render_template('confirm.html', reservation=reservation)
