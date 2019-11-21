from flask import Flask, request
from flask_restful import Api, Resource
from flask_restful import reqparse, abort
from mark_parser import mark_parser

from flask_cors import CORS

import sys
sys.path.append("..")
from log_backend.models.models import Action

import uuid
import json
import os
env_dist = os.environ 


parser = reqparse.RequestParser()
parser.add_argument('target_filename', type=str)
parser.add_argument('action_type', type=str)
parser.add_argument('source_filename', type=str)
parser.add_argument('timestamp', type=str)
parser.add_argument('order_number', type=str)
parser.add_argument('log_backend', type=str)



import fcntl

def load_logs(target_filename):
  if not os.path.exists(target_filename):  
    f =  open(target_filename, 'w')        
    fcntl.flock(f, fcntl.LOCK_EX)
    f.write("{}")                                                    
    f.close()                                                        
    fcntl.flock(load_f, fcntl.LOCK_UN)

                                                                     
  with open(target_filename,'r') as load_f:
    fcntl.flock(load_f, fcntl.LOCK_EX)
    print(load_f)
    logs = json.load(load_f)

  return logs


def write_logs(logs, target_filename):
  with open(target_filename, 'w+') as outfile:
    fcntl.flock(outfile, fcntl.LOCK_EX)
    json.dump(logs, outfile)          
    outfile.write("\n")



def abort_if_log_doesnt_exist(logs, log_id):
    if log_id not in logs:
        abort(404, message="log {} doesn't exist".format(log_id))



class RemoteLog(Resource):
    def get(self, log_id):
        return ""

    def put(self, log_id):
        return ""

    def delete(self, log_id):
        return ""

def myFunc(e):
  return int(e['timestamp'])

def jsonify(data):
  try:
  
    if type(data) == str:
      return json.loads(data)
    else:
      return {}
  except json.decoder.JSONDecodeError:
    return "JSONDecodeError"


class RemoteLogList(Resource):
    def get(self):
        all = Action.select()
        r = []
        for a in  all:
          r.append({"type": a.action_type, "timestamp": a.timestamp, "log_backend": a.log_backend})
        r.sort(key=myFunc)
        if r:
          return [{"type": x["type"], "number": i, "log_backend":  jsonify(x["log_backend"])} for i,x in enumerate(r)]
        else:
          return [{"nodata": True }]





    def post(self):
        args = parser.parse_args()
        print(args)
        action = Action.create(action_type=args["action_type"], timestamp=args["timestamp"], log_backend=args["log_backend"])
        return ""

 
