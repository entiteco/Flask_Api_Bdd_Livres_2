from marshmallow import Schema, fields

class LecteurSchema(Schema):
    id = fields.Int(dump_only=True)
    nom = fields.Str()
    prenom = fields.Str()
    mail = fields.Str()
    password = fields.Str()

class LivreSchema(Schema):
    id = fields.Int(dump_only=True)
    titre = fields.Str()
    auteur = fields.Str()
    isbn = fields.Str()

class EmpruntSchema(Schema):
    id = fields.Int(dump_only=True)
    date_emprunt = fields.DateTime()
    date_retour = fields.DateTime()
    lecteur = fields.Nested(LecteurSchema)
    livre = fields.Nested(LivreSchema)
