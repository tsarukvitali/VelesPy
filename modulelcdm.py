#! python3

import os
import re
import linecache

path = os.path.dirname(os.path.realpath(__file__))
pattern = re.compile(r"\.txt")
lcdm = ['LCDM']
outlcdm = [] 

for subdir, dirs, files in os.walk(path):
    for file in files:
        if pattern.search(file):
            logged = os.path.join(subdir, file)
            with open(logged) as logged: 
                for line in logged:
                    for elem_lcdm in lcdm:                       
                        if elem_lcdm in line:
                            outlcdm.append(re.sub(r'^[^\(]+\(', r'(', line))                            

if not os.path.exists(path + '/output/'):
    os.makedirs(path + '/output/')

with open(path + '/output/LCDM.txt', 'w') as out:
    out.write("".join(outlcdm))
    









