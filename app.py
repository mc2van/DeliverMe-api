from main import mtspDriver
from flask import Flask, Response, request
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)
CORS(app)


@app.route('/api/mtsp', methods=['POST'])
@cross_origin()
def mtsp():
    locationsArray = request.get_json()
    data = json.loads(json.dumps(locationsArray))
    resp = mtspDriver(data)
    return Response(json.dumps(resp),  mimetype='application/json')


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


if __name__ == "__app__":
    app.run()
