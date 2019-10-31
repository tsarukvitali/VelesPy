#! python3

import os
import re
import linecache

path = os.path.dirname(__file__)

pattern = re.compile(r"\.txt")
inkreg = ['BOX 0 l', 'BOX 1 l', 'LCDM: e', 'BOX 0 - u', 'BOX 1 - u', 'LCDM: command \'44', 'bill end status', 'LCDM box 0 blocked', 'LCDM box 1 blocked', 'answer: Timeout', 'sensor status', 'LCDM: read timeout', 'Counting error', 'Motor stop status', 'SOL sensor', 'Pickup error', 'Over reject status', 'Reject tray is not recognized' ]
f1 = [] 
for subdir, dirs, files in os.walk(path):
    for file in files:
        if pattern.search(file):
            logged_in = os.path.join(subdir, file)
            #with open('output.txt', 'a') as f1:                          
            with open(logged_in) as logged:
                #lines = list(logger)
                for num, line in enumerate(logged):
                    for ext in inkreg[2:len(inkreg)]:                       
                        if ext in line:                                
                            #f1.write(re.sub(r'^[^\(]+\(', r'(', line)) 
                            f1.append(re.sub(r'^[^\(]+\(', r'(', line))
                    for ext in inkreg[:2]:
                        if ext in line:
                            for i in range((num+1),(num+18),1):
                                #print(logged_in)
                                f1.append(re.sub(r'^[^\(]+\(', r'(', linecache.getline(logged_in, i)))
with open('output.txt', 'w') as f2:
    f2.write("".join(f1))








