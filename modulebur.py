#! python3

import os
import re
import linecache

path = os.path.dirname(__file__)
pattern = re.compile(r"\.txt")
bur = ['BD: EncAcceptorBtn ', 'Escrow command', 'Stacked complete', 'BillAcceptor', 'CCNet: error read answer', 'initialize billacceptor on port', ' BD: 1', ' BD: 2', ' BD: 5']
f1 = [] 
f2 = []
for subdir, dirs, files in os.walk(path):
    for file in files:
        if pattern.search(file):
            logged_in = os.path.join(subdir, file)
            with open(logged_in) as logged: 
                for num, line in enumerate(logged):
                    for elem_bur in bur[1:len(bur)]:                       
                        if elem_bur in line:
                            f1.append(re.sub(r'^[^\(]+\(', r'(', line))
                    if bur[0] in line:
                        for i in range((num+1),(num+42),1):                                
                            f2.append(re.sub(r'^[^\(]+\(', r'(', linecache.getline(logged_in, i)))
if not os.path.exists(path + '/output/'):
    os.makedirs(path + '/output/')

f1 = sorted(f1)
with open(path + '/output/bur.txt', 'w') as f3:
    f3.write("".join(f1))
    f3.write("\n\n\n")
    f3.write("".join(f2))









