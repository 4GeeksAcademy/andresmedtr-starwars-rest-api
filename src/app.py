"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Favorites, Planet, Character
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)




# GET ALL USERS
@app.route('/user', methods=['GET'])
def get_users():

    users = User.query.all()
    request_body = list(map(lambda x: x.serialize(), users))

    return jsonify(request_body), 200



# GET SPECIFIC USER
@app.route('/user/<int:user_id>', methods=['GET'])
def get_single_user(user_id):
    user1 = User.query.get(user_id)
    if user1 is None:
        raise APIException("User doesn't exist", status_code=404)

    user_data = {
        'id': user1.id,
        'username': user1.username,
    }

    return jsonify(user_data), 200



# GET USERS/FAVORITES
@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def user_favorites(user_id):
    user = User.query.get(user_id)
    if user is None:
        raise APIException("User doesn't exist", status_code=404)
    
    favorites = user.favorites_id
    favorites_data = []

    for favorite in favorites:
        favorite_data = {
            'id': favorite.id,
            'name': favorite.name
        }
        favorites_data.append(favorite_data)

    return jsonify(favorites_data), 200

# GET ALL CHARACTERS
@app.route('/characters', methods=['GET'])
def get_characters():

    characters = Character.query.all()
    request_body = list(map(lambda x: x.serialize(), characters))

    return jsonify(request_body), 200

# GETT SPECIFIC CHARACTER
@app.route('/character/<int:character_id>', methods=['GET'])
def get_single_character(character_id):

    character = Character.query.get(character_id)
    if character is None:
        raise APIException("character doesn't exist", status_code=404)

    character_data = {
        'id': character.id,
        'name': character.name,
    }

    return jsonify(character_data), 200

# GET ALL PLANETS
@app.route('/planets', methods=['GET'])
def get_planets():

    planets = Planet.query.all()
    request_body = list(map(lambda x: x.serialize(), planets))

    return jsonify(request_body), 200

# GETT SPECIFIC CHARACTER
@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        raise APIException("planet doesn't exist", status_code=404)

    planet_data = {
        'id': planet.id,
        'name': planet.name,
    }

    return jsonify(planet_data), 200    

# /favorite/planet/<int:planet_id>
# POST A FAVORITE PLANET ON AN USER
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):

    # Get the current user (you can implement the logic to get the current user based on your authentication system)
    current_user = User.query.get(current_user.id)  # Replace with your logic to get the current user

    # Create a new favorite planet
    new_favorite_planet = Planet(name='Planet Name', planet_id=planet_id)
    current_user.favorites_id.favorite_planets = new_favorite_planet

    # Save the changes to the database
    db.session.add(new_favorite_planet)
    db.session.commit()

    return 'Favorite planet added successfully'

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
