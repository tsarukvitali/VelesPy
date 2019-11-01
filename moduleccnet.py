#! python3

import os
import re
import linecache

path = os.path.dirname(os.path.realpath(__file__))
pattern = re.compile(r"\.log.*.txt")
ccnet = ['CCNet']
outccnet = [] 
for subdir, dirs, files in os.walk(path):
    for file in files:
        if pattern.search(file):
            print(file)
            logged = os.path.join(subdir, file)
            with open(logged) as logged: 
                for line in logged:                                       
                    if ccnet[0] in line:
                        outccnet.append(re.sub(r'^[^\(]+\(', r'(', line))                            

if not os.path.exists(path + '/output/'):
    os.makedirs(path + '/output/')

with open(path + '/output/ccnet.txt', 'w') as out:
    out.write("".join(outccnet))
    









