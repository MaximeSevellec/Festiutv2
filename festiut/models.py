from .app import db, login_manager
from flask_login import UserMixin
from datetime import datetime, time

class Utilisateur(db.Model, UserMixin):
    nom = db.Column(db.String(25), primary_key=True, default="Utilisateur")
    password = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(25), nullable=False)
    
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

    events = db.relationship('Event', backref='festival', lazy=True)
    logements = db.relationship('Logement', backref='festival', lazy=True)
    billets = db.relationship('Billet', backref='festival', lazy=True)

    def ajouter_nouveau_festival(nomFestival, villeFestival, codePostalFestival, debutFest, finFest, imageFestival):
        debutFest = datetime.combine(datetime.strptime(debutFest, "%Y-%m-%d"), time(0,0))
        finFest = datetime.combine(datetime.strptime(finFest, "%Y-%m-%d"), time(0,0))
        if Festival.query.filter(Festival.nomFestival == nomFestival).first() is not None:
            return None
        festival = Festival(nomFestival=nomFestival, villeFestival=villeFestival, codePostalFestival=codePostalFestival, debutFest=debutFest, finFest=finFest, imageFestival=imageFestival)
        db.session.add(festival)
        db.session.commit()
        return festival

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
    nom_groupe = db.Column(db.String(25), db.ForeignKey('groupe.nomGroupe'), nullable=True)
    imageEvent = db.Column(db.LargeBinary(length=(2**32)-1), nullable=True)

    reservations = db.relationship('Reserver', backref='event', lazy=True)
    
    def to_json(self):
        return {
            'idEvent': self.idEvent,
            'idFestival': self.idFestival,
            'nomEvent': self.nomEvent,
            'typeEvent': self.typeEvent,
            'dateHeureDebutEvent': self.dateHeureDebutEvent,
            'dateHeureFinEvent': self.dateHeureFinEvent,
            'estGratuit': self.estGratuit,
            'adresseEvent': self.adresseEvent,
            'nbPlaceEvent': self.nbPlaceEvent,
            'nom_groupe': self.nom_groupe,
            'imageEvent': self.imageEvent
        }

    def ajouter_nouveau_event(idFestival, nomEvent, typeEvent, dateHeureDebutEvent, dateHeureFinEvent, estGratuit, adresseEvent, nbPlaceEvent, nom_groupe, imageEvent):
        
        event = Event(idFestival=idFestival, nomEvent=nomEvent, typeEvent=typeEvent, dateHeureDebutEvent=dateHeureDebutEvent, dateHeureFinEvent=dateHeureFinEvent, estGratuit=estGratuit, adresseEvent=adresseEvent, nbPlaceEvent=nbPlaceEvent, nom_groupe=nom_groupe, imageEvent=imageEvent)
        db.session.add(event)
        db.session.commit()
        return event

class Groupe(db.Model):
    nomGroupe = db.Column(db.String(25), primary_key=True, nullable=False)
    imageGroupe = db.Column(db.LargeBinary(length=(2**32)-1), nullable=True)

    artistes = db.relationship('Artiste', backref='groupe', lazy=True)
    events = db.relationship('Event', backref='groupe', lazy=True)
    logements = db.relationship('Logement', backref='groupe', lazy=True)

    def ajouter_nouveau_groupe(nomGroupe, imageGroupe):
        if Groupe.query.get(nomGroupe) is not None:
            return Groupe.query.get(nomGroupe)
        groupe = Groupe(nomGroupe=nomGroupe, imageGroupe=imageGroupe)
        db.session.add(groupe)
        db.session.commit()
        return groupe

class Artiste(db.Model):
    nomArtiste = db.Column(db.String(25), primary_key=True, nullable=False)
    nomGroupe = db.Column(db.String(25), db.ForeignKey('groupe.nomGroupe'), nullable=False)
    styleArtiste = db.Column(db.String(25), nullable=False)
    urlInstaArtiste = db.Column(db.String(25), nullable=False)
    urlYoutubeArtiste = db.Column(db.String(25), nullable=False)
    imageArtiste = db.Column(db.LargeBinary(length=(2**32)-1), nullable=True)

    def ajouter_un_artiste(nomArtiste, nomGroupe, styleArtiste, urlInstaArtiste, urlYoutubeArtiste, imageArtiste):
        try:
            artiste = Artiste(nomArtiste=nomArtiste, nomGroupe=nomGroupe, styleArtiste=styleArtiste, urlInstaArtiste=urlInstaArtiste, urlYoutubeArtiste=urlYoutubeArtiste, imageArtiste=imageArtiste)
            db.session.add(artiste)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False

class Reserver(db.Model):
    idEvent = db.Column(db.Integer, db.ForeignKey('event.idEvent'), primary_key=True, nullable=False)
    nomUtilisateur = db.Column(db.String(25), db.ForeignKey('utilisateur.nom'), primary_key=True, nullable=False)
    dateReservation = db.Column(db.Date, nullable=False, default=datetime.now())
    nbPlaceReserve = db.Column(db.Integer, nullable=False, default=1)

    def reserver_event(idEvent, nomUtilisateur, dateReservation, nbPlaceReserve):
        try:
            reserver = Reserver(idEvent=idEvent, nomUtilisateur=nomUtilisateur, dateReservation=dateReservation, nbPlaceReserve=nbPlaceReserve)
            db.session.add(reserver)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False
        

class Billet(db.Model):
    idBillet = db.Column(db.Integer, primary_key=True, nullable=False)
    nomUtilisateur = db.Column(db.String(25), db.ForeignKey('utilisateur.nom'), nullable=False)
    idFestival = db.Column(db.Integer, db.ForeignKey('festival.idFestival'), nullable=False)
    dateAchat = db.Column(db.DateTime, nullable=False)
    debutBillet = db.Column(db.DateTime, nullable=False)
    finBillet = db.Column(db.DateTime, nullable=False)
    prixBillet = db.Column(db.Float, nullable=False)
    nbPlaceBillet = db.Column(db.Integer, default=1)

    def acheter_billet(nomUtilisateur, idFestival, dateAchat, debutBillet, finBillet, prixBillet, nbPlaceBillet):
        try:
            billet = Billet(nomUtilisateur=nomUtilisateur, idFestival=idFestival, dateAchat=dateAchat, debutBillet=debutBillet, finBillet=finBillet, prixBillet=prixBillet, nbPlaceBillet=nbPlaceBillet)
            db.session.add(billet)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False
    
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
    adresseLogement = db.Column(db.String(25), nullable=False)

    def ajouter_nouveau_logement(idFestival, nomGroupe, nomLogement, typeLogement, nbPlaceLogement, prixLogement, dateDebutLogement, dateFinLogement, adresseLogement):
        logement = Logement(idFestival=idFestival, nomGroupe=nomGroupe, nomLogement=nomLogement, typeLogement=typeLogement, nbPlaceLogement=nbPlaceLogement, prixLogement=prixLogement, dateDebutLogement=dateDebutLogement, dateFinLogement=dateFinLogement, adresseLogement=adresseLogement)
        db.session.add(logement)
        db.session.commit()
        return logement

@login_manager.user_loader
def load_user(nom):
    return Utilisateur.query.get(nom)

def save_user(user):
    db.session.add(user)
    db.session.commit()