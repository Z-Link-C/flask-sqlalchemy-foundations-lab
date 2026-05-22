# server/app.py
#!/usr/bin/env python3
import json
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

@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_magnitude(magnitude):
    mag=db.session.execute(
        db.select(Earthquake).where(Earthquake.magnitude >= magnitude)
    ).scalars().all()

    d={
        "count":len(mag),
        "quakes":[
            {
            "id":e.id,
            "location":e.location,
            "magnitude":float(e.magnitude),
            "year":e.year
            }
            for e in mag
        ]
    }

    try:
        json_data = json.dumps(d)
        print("Serialized OK:", json_data)
    except Exception as e:
        print("json.dumps failed:", e)
        print("Data was:", d)
        raise
    response=make_response(json.dumps(d),200)
    response.headers["Content-Type"]="application/json"
    return response

@app.route('/earthquakes/<int:id>')
def get_earthquake(id):
    e=db.session.get(Earthquake,id)
    if e is None:
        b=json.dumps({"message":f"Earthquake {id} not found."})
        response = make_response(b,404)
    else:
        b=json.dumps({
            "id":e.id,"location":e.location,
            "magnitude":e.magnitude,"year":e.year
        })
        response=make_response(b)
    response.headers["Content-Type"]="application/json"
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
