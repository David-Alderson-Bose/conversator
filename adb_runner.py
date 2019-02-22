#!/usr/bin/env python3

import sys
if not sys.platform.startswith('java'):
    print('This utility requires Jython!')
    sys.exit(1)

import paramiko
from coroutine import coroutine



@coroutine
def run_ssh_commands(username, hostname, password=None, port=22):
    # TODO: Should have some sort of exception handling??
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy)
    client.connect(hostname, port=port, username=username, password=password)
    
    try:
        while True:
            cmd = (yield)
            print('\nrunning cmd: {}'.format(cmd))
            stdin, stdout, stderr = client.exec_command(cmd)
            error_raw = stderr.read().decode('utf-8')
            response_raw = stdout.read().decode('utf-8')
            if error_raw:
                print('Errors from {}: {}'.format(cmd, error_raw.splitlines()))
            if response_raw:
                response = response_raw.splitlines()
                print('Response from {}:'.format(cmd)) 
                for r in response_raw.splitlines():
                    print(r)
    except GeneratorExit:  # caller closed coroutine
        print('\nI GOT CLOSED')
    finally:
        client.close()



if __name__== "__main__":

    
    if len(sys.argv) < 4:
        print("args missing")
        sys.exit(1)

    username = sys.argv[1]
    hostname = sys.argv[2]
    password = sys.argv[3]
    linux_box_ssh = run_ssh_commands(username, hostname, password)
    
    # loop over commands
    for cmd in ['ls', 'ifconfig', 'echo HI MOM', 'galfarple THIS SHOULD ERROR']:
        linux_box_ssh.send(cmd)
    linux_box_ssh.close()

    print('so long!')

#    #command  = sys.argv[4]
#    
#
#    
#    try:
#        client = paramiko.SSHClient()
#        client.load_system_host_keys()
#        client.set_missing_host_key_policy(paramiko.WarningPolicy)
#        client.connect(hostname, port=port, username=username, password=password)
#    
#        stdin, stdout, stderr = client.exec_command(command)
#        result = stdout.read().decode('utf-8').splitlines()
#        for r in result:
#            print(r)
#    
#    finally:
#        client.close()
