#! python3

import os
import re
import linecache

path = os.path.dirname(__file__)
pattern = re.compile(r"\.txt")
bill = ['BD: EncAcceptorBtn ', 'Escrow command', 'Stacked command', 'BillAcceptor', ' BD: 2', ' BD: 1', ' BD: 4', ' BD: 5', 'Transport', 'jammed status', 'CCTALK: error read answer', 'billacceptor']
f1 = [] 
f2 = []
for subdir, dirs, files in os.walk(path):
    for file in files:
        if pattern.search(file):
            logged_in = os.path.join(subdir, file)
            with open(logged_in) as logged: 
                for num, line in enumerate(logged):
                    for elem_bill in bill[1:len(bill)]:                       
                        if elem_bill in line:
                            f1.append(re.sub(r'^[^\(]+\(', r'(', line))
                    if bill[0] in line:
                        for i in range((num+1),(num+42),1):                                
                            f2.append(re.sub(r'^[^\(]+\(', r'(', linecache.getline(logged_in, i)))
if not os.path.exists(path + '/output/'):
    os.makedirs(path + '/output/')

f1 = sorted(f1)
with open(path + '/output/bill.txt', 'w') as f3:
    f3.write("".join(f1))
    f3.write("\n\n\n")
    f3.write("".join(f2))









