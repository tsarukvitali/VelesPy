
# Copyright 2019 Tsaruk Vitaly
# Licensed under the Apache License, Version 2.0


import argparse
import os
import paramiko
import re
import linecache
import subprocess
import multiprocessing
import shutil

path = os.path.dirname(os.path.realpath(__file__))
pattern = re.compile(r"\.log.*.txt")

def inkass_action():
    inkreg = [
        'unload from   cashbox', 'BOX 0 l', 'BOX 1 l', 'LCDM: e', 'BOX 0 - u', 'BOX 1 - u', 'LCDM: command \'44','bill end status',
        'LCDM box 0 blocked', 'LCDM box 1 blocked', 'answer: Timeout', 'sensor status', 'LCDM: read timeout', 'Counting error',
        'Motor stop status', 'SOL sensor', 'Pickup error', 'Over reject status', 'Reject tray is not recognized',
        ]
    inkassout1 = []
    inkassout2 = []
    for dirname, subdirs, files in os.walk(path):
        for file in files:
            if pattern.search(file):
                logged_in = os.path.join(dirname, file)
                with open(logged_in, encoding="utf-8") as logged:
                    for num, line in enumerate(logged):
                        for ext in inkreg[1:len(inkreg)]:
                            if ext in line:
                                inkassout1.append(re.sub(r'^[^\(]+\(', r'(', line))
                        for ext in inkreg[1:3]:
                            if ext in line:
                                for i in range((num+1),(num+18),1):
                                    inkassout2.append(re.sub(r'^[^\(]+\(', r'(', linecache.getline(logged_in, i)))
                        if inkreg[0] in line:
                            if num >19:
                                for i in range((num-19),(num+1),1):
                                    inkassout2.append(re.sub(r'^[^\(]+\(', r'(', linecache.getline(logged_in, i)))
    if not os.path.exists(path + '/output/'):
        os.makedirs(path + '/output/')
    inkass_file = path + '/output/inkass_output.txt'
    if os.path.isfile(inkass_file):
        os.remove(inkass_file)
    with open(inkass_file, 'w', encoding="utf-8") as inkass_file:
        with open('inkass_head', encoding="utf8") as inkass_head:
            inkasslegend = inkass_head.read()
            inkass_file.write(inkasslegend)
        inkass_file.write("\n\n\n")
        inkass_file.write("".join(sorted(inkassout1)))
        inkass_file.write("\n\n\n")
        inkass_file.write("".join(inkassout2))

def keno_action():
    keno = ['AddTicketButton', ' BD: ', ' BL ', ' BMA: ', 'BEGIN ']
    outkeno = []
    sdata = "(" + input("Enter start date(YYYY-MM-DD HH:MM): ")
    edata = "(" + input("Enter end date(YYYY-MM-DD HH:MM): ")
    f1data = "(1970-01-01 00:00"
    f2data = "(1970-01-01 00:10"
    for dirname, subdirs, files in os.walk(path):
        for file in files:
            if pattern.search(file):
                logged = os.path.join(dirname, file)
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
    with open(keno_file, 'w', encoding="utf-8") as keno_file:
        with open("keno_head", encoding="utf-8") as keno_head:
            kenolegend = keno_head.read()
            keno_file.write(kenolegend)
        keno_file.write("\n\n\n")
        keno_file.write("".join(outkeno))


def bur_action():
    bur = [
    'BD: EncAcceptorBtn ', 'Escrow command', 'Stacked complete', 'CCNet: error read answer',
    'BillAcceptor', 'initialize billacceptor on port', ' BD: 1', ' BD: 2', ' BD: 5',
    ]
    outbur1 = []
    outbur2 = []
    for dirname, subdirs, files in os.walk(path):
        for file in files:
            if pattern.search(file):
                logged_in = os.path.join(dirname, file)
                with open(logged_in) as logged:
                    for num, line in enumerate(logged):
                        for elem_bur in bur[1:len(bur)]:
                            if elem_bur in line:
                                outbur1.append(re.sub(r'^[^\(]+\(', r'(', line))
                        if bur[0] in line:
                            for i in range((num+1),(num+42),1):
                                outbur2.append(re.sub(r'^[^\(]+\(', r'(', linecache.getline(logged_in, i)))
    if not os.path.exists(path + '/output/'):
        os.makedirs(path + '/output/')
    bur_file = path + '/output/bur_output.txt'
    if os.path.isfile(bur_file):
        os.remove(bur_file)
    with open(bur_file, 'w', encoding="utf-8") as bur_file:
        with open("bur_head", encoding="utf-8") as bur_head:
            burlegend = bur_head.read()
            bur_file.write(burlegend)
        bur_file.write("\n\n\n")
        bur_file.write("".join(sorted(outbur1)))
        bur_file.write("\n\n\n")
        bur_file.write("".join(outbur2))

