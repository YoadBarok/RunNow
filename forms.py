from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length


class AddRace(FlaskForm):
    race_name = StringField(label='Race Name', validators=[DataRequired()])
    race_date = StringField(label='Race Date', validators=[DataRequired()])
    submit = SubmitField(label='Add')


class RegisterForm(FlaskForm):
    name = StringField(label='Your name: ', validators=[DataRequired()])
    email = StringField(label="Your email: ", validators=[DataRequired()])
    password = PasswordField(label="Your password: ",
                             validators=[DataRequired(),
                                         Length(min=8),
                                         EqualTo("confirm", message="Password must match")])
    confirm = PasswordField(label="Confirm your password: ")
    submit = SubmitField(label="Register")


class LoginForm(FlaskForm):
    email = StringField(label="Email: ", validators=[DataRequired()])
    password = PasswordField(label="Password: ", validators=[DataRequired()])
    submit = SubmitField(label="Login")
