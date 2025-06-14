from flask import Flask, jsonify, abort
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
    return jsonify({'message': 'Flask SQLAlchemy Lab 1'})

@app.route('/earthquakes/<int:id>')
def earthquake(id):
    earthquake = Earthquake.query.filter_by(id=id).first()
    if not earthquake:
        abort(404, description=f"Earthquake {id} not found.")
    return jsonify(earthquake.to_dict())  # ✅ JSON response

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Not Found",
        "message": error.description
    }), 404

@app.route('/earthquakes/magnitude/<float:magnitude>')
def earthquakes_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    data = [eq.to_dict() for eq in earthquakes]

    response = {
        "count": len(data),
        "earthquakes": data
    }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)
