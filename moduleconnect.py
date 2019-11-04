#! python3

import os
import paramiko 

tid = str(6000739) 
remotepath = "/raid/data/telemetry/" + tid + "/*/platform*"
path = os.path.dirname(os.path.realpath(__file__))
if not os.path.exists(path + '/raw_log/'):
    os.makedirs(path + '/raw_log/')
keyfile =str(path + '/key/key.pem')
outpath = path + '/raw_log/log.gz'
print(keyfile)
command = 'gzip -c ' + remotepath + ' >> /tmp/log.gz'
print(command)
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('54.93.125.153', username='ubuntu', key_filename=keyfile)

stdin, stdout, stderr = ssh.exec_command(command)
sftp = ssh.open_sftp()
sftp.get('/tmp/log.gz', outpath )
ssh.close()









