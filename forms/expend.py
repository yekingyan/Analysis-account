from datetime import date, timedelta
from wtforms import Form, DateField
from wtforms.validators import DataRequired


class DaysForm(Form):
    """默认 start30天之前  end 明天"""
    start_date = DateField(validators=[DataRequired()], format='%Y/%m/%d', default=date.today()-timedelta(days=30))
    end_date = DateField(validators=[DataRequired()], format='%Y/%m/%d', default=date.today()+timedelta(days=1))
