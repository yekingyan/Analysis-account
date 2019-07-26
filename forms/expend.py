from wtforms import Form, DateField
from wtforms.validators import DataRequired


class DaysForm(Form):
    start_date = DateField(validators=[DataRequired()], format='%Y/%m/%d')
    end_date = DateField(validators=[DataRequired()], format='%Y/%m/%d')
