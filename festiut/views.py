from markupsafe import Markup
from .app import app, login_manager
from flask import render_template,request, redirect, url_for, jsonify
from .models import *
from hashlib import sha256
from flask_login import login_user, current_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from datetime import datetime, timedelta
from sqlalchemy.sql.expression import func
import locale
import base64
import copy
from sqlalchemy.orm import joinedload

class LoginForm(FlaskForm):
    nom = StringField('Nom')
    password = PasswordField('Password')
    def get_authenticated_user(self):
        user = Utilisateur.query.get(self.nom.data)
        if user is None:
            return None
        m = sha256()
        m.update(self.password.data.encode())
        passwd = m.hexdigest()
        return user if passwd == user.password else None
    
class RegisterForm(FlaskForm):
    nom = StringField('Nom')
    password = PasswordField('Password')
    def get_register_user(self):
        user = Utilisateur.query.get(self.nom.data)
        if user is not None:
            return None
        m = sha256()
        m.update(self.password.data.encode())
        passwd = m.hexdigest()
        user = Utilisateur(nom=self.nom.data, password=passwd, monRole="Utilisateur")
        save_user(user)
        return user
    
@login_manager.user_loader
def load_user(nom):
    return Utilisateur.query.get(nom)

@app.template_filter('datetime')
def datetime_filter(s):
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
    return s.strftime("%A %d %B %Y %H:%M").capitalize()

@app.template_filter('byte_to_image')
def byte_to_image(byte):
    if byte is None:
        return ""
    image_base64 = base64.b64encode(byte).decode('utf-8')
    return Markup(f'<img class="image" src="data:image/png;base64,{image_base64}" alt="Image">')

@app.route("/")
def home():
    festivals = []
    groupes = []
    for festival in Festival.query.filter(Festival.finFest >= datetime.now().date()).order_by(Festival.finFest).all():
        min_dateheure = Event.query.filter(Event.idFestival == festival.idFestival).with_entities(func.min(Event.dateHeureDebutEvent)).scalar()
        max_dateheure = Event.query.filter(Event.idFestival == festival.idFestival).with_entities(func.max(Event.dateHeureFinEvent)).scalar()

        if min_dateheure is None or max_dateheure is None:
            continue

        if Event.query.filter(Event.idFestival == festival.idFestival).with_entities(Event.nom_groupe, func.min(Event.dateHeureDebutEvent)).first()[0] is None:
            continue

        if Event.query.filter(Event.idFestival == festival.idFestival).with_entities(Event.nom_groupe, func.max(Event.dateHeureDebutEvent)).first()[0] is None:
            continue

        festival_temp = copy.copy(festival)
        festival_temp.debutFest = min_dateheure
        festival_temp.finFest = max_dateheure
        
        festivals.append(festival_temp)

        if len(groupes) <= 5:
            groupes_festival = Groupe.query.join(Event, Groupe.nomGroupe == Event.nom_groupe).filter(Event.idFestival == festival.idFestival).all()
            groupes.extend(groupes_festival)
    return render_template("home.html", festivals=festivals, groupes=groupes)

@app.route("/groupe/<string:nomGroupe>/")
def groupe(nomGroupe):
    groupe = Groupe.query.get(nomGroupe)
    artistes = Artiste.query.join(Groupe).filter(Groupe.nomGroupe == nomGroupe).all()
    return render_template("groupe.html", groupe=groupe, artistes=artistes)

@app.route("/event/<string:nomArtiste>/")
def artiste(nomArtiste):
    artiste = Artiste.query.get(nomArtiste)
    return render_template("artiste.html", artiste=artiste)

@app.route("/billeterie/")
def billeterie():
    billet_jour = {"Journée" : "20€", "2 jours" : "35", "Totalité du festival" : "50€"}
        
        
    return render_template("billeterie.html", billet_jour=billet_jour)

@app.route("/info_billet/<string:nomBillet>/")
def info_billet(nomBillet):
    festival = Festival.query.get(1)   
    if festival:

        debut_festival = festival.debutFest
        fin_festival = festival.finFest

        duree_festival = (fin_festival - debut_festival).days + 1

        jours_dispo = [debut_festival + timedelta(days=i) for i in range(duree_festival)]
        print(jours_dispo)

    return render_template("info_billet.html",nomBillet=nomBillet, jours_dispo=jours_dispo )

@app.template_filter('datetime_format')
def datetime_format(value, format='%A %d %B à %Hh%M'):
    return value.strftime(format) if value else ''


