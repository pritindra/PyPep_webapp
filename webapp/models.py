from .extensions import db

# Defining Models for user
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(32), index = True)
    password_hash = db.Column(db.String(128))

    def hash_password(self,password):
        self.password_hash = generate_password_hash(password)
