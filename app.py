from main import app, db
from main.models import User
from main.forms import RegistrationForm, LoginForm, NaamGegevensForm, AdresGegevensForm, NieuwWachtwoordForm, AccountVerwijderenForm, FotoForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, redirect, request, url_for, flash, session
from flask_login import login_user, login_required, logout_user, current_user
from main.checks import check_profiel, check_Unique, check_and_store_wachtwoord, check_current_password, delete_user
from werkzeug.utils import secure_filename
import uuid as uuid
import os

@app.route('/logout') # Logt de gebruiker uit
@login_required
def logout():
    logout_user()
    flash('Je bent nu uitgelogd!')
    return redirect(url_for('login'))

@app.route('/vragenlijst')
def vragenlijst():
    return render_template('vragenlijst.html')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()

        if user is not None:
            if user.check_password(form.wachtwoord.data):

                login_user(user)
                flash('Logged in successfully.')

                next = request.args.get('next')

                if next == None or not next[0] == '/':
                    next = url_for('profiel')
                flash('Inloggen gelukt')
                return redirect(next)
        else:
            flash('Inloggen mislukt, probeer opnieuw.')
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        try:
            gebruikersnaam = request.form['gebruikersnaam']
            email = request.form['email'].lower()
            geslacht = request.form['geslacht']
            telefoon = request.form['telefoon']
            password = request.form['wachtwoord']
            nieuwe_user = User(gebruikersnaam=gebruikersnaam, email=email, geslacht=geslacht, telefoon=telefoon, 
                            password=password, voornaam=None, achternaam=None, adres=None, stad=None, taal=None, land=None)
            db.session.add(nieuwe_user)
            db.session.commit()
            return redirect(url_for('login'))
        except:
            flash('Gebruikersnaam of E-Mail al in gebruik!')
    return render_template('register.html', form=form)

@app.route('/profiel', methods=['GET', 'POST'])
@login_required
def profiel():

    user = User.query.filter_by(id=current_user.get_id()).first()
    naamGegevensForm = NaamGegevensForm()
    adresGegevensForm = AdresGegevensForm()
    nieuwWachtwoordForm = NieuwWachtwoordForm()
    accountVerwijderenForm = AccountVerwijderenForm()
    fotoForm = FotoForm()
    # Check of de request methode "POST" is
    if request.method == "POST":
        
        # Aanpassingen inventariseren
        gebruikersnaam = request.form.get('gebruikersnaam')
        email = request.form.get('email')
        voornaam = request.form.get('voornaam')
        achternaam = request.form.get('achternaam')
        adres = request.form.get('adres')
        stad = request.form.get('stad')
        land = request.form.get('land')
        taal = request.form.get('engels')
        telefoon = request.form.get('telefoon')
        huidig_wachtwoord = request.form.get('huidig_wachtwoord')
        nieuw_wachtwoord = request.form.get('nieuw_wachtwoord')
        confirm_wachtwoord = request.form.get('confirm_wachtwoord')
        profiel_foto = request.files['profiel_foto']
        # Pak foto bestandsnaam
        profielfoto_filename = secure_filename(profiel_foto.filename)
        # Set UUID
        profiel_foto_naam = str(uuid.uuid1()) + "_" + profielfoto_filename


        titels = ['gebruikersnaam', 'email', 'voornaam', 'achternaam', 'adres', 'stad', 'land', 'taal', 'telefoon']
        waardes = [gebruikersnaam, email, voornaam, achternaam, adres, stad, land, taal, telefoon]

        # Check of gebruikersnaam en email bestaat 
        gebruikersnaam_bestaat = check_Unique(User, 'gebruikersnaam', gebruikersnaam)
        email_bestaat = check_Unique(User, 'email', email)

        # Gebruiker wil wachtwoord wijzigen
        if huidig_wachtwoord != None:
            controle = check_current_password(user, huidig_wachtwoord)
            # Controleren of controlefunctie True heeft teruggestuurd (huidige wachtwoord komt overeen)
            if controle == False:
                return redirect(url_for('profiel')), flash('Huidig wachtwoord komt niet overeen')
            else:
                check_and_store_wachtwoord(user, nieuw_wachtwoord)

        if gebruikersnaam_bestaat:
            return redirect(url_for('profiel')), flash('Gebruikersnaam bestaat al')

        if email_bestaat:
            return redirect(url_for('profiel')), flash('Email bestaat al')

        # Gebruiker wil account verwijderen
        if confirm_wachtwoord != None:
            controleer_wachtwoord = check_current_password(user, confirm_wachtwoord)
            if controleer_wachtwoord == False:
                return redirect(url_for('profiel')), flash('Huidig wachtwoord komt niet overeen')
            else:
                delete_user(user)
                return redirect(url_for('account_verwijderd'))

        # Profielfoto veranderen
        split_foto = profiel_foto_naam.split("_")
        naam = split_foto[1]
        if naam != "":
            uploads_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'uploads')
            os.makedirs(uploads_dir, exist_ok=True)
            profiel_foto.save(os.path.join(uploads_dir, profiel_foto_naam))
            user.profiel_foto = profiel_foto_naam
            db.session.add(user)
            db.session.commit()

        # Check waardes en data
        for i, j in zip(titels, waardes):
            check_profiel(user, i, j)
    

    gebruikersnaam = user.gebruikersnaam
    email = user.email
    voornaam = user.voornaam
    achternaam = user.achternaam
    email = user.email
    adres = user.adres
    stad = user.stad
    land = user.land
    telefoon = user.telefoon
    profielfoto = user.profiel_foto

    return render_template('profiel.html', gebruikersnaam=gebruikersnaam, email=email, voornaam=voornaam, achternaam=achternaam,
                            adres=adres, stad=stad, land=land, telefoon=telefoon, accountVerwijderenForm=accountVerwijderenForm, 
                            naamGegevensForm=naamGegevensForm, adresGegevensForm=adresGegevensForm, nieuwWachtwoordForm=nieuwWachtwoordForm,
                            fotoForm=fotoForm, profielfoto=profielfoto)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    profielfoto = User.query.filter_by(id=current_user.get_id()).first().profiel_foto
    return render_template('dashboard.html', profielfoto=profielfoto)

@app.route('/privacy', methods=['GET', 'POST'])
def privacy():
    try:
        profielfoto = User.query.filter_by(id=current_user.get_id()).first().profiel_foto
    except:
        profielfoto = 1

    return render_template('privacy.html', profielfoto=profielfoto)

@app.route('/account_verwijderd')
def account_verwijderd():
    user = current_user.get_id()
    if user != None:
        return redirect(url_for('profiel'))
    else:
        return render_template('account_verwijderd.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')