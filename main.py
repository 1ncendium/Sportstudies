from pwa import app, db
from pwa.models import User
from pwa.forms import RegistrationForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, redirect, request, url_for, flash, session
from flask_login import login_user, login_required, logout_user, current_user

@app.route('/logout') # Logt de gebruiker uit
@login_required
def logout():
    logout_user()
    flash('Je bent nu uitgelogd!')
    return redirect(url_for('login'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is not None:
            if user.check_password(form.wachtwoord.data):

                login_user(user)
                print('Je bent ingelogd')
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
        gebruikersnaam = request.form['gebruikersnaam']
        email = request.form['email']
        geslacht = request.form['geslacht']
        telefoon = request.form['telefoon']
        password = request.form['wachtwoord']
        nieuwe_user = User(gebruikersnaam=gebruikersnaam, email=email, geslacht=geslacht, telefoon=telefoon, password=password)
        db.session.add(nieuwe_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/profiel')
@login_required
def profiel():
    return render_template('profiel.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')