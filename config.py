class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///library.db'  # Vous pouvez utiliser une autre base de données
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'your_jwt_secret_key'  # Remplacez par une clé secrète robuste
