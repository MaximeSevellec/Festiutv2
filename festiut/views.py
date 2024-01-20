from markupsafe import Markup
from .app import app, login_manager
from flask import render_template,request, redirect, url_for
from .models import *
from hashlib import sha256
from flask_login import login_user, current_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from datetime import datetime, time
from sqlalchemy.sql.expression import func
import locale
import base64
import copy

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

        festival_temp = copy.copy(festival)
        festival_temp.debutFest = min_dateheure
        festival_temp.finFest = max_dateheure
        
        festivals.append(festival_temp)

        groupes_festival = Groupe.query.select_from(Event).filter(Event.idFestival == festival.idFestival).all()
        if len(groupes) <= 5:
            groupes.extend(groupes_festival)
    return render_template("home.html", festivals=festivals, groupes=groupes)

@app.route("/festival/<int:idFestival>/")
def festival(idFestival):
    festival = Festival.query.get(idFestival)
    events = Event.query.filter(Event.idFestival == idFestival).order_by(Event.dateHeureDebutEvent).all()
    groupes = Groupe.query.select_from(Event).filter(Event.idFestival == idFestival).all()
    modifiable = Billet.query.filter(Billet.idFestival == festival.idFestival).first()
    return render_template("festival.html", festival=festival, events=events, groupes=groupes, modifiable=modifiable)

@app.route("/groupe/<string:nomGroupe>/")
def groupe(nomGroupe):
    groupe = Groupe.query.get(nomGroupe)
    artistes = Artiste.query.select_from(Groupe).filter(Groupe.nomGroupe == nomGroupe).all()
    return render_template("groupe.html", groupe=groupe, artistes=artistes)

@app.route("/event/<string:nomArtiste>/")
def artiste(nomArtiste):
    artiste = Artiste.query.get(nomArtiste)
    return render_template("artiste.html", artiste=artiste)

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