from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, DateField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional
from wtforms import ValidationError
from flask_login import current_user
from main.models import User

class RegistrationForm(FlaskForm):
    gebruikersnaam = StringField('Gebruikersnaam:', render_kw={"placeholder": "Gebruikersnaam"}, validators=[DataRequired()])
    email = StringField('Email', render_kw={"placeholder": "Gerbuiker@Domein.com"}, validators=[DataRequired(), Email()])
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

class NaamGegevensForm(FlaskForm):
    gebruikersnaam = StringField('Gebruikersnaam:', render_kw={"placeholder": 'Gebruikersnaam'}, validators=[Length(min=1, max=15)])
    email = StringField('Email:', render_kw={"placeholder": "E-Mail"}, validators=[Email()])
    voornaam = StringField('Voornaam:',render_kw={"placeholder": "Voornaam"}, validators=[Length(min=1, max=24)])
    achternaam = StringField('Achternaam:', render_kw={"placeholder": "Achternaam"}, validators=[Length(min=1, max=24)])
    telefoon = StringField('Telefoonnummer:', render_kw={"placeholder": "Telefoonnummer"}, validators=[Length(min=10, max=10)])

class AdresGegevensForm(FlaskForm):
    adres = StringField('Adres:',render_kw={"placeholder": "Adres"}, validators=[Length(min=1, max=24), Optional()])
    stad = StringField('Stad:',render_kw={"placeholder": "Stad"}, validators=[Length(min=1, max=24)])
    land = StringField('Land:',render_kw={"placeholder": "Land"}, validators=[Length(min=1, max=24)])

class NieuwWachtwoordForm(FlaskForm):
    wachtwoord = PasswordField('Wachtwoord:', render_kw={"placeholder": "*******"},
                             validators=[DataRequired(), EqualTo('wachtwoord_herhaal', message='Passwords Must Match!')])
    wachtwoord_herhaal = PasswordField('Bevestig wachtwoord:', render_kw={"placeholder": "*******"}, validators=[DataRequired()])