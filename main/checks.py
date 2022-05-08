from main import db
from main.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import uuid as uuid
import os
from main import app

def check_profiel(model, item, value):
    """
    Deze functie bekijkt de data die de gebruiker heeft opgegeven bij /profiel, en controleert of deze is veranderd.
    Als je dit niet zou doen, wordt de data None, omdat je deze wel meestuurt in de POST request.
    """
    if value == '' or value == getattr(model, item) or value == None:
        # Niks veranderd aan item, niks doen.
        pass
    else:
        # Iets veranderd aan item, doorvoeren in DB
        setattr(model, item, value)
        db.session.add(model)
        db.session.commit()

def check_Unique(model, item, value):
    """
    Is verantwoordelijk voor het controleren van de unieke waardes in onze database.
    Als een gebruiker zijn of haar gebruikersnaam veranderd naar iets dat al bestaat, moet deze functie dat aangeven.
    """
    exists = db.session.query(db.exists().where(getattr(model, item) == value)).scalar()
    if exists:
        return True
    else:
        return False

def check_and_store_wachtwoord(user, plaintextpassword):
    """
    Deze functie zorgt ervoor dat het nieuwe wachtwoord veilig (hashed) wordt opgeslagen in de database. 
    """

    if plaintextpassword != None:
        versleutelde_wachtwoord = generate_password_hash(plaintextpassword)
        user.wachtwoord_hash = versleutelde_wachtwoord
        db.session.add(user)
        db.session.commit()

def check_current_password(user, submitted_password):
    """
    Bekijkt of het huidige wachtwoord overeenkomt met de input bij het wijzigen van het wachtwoord.
    """
    if submitted_password != None:
        if not check_password_hash(user.wachtwoord_hash, submitted_password):
            return False
        else:
            return True

def delete_user(user):
    """
    Deze functie verwijderd een gebruiker uit de database
    """
    User.query.filter_by(id=user.id).delete()
    db.session.commit()
    return

def change_Profilepic(user, file):
    """
    Update de profielfoto van een user.
    """
    # Pak foto bestandsnaam
    profielfoto_filename = secure_filename(file.filename)
    # Set UUID
    profiel_foto_naam = str(uuid.uuid1()) + "_" + profielfoto_filename

    split_foto = profiel_foto_naam.split("_")
    naam = split_foto[1]
    if naam != "":
        uploads_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'uploads')
        os.makedirs(uploads_dir, exist_ok=True)
        file.save(os.path.join(uploads_dir, profiel_foto_naam))
        user.profiel_foto = profiel_foto_naam
        db.session.add(user)
        db.session.commit()