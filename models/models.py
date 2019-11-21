from peewee import *
import os
db_file = os.path.abspath(os.path.dirname(__file__) + '/db/action.db')

db = SqliteDatabase(db_file)

class Action(Model):
    action_type = CharField()
    timestamp = CharField()
    log_backend = CharField(null=True, default="{}")

    class Meta:
        database = db

import uuid


class Record(Model):
    id = CharField()
    logfile = CharField()
    expectfile = CharField()
    passed = BooleanField()
    casename =  CharField()
    history_cwd =  CharField()
    nightwatch_result =  CharField()

    class Meta:
        database = db


db.connect()

