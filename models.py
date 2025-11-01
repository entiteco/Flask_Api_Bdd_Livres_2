from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Lecteur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    mail = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    emprunts = db.relationship('Emprunt', backref='lecteur', lazy=True)

class Livre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200), nullable=False)
    auteur = db.Column(db.String(200), nullable=False)
    isbn = db.Column(db.String(13), unique=True, nullable=False)
    emprunts = db.relationship('Emprunt', backref='livre', lazy=True)

class Emprunt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_emprunt = db.Column(db.DateTime, default=datetime.utcnow)
    date_retour = db.Column(db.DateTime, nullable=True)
    lecteur_id = db.Column(db.Integer, db.ForeignKey('lecteur.id'), nullable=False)
    livre_id = db.Column(db.Integer, db.ForeignKey('livre.id'), nullable=False)
