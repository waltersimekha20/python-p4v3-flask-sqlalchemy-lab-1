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

@app.route('/earthquakes/<int:id>')
def earthquake(id):
    earthquake = Earthquake.query.filter(Earthquake.id==id).first()

    if earthquake:
        body = earthquake.to_dict()
        response = 200
    else:
        body = {'message': f'Earthquake {id} not found.'}
        response = 404
    return make_response(body, response)

@app.route('/earthquakes/magnitude/<float:magnitude>')
def earthquake_magnitude(magnitude):
    earthquakes = []
    for earthquake in Earthquake.query.filter_by(Earthquake.id >= magnitude).first():
        earthquakes.append(earthquake.to_dict())
    return make_response(earthquakes, 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)