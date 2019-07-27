from datetime import date, timedelta
from wtforms import Form, DateField
from wtforms.validators import DataRequired


class DaysForm(Form):
    """默认 start30天之前  end 明天"""
    start_date = DateField(validators=[DataRequired()], format='%Y/%m/%d', default=date.today()-timedelta(days=30))
    end_date = DateField(validators=[DataRequired()], format='%Y/%m/%d', default=date.today()+timedelta(days=1))


class MonthsForm(Form):
    """默认 start3个月之前  end 下月月初"""
    start_month = DateField(validators=[DataRequired()], format='%Y/%m',
                            default=date.today().replace(month=date.today().month-3, day=1))
    end_month = DateField(validators=[DataRequired()], format='%Y/%m',
                          default=date.today().replace(month=date.today().month+1, day=1))
