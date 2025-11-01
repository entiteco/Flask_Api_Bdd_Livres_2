from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import db, Lecteur, Livre, Emprunt
from schemas import LecteurSchema, LivreSchema, EmpruntSchema
import config

app = Flask(__name__)
app.config.from_object(config.Config)
api = Api(app)
db.init_app(app)
jwt = JWTManager(app)

class Register(Resource):
    def post(self):
        data = request.get_json()
        schema = LecteurSchema()
        lecteur = Lecteur(
            nom=data['nom'],
            prenom=data['prenom'],
            mail=data['mail'],
            password=data['password']
        )
        db.session.add(lecteur)
        db.session.commit()
        return schema.dump(lecteur), 201

class Login(Resource):
    def post(self):
        data = request.get_json()
        lecteur = Lecteur.query.filter_by(mail=data['mail'], password=data['password']).first()
        if lecteur:
            access_token = create_access_token(identity=lecteur.id)
            return {'access_token': access_token}, 200
        return {'message': 'Invalid credentials'}, 401

class LivreResource(Resource):
    def get(self, livre_id):
        livre = Livre.query.get_or_404(livre_id)
        schema = LivreSchema()
        return schema.dump(livre), 200

    def post(self):
        data = request.get_json()
        schema = LivreSchema()
        livre = Livre(
            titre=data['titre'],
            auteur=data['auteur'],
            isbn=data['isbn']
        )
        db.session.add(livre)
        db.session.commit()
        return schema.dump(livre), 201

class EmpruntResource(Resource):
    @jwt_required()
    def get(self):
        lecteur_id = get_jwt_identity()
        lecteur = Lecteur.query.get_or_404(lecteur_id)
        emprunts = Emprunt.query.filter_by(lecteur_id=lecteur_id).all()
        schema = EmpruntSchema(many=True)
        return schema.dump(emprunts), 200

    @jwt_required()
    def post(self):
        data = request.get_json()
        lecteur_id = get_jwt_identity()
        livre = Livre.query.get_or_404(data['livre_id'])
        emprunt = Emprunt(
            lecteur_id=lecteur_id,
            livre_id=livre.id
        )
        db.session.add(emprunt)
        db.session.commit()
        return EmpruntSchema().dump(emprunt), 201

api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(LivreResource, '/livre', '/livre/<int:livre_id>')
api.add_resource(EmpruntResource, '/emprunts')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
