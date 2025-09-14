from flask_wtf import FlaskForm
from wtforms.fields import TimeField
from datetime import date
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, TimeField, SelectField  # و هر فیلدی که نیاز داری
from wtforms.validators import DataRequired, Email, Length, EqualTo
from flask import current_app


class ReservationForm(FlaskForm):
    name = StringField('نام کامل', validators=[DataRequired(), Length(min=2, max=120)])
    phone = StringField('شماره تماس', validators=[DataRequired(), Length(min=7, max=20)])
    email = StringField('ایمیل', validators=[DataRequired(), Email()])
    service = SelectField('خدمت', choices=[
        ('ویزیت عمومی', 'ویزیت عمومی'),
        ('دندانپزشکی', 'دندانپزشکی'),
        ('فیزیوتراپی', 'فیزیوتراپی'),
        ('مشاوره تغذیه', 'مشاوره تغذیه')
    ], validators=[DataRequired()])
    date = DateField('تاریخ نوبت', validators=[DataRequired()], default=date.today)
    time = SelectField('ساعت نوبت', choices=[
        ('09:00', '09:00'),
        ('10:00', '10:00'),
        ('11:00', '11:00'),
        ('12:00', '12:00'),
        ('13:00', '13:00'),
        ('14:00', '14:00'),
        ('15:00', '15:00'),
        ('16:00', '16:00')
    ], validators=[DataRequired()])
    submit = SubmitField('رزرو کن')

class AdminLoginForm(FlaskForm):
    username = StringField('نام کاربری', validators=[DataRequired()])
    password = PasswordField('رمز عبور', validators=[DataRequired()])
    submit = SubmitField('ورود')

