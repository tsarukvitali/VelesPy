#! python3

import os
import re
import linecache

path = os.path.dirname(os.path.realpath(__file__))
pattern = re.compile(r"\.txt")
cctalk = ['CCTALK', ' cctalk']
outcctalk = [] 

for subdir, dirs, files in os.walk(path):
    for file in files:
        if pattern.search(file):
            logged = os.path.join(subdir, file)
            with open(logged) as logged: 
                for line in logged:
                    for elem_cctalk in cctalk:                       
                        if elem_cctalk in line:
                            outcctalk.append(re.sub(r'^[^\(]+\(', r'(', line))                            

if not os.path.exists(path + '/output/'):
    os.makedirs(path + '/output/')

with open(path + '/output/CCTALK.txt', 'w') as out:
    out.write("".join(outcctalk))
    









