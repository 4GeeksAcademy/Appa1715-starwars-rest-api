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
from models import db, User, Planet, People, Favorite
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

# User ------------------------------------------------------------------------------

@app.route('/user', methods=['GET'])
def get_user():
    user = User.query.all()
    user_serialized = list(map(lambda x : x.serialized(), user))
    return jsonify({"msg": 'The user has been successfuly created!', "user": user_serialized})

@app.route('/user/favorite', methods=['GET'])
def get_user_favorites():
    favorites = User.query.all()
    favorites_serialized = list(map(lambda x : x.serialized(), favorites))
    return jsonify({"msg": 'You have added a new favorite!', "favorites": favorites_serialized})


# People ------------------------------------------------------------------------------


@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    people_serialized = list(map(lambda x : x.serialized(), people))
    return jsonify({"msg": 'Completed', "people": people_serialized})

@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_by_id(people_id):
    single_person = People.query.get(people_id)
    if single_person is None:
        raise APIException("The person was not found")
    people_serialized = single_person.serialize()
    return jsonify({"msg": 'Success!', "people": people_serialized['people']})

# Planets ----------------------------------------------------------------------------

@app.route('/planet', methods=['GET'])
def get_planet():
    planet = Planet.query.all()
    planet_serialized = list(map(lambda x : x.serialized(), planet))
    return jsonify({"msg": 'Completed', "planet": planet_serialized})

@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet_by_id(planet_id):
    single_planet = Planet.query.get(planet_id)
    if single_planet is None:
        raise APIException("The planet does not exist")
    planet_serialized = single_planet.serialize()
    return jsonify({"msg": 'Success!', "planet": planet_serialized['planet']})


# Post Favorites ----------------------------------------------------------------------------

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def get_favorite_people(people_id):
    current_user = ""
    people = People.filter_by(id=people_id).first()
    if people is not None:
        new_favorite = Favorite.query.filter_by(name =people.name).first()
    if new_favorite:
        return jsonify({"ok": True, "msg": 'A person has been added to favorites'}), 200
    body = {
            "name": people.name,
            "user_id": current_user
        }
    the_favorite = Favorite.create(body)
    if the_favorite is not None:
            return jsonify(the_favorite.serialize()), 201
    return jsonify({
        "msg": "Person not found!"
    }), 404
        
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def get_favorite_planet(planet_id):
    current_user = ""
    planet = Planet.filter_by(id=planet_id).first()
    if planet is not None:
        new_favorite = Favorite.query.filter_by(name =planet.name).first()
    if new_favorite:
        return jsonify({"ok": True, "msg": 'A planet has been added to favorites'}), 200
    body = {
            "name": planet.name,
            "user_id": current_user
        }
    the_favorite = Favorite.create(body)
    if the_favorite is not None:
            return jsonify(the_favorite.serialize()), 201
    return jsonify({
        "msg": "Planet not found!"
    }), 404


# Delete Favorites ----------------------------------------------------------------------------

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    current_user = ""
    people = People.filtered_by(id=people_id).first()
    if people is not None:
        delete_person = Favorite.query.filter_by(name =people.name, user_id=current_user).first()
    if not delete_person:
        return jsonify({"ok": False, "msg": 'The person is not in favorites'}), 404
    try:
            db.session.delete(delete_person)
            db.session.commit()
            return jsonify({"ok": True, "msg": "A person has been removed from favorites"}), 200
    except Exception as error:
            print(error)
            db.session.rollback()
            return jsonify({"msg": "Sorry! Something happened! Try again later..."}), 500


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    current_user = ""
    planet = Planet.filtered_by(id=planet_id).first()
    if planet is not None:
        delete_planet = Favorite.query.filter_by(name =planet.name, user_id=current_user).first()
    if not delete_planet:
        return jsonify({"ok": False, "msg": 'The planet is not in favorites'}), 404
    try:
            db.session.delete(delete_planet)
            db.session.commit()
            return jsonify({"ok": True, "msg": "A planet has been removed from favorites"}), 200
    except Exception as error:
            print(error)
            db.session.rollback()
            return jsonify({"msg": "Sorry! Something happened! Try again later..."}), 500



















# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