def balance_action():
    balance = [
        'total spin', 'BEGIN', ' BL ', ' RB: ', ' RW: ', ' TW: ', ' Balance ', 'LUA:', 'enter double',
        'opened', 'LCDM: e', 'BOX 0 - u', 'BOX 1 - u', 'SSP: dd ', 'paycenter', 'exit double',
        ]
    outbalance = []
    sdata = "(" + input("Enter start date(YYYY-MM-DD HH:MM): ")
    edata = "(" + input("Enter end date(YYYY-MM-DD HH:MM): ")
    f1data = "(1970-01-01 00:00"
    f2data = "(1970-01-01 00:10"
    for dirname, subdirs, files in os.walk(path):
        for file in files:
            if pattern.search(file):
                logged = os.path.join(dirname, file)
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
    with open(balance_file, 'w', encoding="utf-8") as balance_file:
        with open("balance_head", encoding="utf-8") as balance_head:
            balancelegend = balance_head.read()
            balance_file.write(balancelegend)
        balance_file.write("\n\n\n")
        balance_file.write("".join(outbalance))

def bill_action():
    bill = [
        'BD: EncAcceptorBtn ', 'Escrow command', 'Stacked command', 'BillAcceptor', ' BD: 2', ' BD: 1',
        ' BD: 4', ' BD: 5', 'Transport', 'jammed status', 'CCTALK: error read answer', 'billacceptor',
        ]
    outbill1 = []
    outbill2 = []
    for dirname, subdirs, files in os.walk(path):
        for file in files:
            if pattern.search(file):
                logged_in = os.path.join(dirname, file)
                with open(logged_in, encoding="utf-8") as logged:
                    for num, line in enumerate(logged):
                        for elem_bill in bill[1:len(bill)]:
                            if elem_bill in line:
                                outbill1.append(re.sub(r'^[^\(]+\(', r'(', line))
                        if bill[0] in line:
                            for i in range((num+1),(num+42),1):
                                outbill2.append(re.sub(r'^[^\(]+\(', r'(', linecache.getline(logged_in, i)))
    if not os.path.exists(path + '/output/'):
        os.makedirs(path + '/output/')
    bill_file = path + '/output/bill_output.txt'
    if os.path.isfile(bill_file):
        os.remove(bill_file)
    with open(bill_file, 'w', encoding="utf-8") as bill_file:
        with open("bill_head", encoding="utf-8") as bill_head:
            billlegend = bill_head.read()
            bill_file.write(billlegend)
        bill_file.write("\n\n\n")
        bill_file.write("".join(sorted(outbill1)))
        bill_file.write("\n\n\n")
        bill_file.write("".join(outbill2))


def cctalk_action():
    cctalk = ['CCTALK', ' cctalk']
    outcctalk = []
    for dirname, subdirs, files in os.walk(path):
        for file in files:
            if pattern.search(file):
                logged = os.path.join(dirname, file)
                with open(logged, encoding="utf-8") as logged:
                    for line in logged:
                        for elem_cctalk in cctalk:
                            if elem_cctalk in line:
                                outcctalk.append(re.sub(r'^[^\(]+\(', r'(', line))
    if not os.path.exists(path + '/output/'):
        os.makedirs(path + '/output/')
    cctalk_file = path + '/output/cctalk_output.txt'
    if os.path.isfile(cctalk_file):
        os.remove(cctalk_file)
    with open(cctalk_file, 'w', encoding="utf-8") as cctalk_file:
        cctalk_file.write("".join(outcctalk))


def lcdm_action():
    lcdm = ['LCDM']
    outlcdm = []
    for dirname, subdirs, files in os.walk(path):
        for file in files:
            if pattern.search(file):
                logged = os.path.join(dirname, file)
                with open(logged, encoding="utf-8") as logged:
                    for line in logged:
                        for elem_lcdm in lcdm:
                            if elem_lcdm in line:
                                outlcdm.append(re.sub(r'^[^\(]+\(', r'(', line))
    if not os.path.exists(path + '/output/'):
        os.makedirs(path + '/output/')
    lcdm_file = path + '/output/lcdm_output.txt'
    if os.path.isfile(lcdm_file):
        os.remove(lcdm_file)
    with open(lcdm_file, 'w', encoding="utf-8") as lcdm_file:
        lcdm_file.write("".join(outlcdm))


def ccnet_action():
    ccnet = ['CCNet']
    outccnet = []
    for dirname, subdirs, files in os.walk(path):
        for file in files:
            if pattern.search(file):
                logged = os.path.join(dirname, file)
                with open(logged, encoding="utf-8") as logged:
                    for line in logged:
                        if ccnet[0] in line:
                            outccnet.append(re.sub(r'^[^\(]+\(', r'(', line))
    if not os.path.exists(path + '/output/'):
        os.makedirs(path + '/output/')
    ccnet_file = path + '/output/ccnet_output.txt'
    if os.path.isfile(ccnet_file):
        os.remove(ccnet_file)
    with open(ccnet_file, 'w', encoding="utf-8") as ccnet_file:
        ccnet_file.write("".join(outccnet))


