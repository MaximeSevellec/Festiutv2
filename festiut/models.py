from .app import db, login_manager
from flask_login import UserMixin

class Utilisateur(db.Model, UserMixin):
    nom = db.Column(db.String(25), primary_key=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    monRole = db.Column(db.String(25), nullable=False)
    
    def get_id(self):
        return self.nom

class Festival(db.Model):
    idFestival = db.Column(db.Integer, primary_key=True, nullable=False)
    nomFestival = db.Column(db.String(25), nullable=False)
    villeFestival = db.Column(db.String(25), nullable=False)
    codePostalFestival = db.Column(db.String(5), nullable=False)
    debutFest = db.Column(db.DateTime, nullable=False)
    finFest = db.Column(db.DateTime, nullable=False)
    imageFestival = db.Column(db.LargeBinary(length=(2**32)-1), nullable=True)

class Event(db.Model):
    idEvent = db.Column(db.Integer, primary_key=True, nullable=False)
    idFestival = db.Column(db.Integer, db.ForeignKey('festival.idFestival'), nullable=False)
    nomEvent = db.Column(db.String(25), nullable=False)
    typeEvent = db.Column(db.String(25), nullable=False)
    dateHeureDebutEvent = db.Column(db.DateTime, nullable=False)
    dateHeureFinEvent = db.Column(db.DateTime, nullable=False)
    estGratuit = db.Column(db.Boolean, nullable=False)
    adresseEvent = db.Column(db.String(25), nullable=False)
    nbPlaceEvent = db.Column(db.Integer, nullable=False)
    imageEvent = db.Column(db.LargeBinary(length=(2**32)-1), nullable=True)

class Groupe(db.Model):
    nomGroupe = db.Column(db.String(25), primary_key=True, nullable=False)
    imageGroupe = db.Column(db.LargeBinary(length=(2**32)-1), nullable=True)

class Artiste(db.Model):
    nomArtiste = db.Column(db.String(25), primary_key=True, nullable=False)
    nomGroupe = db.Column(db.String(25), db.ForeignKey('groupe.nomGroupe'), nullable=False)
    styleArtiste = db.Column(db.String(25), nullable=False)
    urlInstaArtiste = db.Column(db.String(25), nullable=False)
    urlYoutubeArtiste = db.Column(db.String(25), nullable=False)
    imageArtiste = db.Column(db.LargeBinary(length=(2**32)-1), nullable=True)

class Reserver(db.Model):
    idEvent = db.Column(db.Integer, db.ForeignKey('event.idEvent'), primary_key=True, nullable=False)
    nomUtilisateur = db.Column(db.String(25), db.ForeignKey('utilisateur.nom'), primary_key=True, nullable=False)
    dateReservation = db.Column(db.Date, nullable=False)
    nbPlaceReserve = db.Column(db.Integer, nullable=False)

class Billet(db.Model):
    idBillet = db.Column(db.Integer, primary_key=True, nullable=False)
    nomUtilisateur = db.Column(db.String(25), db.ForeignKey('utilisateur.nom'), nullable=False)
    idFestival = db.Column(db.Integer, db.ForeignKey('festival.idFestival'), nullable=False)
    dateAchat = db.Column(db.DateTime, nullable=False)
    debutBillet = db.Column(db.DateTime, nullable=False)
    finBillet = db.Column(db.DateTime, nullable=False)
    prixBillet = db.Column(db.Float, nullable=False)
    nbPlaceBillet = db.Column(db.Integer, default=1)

class Logement(db.Model):
    idLogement = db.Column(db.Integer, primary_key=True, nullable=False)
    idFestival = db.Column(db.Integer, db.ForeignKey('festival.idFestival'), nullable=False)
    nomGroupe = db.Column(db.String(25), db.ForeignKey('groupe.nomGroupe'), nullable=False)
    nomLogement = db.Column(db.String(25), nullable=False)
    typeLogement = db.Column(db.String(25), nullable=False)
    nbPlaceLogement = db.Column(db.Integer, nullable=False)
    prixLogement = db.Column(db.Float, nullable=False)
    dateDebutLogement = db.Column(db.DateTime, nullable=False)
    dateFinLogement = db.Column(db.DateTime, nullable=False)
    imageLogement = db.Column(db.LargeBinary(length=(2**32)-1), nullable=True)

@login_manager.user_loader
def load_user(nom):
    return Utilisateur.query.get(nom)

def save_user(user):
    db.session.add(user)
    db.session.commit()