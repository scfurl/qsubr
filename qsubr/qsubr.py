#!/usr/bin/python

import os
from subprocess import Popen, PIPE, check_call
import argparse
import json
import re
import sys
import time

_ROOT = os.path.abspath(os.path.dirname(__file__))
#_ROOT = '/Users/sfurla/Box Sync/PI_FurlanS/computation/develop/qsubr/qsubr'
ENVIRONS_JSON = os.path.join(_ROOT, 'data', 'environs.json')

class make_script:
    def __init__(self, *args, **kwargs):
        self.debug = kwargs.get('debug')
        self.environs = environs(command = kwargs.get('command'), cluster = kwargs.get('cluster'), nodes = kwargs.get('nodes'), name = kwargs.get('name'), user = kwargs.get('user'), log = kwargs.get('log'), threads = kwargs.get('threads'), mem = kwargs.get('mem'))
        self.bash_script = self.environs.generate_job(command = kwargs.get('command'))
    def __call__():
        pass

    def run_job(self):
        f = open("tempscript.sh", "w")
        f.write(self.bash_script)
        f.close()
        popen_command = self.environs.popen_command+" tempscript.sh"
        if self.debug==False:
            check_call(popen_command, stdout=open(self.environs.log, "r"), stderr=open(self.environs.log, "r"), shell=True)
            print(self.bash_script)
            time.sleep(0.1)
        if self.debug==True:
            print(self.bash_script)

class environs:
    def __init__(self, *args, **kwargs):
        self.cluster = kwargs.get('cluster')
        self.user = kwargs.get('user')
        self.log = kwargs.get('log')
        self.name = kwargs.get('name')
        self.environs_data = self.load_environs(ENVIRONS_JSON).get(self.cluster)
        self.popen_command = self.environs_data["popen"]
        self.threads = kwargs.get('threads')
        self.ram = kwargs.get('mem')
        self.nodes = kwargs.get('nodes')



    def load_environs(self, environs_file):
        with open(environs_file, "r") as read_file:
            data = json.load(read_file)
        return data

    def generate_job(self, command):
        bash_script = self.assemble_script(   LOG_FILE = self.log, \
                                    JOB_NAME = self.name, \
                                    NODES = self.nodes, \
                                    COMMAND = command,
                                    RAM = self.ram,
                                    THREADS = self.threads,
                                    USER = self.user)
        return bash_script

    def assemble_script(self, *args, **kwargs):
        script_list=[]
        order=[]
        fn_args = kwargs
        for key, value in self.environs_data["script_lines"].items():
            script_list.append(value)
            order.append(key)
        script_list = [x for _,x in sorted(zip(order,script_list))]
        lines_unparsed = [x[0] for x in script_list]
        values_to_insert = [x[1].split("|") for x in script_list]
        lines_parsed = []
        global to_test
        to_test=[lines_unparsed, values_to_insert, fn_args]
        for i in range(len(lines_unparsed)):
            if values_to_insert[i][0] is "":
                lines_parsed.append(lines_unparsed[i])
            else:
                string=lines_unparsed[i]
                for j in range(len(values_to_insert[i])):
                    string = re.sub("<--{0}-->".format(j), str(fn_args.get(values_to_insert[i][j])), string)
                lines_parsed.append(string)
        return "\n".join(lines_parsed)
