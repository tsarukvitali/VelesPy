#! python3

import os
import paramiko 

tid = str(6000739) 
remotepath = "/raid/data/telemetry/" + tid + "/*/platform*"
path = os.path.dirname(os.path.realpath(__file__))
if not os.path.exists(path + '/raw_log/'):
    os.makedirs(path + '/raw_log/')
keyfile =str(path + '/key/key.pem')
outpath = path + '/raw_log/logs.tar.gz'
command = 'tar -czvf /tmp/logs.tar.gz ' + remotepath 
command2 = 'rm /tmp/logs.tar.gz'
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('54.93.125.153', username='ubuntu', key_filename=keyfile)
stdin, stdout, stderr = ssh.exec_command(command)
sftp = ssh.open_sftp()
sftp.get('/tmp/logs.tar.gz', outpath )
stdin, stdout, stderr = ssh.exec_command(command2)
ssh.close()









