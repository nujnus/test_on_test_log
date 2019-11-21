from flask import Flask, request
from flask_restful import Api, Resource
from flask_restful import reqparse, abort
from mark_parser import mark_parser

from flask_cors import CORS

import sys
sys.path.append("..")
from log_backend.models.models import Record

import uuid
import json
import os
env_dist = os.environ 


parser = reqparse.RequestParser()
parser.add_argument('logfile', type=str)
parser.add_argument('expectfile', type=str)
parser.add_argument('passed', type=str)
parser.add_argument('casename', type=str)
parser.add_argument('history_cwd', type=str)
parser.add_argument('nightwatch_result', type=str)


class RecordList(Resource):
    def post(self):
        args = parser.parse_args()
        print(args)
        print(request.get_data())
        if args["passed"] == "true":
            arg_passed = True
        else:
            arg_passed = False
        action = Record.create(
            id=str(uuid.uuid4()),
            expectfile=args["expectfile"],
            logfile=args["logfile"],
            passed=arg_passed,
            casename=args["casename"],
            history_cwd=args["history_cwd"],
            nightwatch_result=args["nightwatch_result"]

        )

        return ""