def connect_action(uuid):
    remotepath = "/raid/data/telemetry/" + uuid + "/*/platform*"
    if not os.path.exists(path + '/raw_log/'):
        os.makedirs(path + '/raw_log/')
    keyfile =str(path + '/key/key.pem')
    outpath = path + '/raw_log/logs.tar.gz'
    command = 'tar -czvf /tmp/logs.tar.gz ' + remotepath
    command2 = 'rm /tmp/logs.tar.gz'
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('54.216.225.233', username='root', key_filename=keyfile)
    stdin, stdout, stderr = ssh.exec_command(command)
    #print(stdin, '\n', stdout, '\n', stderr)
    sftp = ssh.open_sftp()
    sftp.get('/tmp/logs.tar.gz', outpath )
    print("logs.tar.gz downloaded")
    stdin, stdout, stderr = ssh.exec_command(command2)
    #print(stdin, '\n', stdout, '\n', stderr)
    sftp.close()
    ssh.close()
    shutil.unpack_archive(outpath, path + '/raw_log/')

def processFile(arglistloggedfile):
    decrypter = "decrypt_log"
    decrypterPath = os.path.join(path, decrypter)
    if not os.path.isfile(decrypterPath):
        decrypter2 = "decrypt_log.exe"
        decrypterPath2 = os.path.join(path, decrypter2)
        if not os.path.isfile(decrypterPath2):
            print ("can not find decrypter by path " + decrypterPath + " or " + decrypterPath2)
        else:
            decrypterPath = decrypterPath2
    unloggedName = os.path.basename(arglistloggedfile) + ".txt"
    loggeddir = path + '/log'
    unlogged = os.path.join(loggeddir, unloggedName)
    print (arglistloggedfile + " > " + unlogged)
    with open(unlogged, "w", encoding="utf-8") as outfile:
        subprocess.run([ decrypterPath, arglistloggedfile], stdout=outfile)

def unlog():
    unlogPattern = re.compile(r"(veksel\.log|platform\.log|watchdog\.log|updater\.log)[\.\d+]*$")
    if not os.path.exists(path + '/log/'):
        os.makedirs(path + '/log/')
    loggedFiles = []
    for dirname, subdirs, files in os.walk(path):
        for file in files:
            if unlogPattern.search(file):
                logged = os.path.join(dirname, file)
                loggedFiles.append(logged)
    p = multiprocessing.Pool(multiprocessing.cpu_count())
    p.map(processFile, loggedFiles)

def deldir():
    log = path + '/log/'
    output = path + '/output/'
    raw_log = path + '/raw_log/'
    if os.path.exists(log):
        shutil.rmtree(log)
    if os.path.exists(output):
        shutil.rmtree(output)
    if os.path.exists(raw_log):
        shutil.rmtree(raw_log)

def createzip(uuid):
    pathzip = path + '/log/'
    shutil.make_archive(uuid, 'zip', pathzip)

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
    parser.add_argument("-d", "--declog", nargs='?', const="0",
                        help="Log decoding")
    args = parser.parse_args()

    if args.inkass:
        print("Armenia collection problems")
        if args.inkass > "0":
            deldir()
            connect_action(args.inkass)
            unlog()
        inkass_action()
        if args.inkass > "0":
            createzip(args.inkass)
    if args.bill:
        print("Armenia billacceptor problems")
        if args.bill > "0":
            deldir()
            connect_action(args.bill)
            unlog()
        bill_action()
        if args.bill > "0":
            createzip(args.bill)
    if args.bur:
        print("Bur billacceptor problems")
        if args.bur > "0":
            deldir()
            connect_action(args.bur)
            unlog()
        bur_action()
        if args.bur > "0":
            createzip(args.bur)
    if args.balance:
        print("Player balance problem")
        if args.balance > "0":
            deldir()
            connect_action(args.balance)
            unlog()
        balance_action()
        if args.balance > "0":
            createzip(args.balance)
    if args.keno:
        print("Keno problem")
        if args.keno > "0":
            deldir()
            connect_action(args.keno)
            unlog()
        keno_action()
        if args.keno > "0":
            createzip(args.keno)
    if args.cctalk:
        print("CCTALK protocol")
        cctalk_action()
    if args.lcdm:
        print("LCDM protocol")
        lcdm_action()
    if args.ccnet:
        print("CCNET protocol")
        ccnet_action()
    if args.declog:
        print("Log decoding")
        if args.declog > "0":
            deldir()
            connect_action(args.declog)
        unlog()
        if args.declog > "0":
            createzip(args.declog)

if __name__ == "__main__":
    main()
