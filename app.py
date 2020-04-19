from flask import Flask, request, jsonify, make_response, abort
from services import Services
app = Flask(__name__)

services = Services()

@app.route('/insert', methods=['POST'])
def insert():
    return jsonify({'key': services.insert(request.json)})


@app.route('/remove/<int:key>', methods=['DELETE'])
def remove(key):
    try:
        services.remove(key)
    except KeyError:
        abort(404)
    return ('', 204)


@app.route('/get/<int:key>', methods=['GET'])
def get(key):
    # Get point from Dict by key
    try:
        point = services.get(key)
    except KeyError:
        abort(404)
    return jsonify({'x': point[0], 'y': point[1]})


@app.route('/search', methods=['GET'])
def search():
        return jsonify({'points within rectangle': services.search(request.json)})

@app.errorhandler(404)
def notFound(error):
    return make_response("NOT FOUND", 404)


if __name__ == "__main__":
    app.run()
