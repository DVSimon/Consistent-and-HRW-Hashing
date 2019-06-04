from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import sys

app = Flask(__name__)
api = Api(app)

entries = {'num_entries': 0, 'entries': []}

# parser = reqparse.RequestParser()
# parser.add_argument('keyvalue')

class Cause(Resource):
    def post(self):
        # args = parser.parse_args()
        r_d = request.get_json()
        print(r_d)
        # kv = args['keyvalue']
        # key = kv.partition('{')[-1].rpartition(':')[0]
        # value = kv.partition(':')[-1].rpartition('}')[0]
        # entries['entries'].append({key: value})
        # entries['num_entries'] += 1
        [(k, v)] = r_d.items()
        entries['entries'].append({k: v})
        entries['num_entries'] += 1
        return r_d, 201

    def get(self):
        return entries


api.add_resource(Cause, '/api/v1/entries')

if __name__ == '__main__':
    app.run(port=sys.argv[1])
