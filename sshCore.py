from paramiko import *
from time import sleep


# this set of methods provides a means to streamline ssh communications from EOG unit to vibrator unit.

def initSSH():
    # establishes a connection to the other raspi, returns the connection (client) object.
    # i hardcoded the IP and credentials, will require tweaking when you connect to another wifi source.
    client = SSHClient()
    client.load_system_host_keys()
    # client.load_host_keys('~/.ssh/known_hosts')
    client.set_missing_host_key_policy(AutoAddPolicy())
    # client.look_for_keys(True)
    ip = '192.168.1.214'
    client.connect(ip, username='pi', passphrase='doc', password='doc', pkey=None)
    return client


def sshCommand(client, string):
    # this function processes a string and feeds it into ssh command.
    # returns function call status for debugging.
    stdin, stdout, stderr = client.exec_command(string)
    print("executing ssh command: " + string)
    return {'out': stdout.readlines(),
            'err': stderr.readlines(),
            'retval': stdout.channel.recv_exit_status()}


def motorControlSSH(client, setting):
    # utilizes sshCommand to calll different scripts in the vibration unit environment. note that the directory for
    # these scripts are hardcoded and may need to be tweaked if you manipulate the repository.
    if setting == "Coarse":
        string = 'python3 /home/pi/EOG/SSHScripts/pulseCoarse.py'
    elif setting == "Fine":
        string = 'python3 /home/pi/EOG/SSHScripts/pulseFine.py'
    print(sshCommand(client, string))


def motorKillSSH(client):
    # utilizes sshCommand to call different scripts in the vibration unit environment. note that the directory for
    # these scripts are hardcoded and may need to be tweaked if you manipulate the repository.
    string = "python3 /home/pi/EOG/SSHScripts/pulseKill.py"
    print(sshCommand(client, string))


def sshTest():
    # runs all the above functions to test if ssh connection si working.
    SSH = initSSH()
    print(sshCommand(SSH, 'pwd'))
    print(sshCommand(SSH, 'ls'))
    motorControlSSH(SSH, "Fine")
    sleep(5)
    motorKillSSH(SSH)
    sleep(5)
    motorControlSSH(SSH, "Coarse")
    sleep(5)
    motorKillSSH(SSH)


if __name__ == '__main__':
    sshTest()
