from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, DateField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError

class RegistrationForm(FlaskForm):
    gebruikersnaam = StringField('Gebruikersnaam:', render_kw={"placeholder": "Gebruikersnaam"}, validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    telefoon = IntegerField('Telefoonnummer:', render_kw={"placeholder": "Telefoonnummer"}, validators=[DataRequired()])
    geslacht = SelectField('Geslacht:', choices=['Man', 'Vrouw', 'Overig'])
    wachtwoord = PasswordField('Wachtwoord:', render_kw={"placeholder": "Wachtwoord"},
                             validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords Must Match!')])
    pass_confirm = PasswordField('Bevestig wachtwoord:', render_kw={"placeholder": "Bevestig Wachtwoord"}, validators=[DataRequired()])
    submit = SubmitField('Registreer!')

class LoginForm(FlaskForm):
    email = StringField('Email:', render_kw={"placeholder": "Email"}, validators=[DataRequired()])
    wachtwoord = PasswordField('Wachtwoord:', render_kw={"placeholder": "Wachtwoord"}, validators=[DataRequired()])
    submit = SubmitField('Log in:')