app.route("/programme/<int:idFestival>/<dateHeureDebutEvent>/")
def programme(idFestival, dateHeureDebutEvent):
        events = Event.query.filter(Event.idFestival == idFestival, Event.dateHeureDebutEvent == dateHeureDebutEvent, Event.dateHeureDebutEvent < dateHeureDebutEvent + timedelta(days=1)).order_by(Event.dateHeureDebutEvent).all()
        return render_template("programme.html", events=events)
    
@app.route('/festival/<int:festival_id>/day/<string:day>')
def day_detail(festival_id, day):
    festival = Festival.query.get_or_404(festival_id)

    day_date = datetime.strptime(day, '%Y-%m-%d')

    events = Event.query.filter_by(idFestival=festival_id).order_by(Event.dateHeureDebutEvent).all()

    events_for_day = [event for event in events if event.dateHeureDebutEvent.date() == day_date.date()]

    
    events_by_day = {}
    for event in events:
        event_day = event.dateHeureDebutEvent.date()
        if event_day not in events_by_day:
            events_by_day[event_day] = []
        events_by_day[event_day].append(event)

    return render_template('day_detail.html', festival=festival, day=day, events_by_day=events_by_day, events_for_day=events_for_day)

from flask import request

@app.route('/festival/<int:festival_id>/day/<string:day>/filter_by_location')
def filter_by_location(festival_id, day):
    festival = Festival.query.get_or_404(festival_id)
    day_date = datetime.strptime(day, '%Y-%m-%d')
    selected_location = request.args.get('location', default='', type=str)

    events = Event.query.filter_by(idFestival=festival_id).order_by(Event.dateHeureDebutEvent).all()

    if selected_location:
        events = [event for event in events if event.adresseEvent == selected_location]

    events_by_day = {}
    for event in events:
        event_day = event.dateHeureDebutEvent.date()
        if event_day not in events_by_day:
            events_by_day[event_day] = []
        events_by_day[event_day].append(event)

    return render_template('event_list.html', festival=festival, day=day, events_by_day=events_by_day)


@app.route('/festival/<int:festival_id>/location/<string:location>')
def location_detail(festival_id, location):
    festival = Festival.query.get_or_404(festival_id)
    
    events = Event.query.filter_by(idFestival=festival_id).order_by(Event.adresseEvent).all()

    events_for_location = [event for event in events if event.adresseEvent == location]

    return render_template('location_detail.html', festival=festival, location=location, events_for_location=events_for_location)

@app.route("/login/", methods =("GET","POST" ,))
def login():
    f = LoginForm ()
    if f.validate_on_submit():
        user = f.get_authenticated_user()
        if user:
            login_user(user)
            return redirect(url_for("home"))
    return render_template("login.html", form=f)

@app.route("/register/", methods =("GET","POST" ,))
def register():
    f = RegisterForm()
    if f.validate_on_submit():
        user = f.get_register_user()
        if user:
            login_user(user)
            return redirect(url_for("home"))
    return render_template("register.html", form=f)

@app.route("/logout/")
def logout ():
    logout_user()
    return redirect(url_for('home'))

@app.route("/ajouter_groupe_artiste")
def ajouter_groupe_artiste():
    if not current_user.is_authenticated or current_user.role != "Admin":
        return redirect(url_for("home"))
    groupes = Groupe.query.all()
    return render_template("ajouter_groupe_artiste.html", groupes=groupes)

@app.route('/ajouter_nouveau_artiste', methods=['POST'])
def ajouter_nouveau_artiste():

    data = request.form.to_dict()
    fichier = request.files['imageArtiste']

    byte = None
    if fichier:
        byte = fichier.read()

    nomArtiste = data['nomArtiste'] if 'nomArtiste' in data.keys() else None
    nomGroupe = data['nomGroupe'] if 'nomGroupe' in data.keys() else None
    styleArtiste = data['styleArtiste'] if 'styleArtiste' in data.keys() else None
    urlInstaArtiste = data['urlInstaArtiste'] if 'urlInstaArtiste' in data.keys() else None
    urlYoutubeArtiste = data['urlYoutubeArtiste'] if 'urlYoutubeArtiste' in data.keys() else None

    if nomArtiste is None or styleArtiste is None or urlInstaArtiste is None or urlYoutubeArtiste is None:
        return jsonify({'success': False, 'message': "Le nom de l'artiste ou le style n'est pas renseigné"})

    if nomGroupe is None:
        nomGroupe = Groupe.ajouter_nouveau_groupe(nomGroupe=nomArtiste, imageGroupe=None).nomGroupe
        print(nomGroupe)

    if Artiste.ajouter_un_artiste(nomArtiste=nomArtiste, nomGroupe=nomGroupe,styleArtiste=styleArtiste,urlInstaArtiste=urlInstaArtiste,urlYoutubeArtiste=urlYoutubeArtiste, imageArtiste=byte):
        return jsonify({'success': True})

    return jsonify({'success': False, 'message': "L'artiste est déjà dans la base de données"})

