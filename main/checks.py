from main import db
from main.models import User
from werkzeug.security import generate_password_hash, check_password_hash

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