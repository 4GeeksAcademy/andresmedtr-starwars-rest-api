from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites_id = relationship("Favorites", lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username
            # do not serialize the password, its a security breach
        }
    
class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    favorite_id = db.Column(db.Integer, ForeignKey("user.id"), unique=True, nullable=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    favorite_planets= relationship('Planet', backref="user", uselist=False)
    favorite_character= relationship('Character', backref="user", uselist=False)

    def __repr__(self):
        return f'<Favorites {self.name}>'


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
            # do not serialize the password, its a security breach
        }
    



class Character(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    character_id = db.Column(Integer, ForeignKey("favorites.id"))

    def __repr__(self):
        return f'<Character {self.name}>'


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
            # do not serialize the password, its a security breach
        }    
    

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    planet_id = db.Column(db.Integer, ForeignKey("favorites.id"))
  

    def __repr__(self):
        return f'<Planet {self.name}>'


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
            # do not serialize the password, its a security breach
        }
