#! python3

import os
import re
import linecache

path = os.path.dirname(os.path.realpath(__file__))
pattern = re.compile(r"\.txt")
keno = ['AddTicketButton', ' BD: ', ' BL ', ' BMA: ', 'BEGIN ']
outkeno = [] 
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
                    for elem_keno in keno[1:len(keno)]:                       
                        if elem_keno in line:
                            tmpcutline = re.sub(r'^[^\(]+\(', r'(', line)
                            if (sdata < tmpcutline and tmpcutline < edata) or ( f1data < tmpcutline and tmpcutline < f2data):
                                if keno[0] not in tmpcutline:
                                    outkeno.append(tmpcutline)

if not os.path.exists(path + '/output/'):
    os.makedirs(path + '/output/')

with open(path + '/output/keno.txt', 'w') as out:
    out.write("".join(outkeno))
    









