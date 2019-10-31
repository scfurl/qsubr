import sys
import os
from subprocess import Popen, PIPE
import argparse
import getpass
from . import qsubr

def run_qsubr(args=None):
    parser = argparse.ArgumentParser('The missing qsub command')
    parser.add_argument('script', type=str, help='A quoted string of commands')
    parser.add_argument('--cluster', '-c', type=str, default="PBS", help='cluster settings')
    parser.add_argument('--account', '-A', type=str, default="sfurla", help='account_string')
    parser.add_argument('--name', '-N', type=str, default="qsubr_job", help='name')
    parser.add_argument('--mem', '-gb', type=int, default=16, help='memory in gigabytes')
    parser.add_argument('--nodes', '-n', type=int, default=1, help='nodes')
    parser.add_argument('--threads', '-t', type=int, default=4, help='threads')
    parser.add_argument('--log', '-l', type=str, default="log_out", help='log filename')
    parser.add_argument('--debug', '-d', type=str, action='store_true', help='To print commands (For testing flow). OPTIONAL')
    args = parser.parse_args()
    qsubr_job = qsubr.qsubr(script = args.script, threads = args.threads, nodes = args.nodes, mem = args.mem, name = args.name, debug=args.debug, cluster=args.cluster, log=args.log, user=args.account)
    qsubr.run_job()
