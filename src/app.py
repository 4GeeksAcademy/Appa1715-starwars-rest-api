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
from models import db, User, Planet, People
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
#Get ><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>

@app.route('/user', methods=['GET'])
def get_user():
    user = User.query.all()
    user_serialized = list(map(lambda x : x.serialized(), user))
    return jsonify({"msg": 'The user has been successfuly created!', "user": user_serialized})


# People ------------------------------------------------------------------------------
#Get ><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>

@app.route('/people', methods=['GET'])
def get_planet():
    people = People.query.all()
    people_serialized = list(map(lambda x : x.serialized(), people))
    return jsonify({"msg": 'Completed', "people": people_serialized})

# Planets ----------------------------------------------------------------------------
#Get ><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>

@app.route('/planet', methods=['GET'])
def get_planet():
    planet = Planet.query.all()
    planet_serialized = list(map(lambda x : x.serialized(), planet))
    return jsonify({"msg": 'Completed', "planet": planet_serialized})




#Put ><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>

@app.route('/planet', methods=['PUT'])
def modify_planet():
    body = request.get_json(silent = True)
    if body is None:
        raise APIException("Debes de enviar información al body", status_code=400)
    if "id" not in body:
        raise APIException("Debes enviar el id del planeta a modificar", status_code=400)
    if "name" not in body:
        raise APIException("Debes enviar el nombre del planeta", status_code=400)
    return jsonify({"msg": 'Completed'})



















# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