@app.route("/ajouter_nouveau_groupe", methods=['POST'])
def ajouter_nouveau_groupe():
    data = request.form.to_dict()
    fichier = request.files['imageGroupe']

    byte = None
    if fichier:
        byte = fichier.read()

    groupe = data['nomGroupe'] if 'nomGroupe' in data.keys() else None

    if groupe is None:
        return jsonify({'success': False, 'message': "Le nom du groupe n'est pas renseigné"})

    if Groupe.ajouter_nouveau_groupe(nomGroupe=groupe, imageGroupe=byte) is not None:
        return jsonify({'success': True})

    return jsonify({'success': False, 'message': "Le groupe est déjà dans la base de données"})

@app.route("/festival/<int:idFestival>/")
def festival(idFestival):
    festival = Festival.query.get(idFestival)
    events = Event.query.filter(Event.idFestival == idFestival).order_by(Event.dateHeureDebutEvent).all()
    groupes = Groupe.query.join(Event, Groupe.nomGroupe == Event.nom_groupe).filter(Event.idFestival == idFestival).all()

    events_by_day = {}
    for event in events:
        day = event.dateHeureDebutEvent.date()
        if day not in events_by_day:
            events_by_day[day] = []
        events_by_day[day].append(event)
    return render_template("festival.html", festival=festival, events=events, groupes=groupes, events_by_day=events_by_day)

@app.route("/ajouter_festival/")
def ajouter_festival():
    if not current_user.is_authenticated or current_user.role != "Admin":
        return redirect(url_for("home"))
    return render_template("ajouter_festival.html")

@app.route("/ajouter_nouveau_festival", methods=['POST'])
def ajouter_nouveau_festival():
    data = request.form.to_dict()
    fichier = request.files['imageFestival']

    byte = None
    if fichier:
        byte = fichier.read()

    nomFestival = data['nomFestival'] if 'nomFestival' in data.keys() else None
    villeFestival = data['villeFestival'] if 'villeFestival' in data.keys() else None
    codePostalFestival = data['codePostalFestival'] if 'codePostalFestival' in data.keys() else None
    debutFest = data['debutFest'] if 'debutFest' in data.keys() else None
    finFest = data['finFest'] if 'finFest' in data.keys() else None

    if nomFestival is None or villeFestival is None or codePostalFestival is None or debutFest is None or finFest is None:
        return jsonify({'success': False, 'message': "Le nom du festival, la ville, le code postal, la date de début ou la date de fin n'est pas renseignés"})

    if Festival.ajouter_nouveau_festival(nomFestival=nomFestival, villeFestival=villeFestival, codePostalFestival=codePostalFestival, debutFest=debutFest, finFest=finFest, imageFestival=byte) is not None:
        return jsonify({'success': True})

    return jsonify({'success': False, 'message': "Le festival est déjà dans la base de données"})

@app.route("/voir_festivals/")
def voir_festivals():
    if not current_user.is_authenticated or current_user.role != "Admin":
        return redirect(url_for("home"))
    festivals = Festival.query.order_by(Festival.debutFest).all()
    return render_template("voir_festivals.html", festivals=festivals)

@app.route("/ajouter_evenement/")
def ajouter_evenement():
    if not current_user.is_authenticated or current_user.role != "Admin":
        return redirect(url_for("home"))
    festivals = Festival.query.order_by(Festival.debutFest).all()
    groupes = Groupe.query.all()
    return render_template("ajouter_evenement.html", festivals=festivals, groupes=groupes)

