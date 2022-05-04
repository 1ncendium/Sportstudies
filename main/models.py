from main import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import ForeignKey


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    gebruikersnaam = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    geslacht = db.Column(db.String)
    telefoon = db.Column(db.Integer)
    wachtwoord_hash = db.Column(db.String)
    voornaam = db.Column(db.String, default=None)
    achternaam = db.Column(db.String, default=None)
    adres = db.Column(db.String, default=None)
    stad = db.Column(db.String, default=None)
    land = db.Column(db.String, default=None)
    taal = db.Column(db.String, default='Nederlands')
    profiel_foto = db.Column(db.String, default='anonymous.jpg')

    def __init__(self, gebruikersnaam, email, geslacht, telefoon, password, voornaam, achternaam, adres, stad, land, taal):
        self.gebruikersnaam = gebruikersnaam
        self.email = email
        self.geslacht = geslacht
        self.telefoon = telefoon
        self.wachtwoord_hash = generate_password_hash(password)
        self.voornaam = voornaam
        self.achternaam = achternaam
        self.adres = adres
        self.stad = stad
        self.land = land
        self.taal = taal

    def check_password(self, password):
        return check_password_hash(self.wachtwoord_hash, password)

db.create_all()