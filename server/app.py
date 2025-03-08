# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def earthquake_by_id(id):
    e1 = Earthquake.query.filter(Earthquake.id == id).first()

    if e1:
        body = e1.to_dict()
        status = 200
    else:
        body = {'message': f'Earthquake {id} not found.'}
        status = 404

    return make_response(body, status)

@app.route('/earthquakes/magnitude/<float:magnitude>')
def earthquake_by_magnitude(magnitude):
    """Returns earthquakes with magnitude >= the given parameter"""
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    
    quakes_list = [quake.to_dict() for quake in earthquakes]

    body = {
        'count': len(quakes_list),
        'quakes': quakes_list
    }

    return make_response(body, 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
