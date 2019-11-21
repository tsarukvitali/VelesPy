#! python3

import os
import re
import linecache

path = os.path.dirname(os.path.realpath(__file__))
pattern = re.compile(r"\.txt")
balance = ['BillAcceptor', 'total spin', 'SpinTotal', 'BEGIN', ' BL ', ' RB: ', ' RW: ', ' TW: ', ' Balance ', 'LUA:', 'enter double', 'opened', 'LCDM: e', 'BOX 0 - u', 'BOX 1 - u', 'SSP: dd ', 'paycenter', 'exit double']
outbalance = [] 
sdata = "(" + input("Enter start date(YYYY-MM-DD HH:MM): ")
edata = "(" + input("Enter end date(YYYY-MM-DD HH:MM): ")
f1data = "(1970-01-01 00:00"
f2data = "(1970-01-01 00:10"

for subdir, dirs, files in os.walk(path):
    for file in files:
        if pattern.search(file):
            logged = os.path.join(subdir, file)
            with open(logged) as logged: 
                for line in logged:
                    for elem_balance in balance:                       
                        if elem_balance in line:
                            tmpcutline = re.sub(r'^[^\(]+\(', r'(', line)
                            if (sdata < tmpcutline and tmpcutline < edata) or ( f1data < tmpcutline and tmpcutline < f2data):
                                outbalance.append(tmpcutline)

if not os.path.exists(path + '/output/'):
    os.makedirs(path + '/output/')

with open(path + '/output/balance.txt', 'w') as out:
    out.write("".join(outbalance))
    









