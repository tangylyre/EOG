from paramiko import SSHClient
from eogCore import *


def initSSH():
    client = SSHClient()
    # client.load_system_host_keys()
    # client.load_host_keys('~/.ssh/known_hosts')
    # client.set_missing_host_key_policy(AutoAddPolicy())
    client.look_for_keys(True)
    ip = '192.168.1.214'
    client.connect(ip, username='pi', passphrase='doc')
    sshCommand(client, 'cd EOG')
    return client


def sshCommand(client, string):
    client.exec_command(string)
    print("executing ssh command: " + string)
    return


def motorInitSSH(client):
    string = "motorInit()"
    sshCommand(client, string)


def motorControlSSH(client, setting):
    string = "motorControl(" + setting + ')'
    sshCommand(client, string)


def motorKillSSH(client):
    string = "motorKill()"
    sshCommand(client, string)
