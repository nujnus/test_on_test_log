from os import listdir
from os.path import isfile, join
import sys

import json
import yaml


import os
from colorama import Fore, Back, Style, init

env_dist = os.environ 

def load_logs(target_filename):
  if not os.path.exists(target_filename):  
    f =  open(target_filename, 'w')        
    f.write("{}")                                                    
    f.close()                                                        
                                                                     
  with open(target_filename,'r') as load_f:
    logs = yaml.load(load_f)

  return logs

import requests, json

def compare(target_file, expect_file, casename, cwd, nightwatch_result):
    dict_1 = load_logs(target_file)
    dict_2 = load_logs(expect_file)
    init(autoreset=True)

    records_url = "http://127.0.0.1:5002/records"

    if (dict_1 == dict_2):
      print("=== start compare:")
      print(Fore.YELLOW + "test expect:", expect_file)
      print(Fore.GREEN + "test pass:", target_file)
      print("=== compare done.\n")
      data = {'logfile':target_file,
              'expectfile':expect_file,
              'passed':'true',
              'casename':casename,
              'history_cwd': cwd,
              'nightwatch_result': nightwatch_result
      }
      print("统计:", data)
    else:
      print("=== start compare:")
      print(Fore.YELLOW + "test expect:", expect_file)
      print(Fore.RED + "test failed", target_file)
      print("=== compare done.\n")
      data = {'logfile':target_file,
              'expectfile':expect_file,
              'passed':'false',
              'casename':casename,
              'history_cwd': cwd,
              'nightwatch_result': nightwatch_result
      }
      print("统计:", data)

    requests.post(records_url, json=data)



