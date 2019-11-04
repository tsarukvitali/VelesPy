#! python3

import os
from fabric import Connection  # pip3 install fabric

path = os.path.dirname(os.path.realpath(__file__))
if not os.path.exists(path + '/raw_log/'):
    os.makedirs(path + '/raw_log/')
with Connection(host="54.216.225.233",
                user="root",
                connect_kwargs={"key_filename": path + "/key/key.pem"}
                ) as c:
    c.get('/raid/data/telemetry/6000407/')



