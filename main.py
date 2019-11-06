
# Copyright 2019 Tsaruk Vitaly
# Licensed under the Apache License, Version 2.0


import argparse
import os
import paramiko
import re
import linecache
import subprocess
import shutil

def inkass_action():
    path = os.path.dirname(os.path.realpath(__name__))
    pattern = re.compile(r"\.log.*.txt")
    inkreg = ['unload from   cashbox', 'BOX 0 l', 'BOX 1 l', 'LCDM: e', 'BOX 0 - u', 'BOX 1 - u', 'LCDM: command \'44', 'bill end status', 'LCDM box 0 blocked', 'LCDM box 1 blocked', 'answer: Timeout', 'sensor status', 'LCDM: read timeout', 'Counting error', 'Motor stop status', 'SOL sensor', 'Pickup error', 'Over reject status', 'Reject tray is not recognized' ]
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
    if not os.path.exists(path + '/output/'):
        os.makedirs(path + '/output/')
    inkass_file = path + '/output/inkass_output.txt'
    if os.path.isfile(inkass_file):
        os.remove(inkass_file)
        f1 = sorted(f1)
    with open(inkass_file, 'w') as inkass_file:
        with open('inkass_head') as f3:
            kenolegend = f3.read()
            inkass_file.write(kenolegend)
        inkass_file.write("\n\n\n")
        inkass_file.write("".join(f1))
        inkass_file.write("\n\n\n")
        inkass_file.write("".join(f2))

def keno_action():
    path = os.path.dirname(os.path.realpath(__name__))
    pattern = re.compile(r"\.log.*.txt")
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
    keno_file = path + '/output/keno_output.txt'
    if os.path.isfile(keno_file):
        os.remove(keno_file)
    with open(keno_file, 'w') as keno_file:
        with open("keno_head") as f3:
            kenolegend = f3.read()
            keno_file.write(kenolegend)
        keno_file.write("\n\n\n")
        keno_file.write("".join(outkeno))


def bur_action():
    path = os.path.dirname(os.path.realpath(__name__))
    pattern = re.compile(r"\.log.*.txt")
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
    bur_file = path + '/output/bur_output.txt'
    if os.path.isfile(bur_file):
        os.remove(bur_file)
    f1 = sorted(f1)
    with open(bur_file, 'w') as bur_file:
        with open("bur_head") as f3:
            burlegend = f3.read()
            bur_file.write(burlegend)
        bur_file.write("\n\n\n")
        bur_file.write("".join(f1))
        bur_file.write("\n\n\n")
        bur_file.write("".join(f2))

def balance_action():
    path = os.path.dirname(os.path.realpath(__name__))
    pattern = re.compile(r"\.log.*.txt")
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
    balance_file = path + '/output/balance_output.txt'
    with open(balance_file, 'w') as balance_file:
        with open("balance_head") as f1:
            balancelegend = f1.read()
            balance_file.write(balancelegend)
        balance_file.write("\n\n\n")
        balance_file.write("".join(outbalance))

def bill_action():
    path = os.path.dirname(os.path.realpath(__name__))
    pattern = re.compile(r"\.log.*.txt")
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
    bill_file = path + '/output/bill_output.txt'
    if os.path.isfile(bill_file):
        os.remove(bill_file)
    f1 = sorted(f1)
    with open(bill_file, 'w') as bill_file:
        with open("bill_head") as f3:
            billlegend = f3.read()
            bill_file.write(billlegend)
        bill_file.write("\n\n\n")
        bill_file.write("".join(f1))
        bill_file.write("\n\n\n")
        bill_file.write("".join(f2))


def cctalk_action():
    path = os.path.dirname(os.path.realpath(__name__))
    pattern = re.compile(r"\.log.*.txt")
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
    cctalk_file = path + '/output/cctalk_output.txt'
    if os.path.isfile(cctalk_file):
        os.remove(cctalk_file) 
    with open(cctalk_file, 'w') as cctalk_file:
        cctalk_file.write("".join(outcctalk))


def lcdm_action():
    path = os.path.dirname(os.path.realpath(__name__))
    pattern = re.compile(r"\.log.*.txt")
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
    lcdm_file = path + '/output/lcdm_output.txt'
    if os.path.isfile(lcdm_file):
        os.remove(lcdm_file) 
    with open(lcdm_file, 'w') as lcdm_file:
        lcdm_file.write("".join(outlcdm))


