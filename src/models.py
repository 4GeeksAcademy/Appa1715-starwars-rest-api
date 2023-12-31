from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorite = db.relationship("Favorite", backref= "user", uselist=True)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }
    

class Planet(db.Model):
    __tablename__= 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    gravity = db.Column(db.String(120))
    terrain = db.Column(db.String(120))
    population = db.Column(db.String(120))


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "terrain": self.terrain,
            "population": self.population,
            "gravity": self.gravity,
        }
    
class People(db.Model):
    __tablename__= 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    hair_color = db.Column(db.String(120))
    skin_color = db.Column(db.String(120))
    eye_color = db.Column(db.String(120))
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"))
    planet = db.relationship("Planet")


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
        }


class Favorite(db.Model):
    __tablename__= 'favorite'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    __table_args__= (db.UniqueConstraint(
        'user_id',
        'name',
        name ='favorite_unique'
    ),)



    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "user_id": self.user_id,            
        }