#!/usr/bin/python

import os
from subprocess import Popen, PIPE
import argparse

_ROOT = os.path.abspath(os.path.dirname(__file__))
ENVIRONS_JSON = os.path.join(_ROOT, 'data', 'environs.json')

class SampleFactory:
    def __init__(self, *args, **kwargs):
        self.environs = environs(command = kwargs.get('command'), cluster = kwargs.get('cluster'), name = kwargs.get('name'), user = kwargs.get('user'), log = kwargs.get('log'), threads = kwargs.get('threads'), mem = kwargs.get('mem'))
    def __call__():
        pass

    def run_job(self):
        popen_command = self.environs.popen_command
        for script in self.bash_scripts:
            if self.debug==False:
                # Open a pipe to the command.
                proc = Popen(popen_command, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
                if (sys.version_info > (3, 0)):
                    proc.stdin.write(script.encode('utf-8'))
                    out, err = proc.communicate()
                else:
                    proc.stdin.write(script)
                    out, err = proc.communicate()
            # Print your job and the system response to the screen as it's submitted
            print(script)
            if self.debug==False:
                print(out)
                time.sleep(0.1)

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


    def load_environs(self, environs_file):
        with open(environs_file, "r") as read_file:
            data = json.load(read_file)
        return data

    def generate_job(self, commands, job):
            bash_script = self.assemble_script(   LOG_FILE = self.log, \
                                    JOB_NAME = self.name, \
                                    NODES = self.nodes, \
                                    COMMAND = commands[i][1],
                                    RAM = self.ram,
                                    THREADS = self,threads,
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
                    string = re.sub("<--{0}-->".format(j), fn_args.get(values_to_insert[i][j]), string)
                lines_parsed.append(string)
        return "\n".join(lines_parsed)



def run_qsubr(args=None):
    if args is None:
        args = sys.argv[1:]
    parser = argparse.ArgumentParser('The missing qsub command')
    parser.add_argument('script', type=str, help='A quotes string of commands')
    parser.add_argument('--cluster', '-c', type=str, default="PBS", help='cluster settings')
    parser.add_argument('--account', '-A', type=str, default="sfurla", help='account_string')
    parser.add_argument('--name', '-N', type=str, default="qsubr_job", help='name')
    parser.add_argument('--mem', '-gb', type=int, default=16, help='memory in gigabytes')
    parser.add_argument('--nodes', '-n', type=int, default=1, help='nodes')
    parser.add_argument('--threads', '-t', type=int, default=4, help='threads')
    parser.add_argument('--log', '-l', type=str, default="log_out", help='log filename')
    parser.add_argument('--debug', '-d', type=str, action='store_true', help='To print commands (For testing flow). OPTIONAL')
    args = parser.parse_args()
    qsubr_job = qsubr(script = args.script, threads = args.threads, nodes = args.nodes, mem = args.mem, name = args.name, debug=args.debug, cluster=args.cluster, log=args.log, user=args.account)
    qsubr.run_job()

if __name__ == "__main__":
    run_qsubr()