def ccnet_action():
    path = os.path.dirname(os.path.realpath(__name__))
    pattern = re.compile(r"\.log.*.txt")
    ccnet = ['CCNet']
    outccnet = [] 
    for subdir, dirs, files in os.walk(path):
        for file in files:
            if pattern.search(file):
                logged = os.path.join(subdir, file)
                with open(logged) as logged: 
                    for line in logged:                                       
                        if ccnet[0] in line:
                            outccnet.append(re.sub(r'^[^\(]+\(', r'(', line))
    if not os.path.exists(path + '/output/'):
        os.makedirs(path + '/output/')
    ccnet_file = path + '/output/ccnet_output.txt'
    if os.path.isfile(ccnet_file):
        os.remove(ccnet_file)                            
    with open(ccnet_file, 'w') as ccnet_file:
        ccnet_file.write("".join(outccnet))


def connect_action(uuid):
    remotepath = "/raid/data/telemetry/" + uuid + "/*/platform*"
    path = os.path.dirname(os.path.realpath(__name__))
    if not os.path.exists(path + '/raw_log/'):
        os.makedirs(path + '/raw_log/')
    keyfile =str(path + '/key/key.pem')
    outpath = path + '/raw_log/logs.tar.gz'
    command = 'tar -czvf /tmp/logs.tar.gz ' + remotepath 
    command2 = 'rm /tmp/logs.tar.gz'
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('54.93.125.153', username='ubuntu', key_filename=keyfile)
    stdin, stdout, stderr = ssh.exec_command(command)
    print(stdin, '\n', stdout, '\n', stderr)
    sftp = ssh.open_sftp()
    sftp.get('/tmp/logs.tar.gz', outpath )
    stdin, stdout, stderr = ssh.exec_command(command2)
    print(stdin, '\n', stdout, '\n', stderr)
    sftp.close()
    ssh.close()

    shutil.unpack_archive(outpath, path + '/raw_log/') 
    
    r'''
    if [ -n "$2" ]
    then
    mkdir -p log
    scp -i "key.pem" -r root@54.216.225.233:/raid/data/telemetry/"$2"/*/platform* ./log/
    python3 unlog.py
    case_action "$1" 
    zip "$2".zip ./log/*.txt
    else
    case_action "$1" 
    zip log.zip ./log/*.txt
    fi'''

def unlog():
    rootdir = os.path.dirname(os.path.realpath(__name__))
    decrypter = "decrypt_log"
    decrypterPath = os.path.join(rootdir, decrypter)
    if not os.path.isfile(decrypterPath):
        decrypter2 = "decrypt_log.exe"
        decrypterPath2 = os.path.join(rootdir, decrypter2)
        if not os.path.isfile(decrypterPath2):
            print ("can not find decrypter by path " + decrypterPath + " or " + decrypterPath2)
        else:
            decrypterPath = decrypterPath2
    pattern = re.compile("\.log[\.\d+]*$")
    loggeddir = rootdir + '/log'
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if pattern.search(file):
                logged = os.path.join(subdir, file)
                unloggedName = file + ".txt"
                unlogged = os.path.join(loggeddir, unloggedName)
                #subprocess.call(["C:/Documents and Settings/flow_model/flow.exe"])
                print (logged + " > " + unlogged)
                with open(unlogged, "w") as outfile:
                    subprocess.run([ decrypterPath, logged], stdout=outfile)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-1", "--inkass", nargs='?', const="0",
                        help="Armenia collection problems")
    parser.add_argument("-2", "--bill", nargs='?', const="0",
                        help="Armenia billacceptor problems")
    parser.add_argument("-3", "--bur", nargs='?', const="0",
                        help="Bur billacceptor problems")
    parser.add_argument("-4", "--balance", nargs='?', const="0",
                        help="Player balance problem")
    parser.add_argument("-5", "--keno", nargs='?', const="0",
                        help="Keno problem")
    parser.add_argument("-6", "--cctalk", action="store_true",
                        help="CCTALK protocol")
    parser.add_argument("-7", "--lcdm", action="store_true",
                        help="LCDM protocol")
    parser.add_argument("-8", "--ccnet", action="store_true",
                        help="CCNET protocol")
    args = parser.parse_args()

    if args.inkass:
        print("Armenia collection problems")
        if args.inkass > "0":
            connect_action(args.inkass)
        unlog()
        inkass_action()
    if args.bill:
        print("Armenia billacceptor problems")
        if args.bill > "0":
            connect_action(args.bill)
        bill_action()
    if args.bur:
        print("Bur billacceptor problems")
        if args.bur > "0":
            connect_action(args.bur)
        bur_action()
    if args.balance:
        print("Player balance problem")
        if args.balance > "0":
            connect_action(args.balance)
        balance_action()
    if args.keno:
        print("Keno problem")
        if args.keno > "0":
            connect_action(args.keno)
        keno_action()
    if args.cctalk:
        print("CCTALK protocol")
        cctalk_action()
    if args.lcdm:
        print("LCDM protocol")
        lcdm_action()
    if args.ccnet:
        print("CCNET protocol")
        ccnet_action()


if __name__ == "__main__":
    main()
