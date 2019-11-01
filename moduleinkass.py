#! python3

import os
import re
import linecache

path = os.path.dirname(os.path.realpath(__file__))
pattern = re.compile(r"\.txt")
inkreg = ['unload from   cashbox', 'BOX 0 l', 'BOX 1 l', 'LCDM: e', 'BOX 0 - u', 'BOX 1 - u', 'LCDM: command \'44', 'bill end status', 'LCDM box 0 blocked', 'LCDM box 1 blocked', 'answer: Timeout', 'sensor status', 'LCDM: read timeout', 'Counting error', 'Motor stop status', 'SOL sensor', 'Pickup error', 'Over reject status', 'Reject tray is not recognized' ]
#delink = ['CCTALK', 'Cashe Dispenser', 'LCDM: write to port', 'VKP80II' ]
f1 = [] 
f2 = []
for subdir, dirs, files in os.walk(path):
    for file in files:
        if pattern.search(file):
            logged_in = os.path.join(subdir, file)
            with open(logged_in) as logged: 
                for num, line in enumerate(logged):
                    for ext in inkreg[1:len(inkreg)]:                       
                        if ext in line:
                            f1.append(re.sub(r'^[^\(]+\(', r'(', line))
                    for ext in inkreg[1:3]:
                        if ext in line:
                            for i in range((num+1),(num+18),1):
                                f2.append(re.sub(r'^[^\(]+\(', r'(', linecache.getline(logged_in, i)))
                    if inkreg[0] in line:
                        if num >19:
                            for i in range((num-19),(num+1),1):
                                f2.append(re.sub(r'^[^\(]+\(', r'(', linecache.getline(logged_in, i)))

#for ext2 in delink:
#if ext2 not in linecache.getline(logged_in, i):
f1 = sorted(f1)
with open('output.txt', 'w') as f3:
    f3.write("".join(f1))
    f3.write("\n\n\n")
    f3.write("".join(f2))










