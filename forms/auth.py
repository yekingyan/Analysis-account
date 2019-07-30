from wtforms import Form, StringField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(Form):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
