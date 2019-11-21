from flask import Flask, request
from flask_restful import Api, Resource
from flask_restful import reqparse, abort
from mark_parser import mark_parser

from flask_cors import CORS

import uuid
import json
import os
env_dist = os.environ 


app = Flask(__name__)

api = Api(app)
CORS(app, supports_credentials=True)

from resources.RemoteLog import RemoteLog
from resources.RemoteLog import RemoteLogList
from resources.Record import RecordList


from blueprint.RemoteLogManager import remotelog_blueprint


app.register_blueprint(blueprint=remotelog_blueprint, url_prefix='/manage')

api.add_resource(RemoteLog, '/logs/<log_id>')
api.add_resource(RemoteLogList, '/logs')

api.add_resource(RecordList, '/records')



if __name__ == '__main__':
    app.run(debug=True, port=5002)