@app.route("/ajouter_nouveau_event", methods=['POST'])
def ajouter_nouveau_event():
    data = request.form.to_dict()
    fichier = request.files['imageEvent']

    byte = None
    if fichier:
        byte = fichier.read()

    nomFestival = data['nomFestival'] if 'nomFestival' in data.keys() else None
    if(nomFestival is None):
        return jsonify({'success': False, 'message': "Le nom du festival n'est pas renseigné"})
    else:
        idFestival = Festival.query.filter(Festival.nomFestival == nomFestival).first().idFestival
    nomEvent = data['nomEvent'] if 'nomEvent' in data.keys() else None
    typeEvent = data['typeEvent'] if 'typeEvent' in data.keys() else None
    dateHeureDebutEvent = data['dateHeureDebutEvent'] if 'dateHeureDebutEvent' in data.keys() else None
    dateHeureFinEvent = data['dateHeureFinEvent'] if 'dateHeureFinEvent' in data.keys() else None
    estGratuit = data['estGratuit'] if 'estGratuit' in data.keys() else False
    adresseEvent = data['adresseEvent'] if 'adresseEvent' in data.keys() else None
    nbPlaceEvent = data['nbPlaceEvent'] if 'nbPlaceEvent' in data.keys() else None
    nom_groupe = data['nom_groupe'] if 'nom_groupe' in data.keys() else None

    if nomEvent is None or typeEvent is None or dateHeureDebutEvent is None or dateHeureFinEvent is None or adresseEvent is None or nbPlaceEvent is None:
        return jsonify({'success': False, 'message': "Le nom de l'évènement, le type, la date de début, la date de fin, l'adresse ou le nombre de place ne sont pas renseignés"})

    if nom_groupe is not None and Event.ajouter_nouveau_event(idFestival=idFestival, nomEvent=nomEvent, typeEvent=typeEvent, dateHeureDebutEvent=dateHeureDebutEvent, dateHeureFinEvent=dateHeureFinEvent, estGratuit=estGratuit, adresseEvent=adresseEvent, nbPlaceEvent=nbPlaceEvent, nom_groupe=nom_groupe, imageEvent=byte) is not None:

        nomLogement = data['nomLogement'] if 'nomLogement' in data.keys() else None
        typeLogement = data['typeLogement'] if 'typeLogement' in data.keys() else None
        nbPlaceLogement = data['nbPlaceLogement'] if 'nbPlaceLogement' in data.keys() else None
        prixLogement = data['prixLogement'] if 'prixLogement' in data.keys() else None
        dateDebutLogement = data['dateDebutLogement'] if 'dateDebutLogement' in data.keys() else None
        dateFinLogement = data['dateFinLogement'] if 'dateFinLogement' in data.keys() else None
        adresseLogement = data['adresseLogement'] if 'adresseLogement' in data.keys() else None

        print(nomLogement, typeLogement, nbPlaceLogement, prixLogement, dateDebutLogement, dateFinLogement, adresseLogement)

        if nomLogement is not None and typeLogement is not None and nbPlaceLogement is not None and prixLogement is not None and dateDebutLogement is not None and dateFinLogement is not None and adresseLogement is not None:
            if Logement.ajouter_nouveau_logement(nomGroupe=nom_groupe, nomLogement=nomLogement, typeLogement=typeLogement, nbPlaceLogement=nbPlaceLogement, prixLogement=prixLogement, dateDebutLogement=dateDebutLogement, dateFinLogement=dateFinLogement, adresseLogement=adresseLogement, idFestival=idFestival):
                return jsonify({'success': True})
            else:
                return jsonify({'success': False, 'message': "Une erreur s'est produite lors de l'ajout du logement"})

    return jsonify({'success': True})

@app.route("/assigner_groupe_event_sans_groupe/")
def assigner_groupe_event_sans_groupe():
    if not current_user.is_authenticated or current_user.role != "Admin":
        return redirect(url_for("home"))
    events = Event.query.filter(Event.nom_groupe == None).all()
    return render_template("assigner_groupe_event_sans_groupe.html", events=events)

@app.route("/assigner_groupe/<int:idEvent>/")
def assigner_groupe(idEvent):
    if not current_user.is_authenticated or current_user.role != "Admin":
        return redirect(url_for("home"))
    event = Event.query.get(idEvent)
    if event.nom_groupe is not None:
        return redirect(url_for("home"))
    groupes = Groupe.query.all()
    return render_template("assigner_groupe.html", event=event, groupes=groupes)

@app.route("/assigner_nouveau_groupe_event/<int:idEvent>", methods=['POST'])
def assigner_nouveau_groupe_event(idEvent):
    data = request.form.to_dict()
    nomGroupe = data['nomGroupe'] if 'nomGroupe' in data.keys() else None

    if idEvent is None or nomGroupe is None:
        return jsonify({'success': False, 'message': "L'évènement n'est pas renseigné"})

    event = Event.query.get(idEvent)
    event.nom_groupe = nomGroupe
    db.session.commit()
    return jsonify({'success': True})