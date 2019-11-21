from flask import Blueprint, request
import json
import yaml

import fcntl

import sys
sys.path.append("..")
from log_backend.models.models import Action
from log_backend.models.models import Record
from log_backend.resources.RemoteLog import jsonify


from flask import render_template
import os
statistics_template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
remotelog_blueprint = Blueprint('app', __name__, template_folder=statistics_template_path)


@remotelog_blueprint.route('/clear', methods=['GET'])
def clear():
    deletequery = Action.delete()
    deletequery.execute()
    return "clear!"

def write_logs(logs, target_filename):
  with open(target_filename, 'w+') as outfile:
    fcntl.flock(outfile, fcntl.LOCK_EX)
    yaml.dump(logs, outfile)
    outfile.write("\n")

def myFunc(e):
  return int(e['timestamp'])

@remotelog_blueprint.route('/tofile', methods=['POST'])
def tofile():
    all = Action.select()
    r = []
    for a in  all:
      r.append({"type": a.action_type, "timestamp": a.timestamp})
    print(r)
    r.sort(key=myFunc)
    r = [{"type": x["type"], "number": i} for i,x in enumerate(r)]
    print(r)

    data = request.get_data()    
    js_data = json.loads(data.decode("utf-8"))

    write_logs(r, js_data["target_filename"])

    return  "write_logs:" + js_data["target_filename"]

@remotelog_blueprint.route('/tofile_data', methods=['POST'])
def tofile_data():
    all = Action.select()
    r = []
    for a in  all:
      r.append({"type": a.action_type, "timestamp": a.timestamp, "log_backend": a.log_backend})
    print(r)
    r.sort(key=myFunc)
    r = [{"type": x["type"], "number": i, "log_backend": jsonify(x["log_backend"]) } for i,x in enumerate(r)]
    print(r)

    data = request.get_data()    
    js_data = json.loads(data.decode("utf-8"))

    write_logs(r, js_data["target_filename"]+".data")

    return  "write_logs:" + js_data["target_filename"] + ".data"



@remotelog_blueprint.route('/statistics', methods=['GET'])
def statistics():
    all = Record.select()
    passed = Record.select().where(Record.passed == True).count()
    failed = Record.select().where(Record.passed == False).count()
    nightwatch_passed = Record.select().where(Record.nightwatch_result == "0").count()


    r = []
    for a in  all:
      r.append({"nightwatch_result": a.nightwatch_result,"uuid": str(a.id), "logfile": a.logfile, "expectfile":a.expectfile, "passed": a.passed, "casename": a.casename})
    return render_template('index.html', all=r, passed=passed, failed=failed)



@remotelog_blueprint.route('/clear_statistics', methods=['GET'])
def clear_statistics():
    deletequery = Record.delete()
    deletequery.execute()
    return "clear!"

@remotelog_blueprint.route('/actions/', methods=['GET'])
def actions():
    all = Action.select()
    r = []
    for a in  all:
      r.append({"type": a.action_type, "timestamp": a.timestamp})
    r.sort(key=myFunc)
    if r:
      return render_template("actions.html", actions=[{"type": x["type"], "number": str(i)} for i,x in enumerate(r)])
    else:
      return str([{"nodata": True }])


@remotelog_blueprint.route('/log/', methods=['GET'])
def log():
    uuid = request.args.get('uuid')
    print(uuid)

    r = Record.select().where(Record.id == uuid).first()
    try:
      with open(r.logfile,'r') as parse_f:
        logfile = parse_f.read()
    except FileNotFoundError:
        logfile = "[fault]The file "+r.logfile+" can't find."

    try:
      with open(r.expectfile,'r') as parse_f:
        expectfile = parse_f.read()
    except FileNotFoundError:
        expectfile = "[fault]The file "+r.logfile+" can't find."

    try:
      with open(r.logfile+".data",'r') as parse_f:
        logdatafile = parse_f.read()
    except FileNotFoundError:
        logdatafile = "[fault]The file "+r.logfile+" can't find."

    try:
      with open(r.logfile+".data_expect",'r') as parse_f:
        logdata_expect_file = parse_f.read()
    except FileNotFoundError:
        logdata_exepect_file = "[fault]The file "+r.logfile+" can't find."


    return render_template('log.html', testname="result flow", expectname="expect flow", uuid=uuid, expectfile=expectfile,  logfile=logfile, data=logdatafile, data_expect=logdata_exepect_file, r=r)

from jinja2 import Environment, FileSystemLoader

@remotelog_blueprint.route('/rerun/', methods=['GET'])
def rerun():
    uuid = request.args.get('uuid')
    print(uuid)
    r = Record.select().where(Record.id == uuid).first()
    if(not r):
        return "record not found"

    cmd = "test " + r.logfile.rstrip("_test") + " \"" + r.casename + "\"\n"
    env = Environment(loader=FileSystemLoader(statistics_template_path))
    template = env.get_template('case_runner.template.sh')
    output_from_parsed_template = template.render(cmd=cmd, history_cwd=r.history_cwd, nightwatch_result=r.nightwatch_result) 
    print(output_from_parsed_template)
    
    with open("/tmp/my_new_file.html", "w") as fh:
        fh.write(output_from_parsed_template)

    os.system("osascript shell.scpt  'sh /tmp/my_new_file.html'")

    return  "run again"


@remotelog_blueprint.route('/open_test/', methods=['GET'])
def open_test():
    uuid = request.args.get('uuid')
    print(uuid)
    r = Record.select().where(Record.id == uuid).first()
    if(not r):
        return "record not found"
    os.system("osascript /Users/sunjun/Desktop/dotemacs/emacs_with_line.scpt " + r.logfile  + " " + "1")
    return r.logfile


@remotelog_blueprint.route('/open_expect/', methods=['GET'])
def open_expect():
    uuid = request.args.get('uuid')
    r = Record.select().where(Record.id == uuid).first()
    if(not r):
        return "record not found"
    os.system("osascript /Users/sunjun/Desktop/dotemacs/emacs_with_line.scpt " + r.expectfile  + " " + "1")
    return r.expectfile



@remotelog_blueprint.route('/open_test_data/', methods=['GET'])
def open_test_data():
    uuid = request.args.get('uuid')
    r = Record.select().where(Record.id == uuid).first()
    if(not r):
        return "record not found"
    os.system("osascript /Users/sunjun/Desktop/dotemacs/emacs_with_line.scpt " + r.logfile+".data" + " " + "1")
    return r.logfile+".data"


@remotelog_blueprint.route('/open_expect_data/', methods=['GET'])
def open_expect_data():
    uuid = request.args.get('uuid')
    r = Record.select().where(Record.id == uuid).first()
    if(not r):
        return "record not found"
    os.system("osascript /Users/sunjun/Desktop/dotemacs/emacs_with_line.scpt " + r.logfile+".data_expect" + " " + "1")
    return r.logfile+".data_expect"





