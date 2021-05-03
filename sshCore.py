from paramiko import SSHClient
from time import sleep


def initSSH():
    client = SSHClient()
    client.load_system_host_keys()
    client.load_host_keys('~/.ssh/known_hosts')
    # client.set_missing_host_key_policy(AutoAddPolicy())
    # client.look_for_keys(True)
    ip = '192.168.1.214'
    client.connect(ip, username='pi', passphrase='doc')
    sshCommand(client, 'cd EOG/SSHScripts')
    return client


def sshCommand(client, string):
    client.exec_command(string)
    print("executing ssh command: " + string)
    return


def motorControlSSH(client, setting):
    if setting == "Coarse":
        string = 'python3 pulseCoarse.py'
    elif setting == "Fine":
        string = 'python3 pulseCoarse.py'
    sshCommand(client, string)


def motorKillSSH(client):
    string = "python3 pulseKill.py"
    sshCommand(client, string)


def sshTest():
    SSH = initSSH()
    motorControlSSH(SSH, "Fine")
    sleep(5)
    motorKillSSH(SSH)
    sleep(5)
    motorControlSSH(SSH, "Coarse")
    sleep(5)
    motorKillSSH(SSH)


if __name__ == '__main__':
    sshTest()
