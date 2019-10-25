#!/bin/bash

#Copyright 2019 Tsaruk Vitaly
#Licensed under the Apache License, Version 2.0


display_help() {
    echo "Usage: $0 [option...]" >&2
    echo
    echo "    1,  {--inkass}   Armenia collection problems "
    echo "    2,  {--bill}     Armenia billacceptor problems "
    echo "    3,  {--bur}      Bur billacceptor problems   "
    echo "    4,  {--balance}  balance player problems "
    echo "    5,  {--keno}     problems in game keno  "
    echo "    6,  {--cctalk}   protocol CCTALK "
    echo "    7,  {--lcdm}     protocol LCDM "
    echo "    8,  {--ccnet}    protocol CCNET  "
    echo
    exit 1
}

inkass_action() {
    inkasslegend=$(<inkass_head)
    
    inkass_file="./inkass.txt"
    if [ -f $inkass_file ] ; then
        rm $inkass_file
    fi
    
    findvariable=$(mktemp)
    sortstrings=$(mktemp)
    snumberf=$(mktemp)
    delstrings=$(mktemp)
    egrep -sr 'BOX [0-1] l|LCDM: e|BOX [0-1] - u|LCDM: command .44|bill end status|LCDM box [0-1] blocked|answer: Timeout|sensor status|LCDM: read timeout|Counting error|Motor stop status|SOL sensor|Pickup error|Over reject status|Reject tray is not recognized' log/ | sed -r 's!(^[^\(]+\()!(!g' >> "$findvariable" 
    sort --output="$sortstrings" "$findvariable"
    snumber=$(grep -n "BOX [0-1] l" "$sortstrings" | cut -f1 -d:) 
    echo "$snumber" >> "$snumberf"
    numberoflines=$(wc -l "$snumberf" | cut -f1 -d\ )
    if [ "$numberoflines" == "2" ]; then
        firstline=$(head -n 1 "$snumberf")
        endline=$(tail -n 1 "$snumberf")
        sed ''"$endline"',$d' "$sortstrings" >> "$delstrings"
        echo "$inkasslegend" >> $inkass_file
        sed '1,'"$firstline"'d' "$delstrings" >> $inkass_file
    else
        echo "$inkasslegend" >> $inkass_file
        cat "$sortstrings" >> $inkass_file
    fi
    for file in ./log/*
    do
        grep -sA 17 'BOX [0-1] l' "$file" >> $inkass_file 
        grep -sB 20 'unload from   cashbox' "$file" >> $inkass_file 
    done
}

keno_action() {
    kenolegend=$(<keno_head)
    
    keno_file="./keno.txt"
    if [ -f $keno_file ] ; then
        rm $keno_file
    fi
    
    findvariable=$(mktemp)
    delstrings=$(mktemp)
    egrep -sr ' BD: | BL | BMA: |BEGIN' log/ | sed -r 's!(^[^\(]+\()!(!g' >> "$findvariable"
    echo -n "Enter start date(YYYY-MM-DD HH:MM): "
    read sdata
    echo -n "Enter end date(YYYY-MM-DD HH:MM): "
    read edata
    sdata="(${sdata}"
    edata="(${edata}"
    f1data=$(echo \(1970-01-01 00:00)
    f2data=$(echo \(1970-01-01 00:10)
    echo "$kenolegend" >> $keno_file
    while read LINE; do
        if [[ ("$sdata" < "$LINE" && "$LINE" < "$edata") || ( "$f1data" < "$LINE" && "$LINE" < "$f2data") ]]; then
            echo "$LINE" >> "$delstrings"
        fi
    done < "$findvariable"
    grep -v "AddTicketButton" "$delstrings" >> $keno_file
}

bur_action() {
    burlegend=$(<bur_head)
    
    bur_file="./bur.txt"
    if [ -f $bur_file ] ; then
        rm $bur_file
    fi
    
    findvariable=$(mktemp)
    sortstrings=$(mktemp)
    egrep -sr 'Escrow command|Stacked complete|BillAcceptor|CCNet: error read answer|initialize billacceptor on port| BD: 1| BD: 2| BD: 5' log/ | sed -r 's!(^[^\(]+\()!(!g' >> "$findvariable"
    sort --output="$sortstrings" "$findvariable"
    echo "$burlegend" >> $bur_file
    echo >> $bur_file
    cat "$sortstrings" >> $bur_file
    for file in ./log/*
    do
        grep -sA 41 'BD: EncAcceptorBtn ' "$file" >> $bur_file
    done
}

balance_action() {
    balancelegend=$(<balance_head)
    balance_file="./balance.txt"
    
    if [ -f $balance_file ] ; then
        rm $balance_file
    fi
    
    findvariable=$(mktemp)
    delstrings=$(mktemp)
    egrep -sr 'BillAcceptor|total spin|SpinTotal|BEGIN| BL | RB: | RW: | TW: | Balance |LUA:|enter double|opened|LCDM: e|BOX [0-1] - u|SSP: dd |paycenter|exit double' log/ | sed -r 's!(^[^\(]+\()!(!g' >> "$findvariable"
    echo -n "Enter start date(YYYY-MM-DD HH:MM): "
    read sdata
    echo -n "Enter end date(YYYY-MM-DD HH:MM): "
    read edata
    sdata="(${sdata}"
    edata="(${edata}"
    f1data=$(echo \(1970-01-01 00:00)
    f2data=$(echo \(1970-01-01 00:10)
    echo "$balancelegend" >> $balance_file
    echo >> $balance_file
    while read LINE; do
        if [[ ("$sdata" < "$LINE" && "$LINE" < "$edata") || ( "$f1data" < "$LINE" && "$LINE" < "$f2data") ]]; then
            echo "$LINE" >> "$delstrings"
        fi
    done < "$findvariable"
    cat "$delstrings" >>$balance_file
}


bill_action() {
    billlegend=$(<bill_head)
    
    bill_file="./bill.txt"
    if [ -f $bill_file ] ; then
        rm $bill_file
    fi
    
    findvariable=$(mktemp)
    sortstrings=$(mktemp)
    egrep -sr 'Escrow command|Stacked command|BillAcceptor| BD: 2| BD: 1| BD: 2| BD: 5|Transport|jammed status|CCTALK: error read answer|billacceptor' log/ | sed -r 's!(^[^\(]+\()!(!g' >> "$findvariable"
    sort --output="$sortstrings" "$findvariable"
    echo "$billlegend" >> $bill_file
    echo >> $bill_file
    cat "$sortstrings" >> $bill_file
    for file in ./log/*
    do
        grep -sA 45 'BD: EncAcceptorBtn ' "$file" >> $bill_file
    done
}


case_action(){
case $1 in
    1 | --inkass) inkass_action
        code inkass.txt
    ;;
    2 | --bill) bill_action
        code bill.txt
    ;;
    3 | --bur) bur_action
        code bur.txt
    ;;
    4 | --balance) balance_action
        code balance.txt
    ;;
    5 | --keno) keno_action
        code keno.txt
    ;;
    6 | --cctalk) egrep -sr 'CCTALK| cctalk' log/ | sed -r 's!(^[^\(]+\()!(!g' >>cctalk.txt
    ;;
    7 | --lcdm) egrep -sr 'LCDM' log/ | sed -r 's!(^[^\(]+\()!(!g' >>LCDM.txt
    ;;
    8 | --ccnet) egrep -sr 'CCNET' log/ | sed -r 's!(^[^\(]+\()!(!g' >>CCNET.txt
    ;;
    -h | --help) display_help
    ;;
    9 ) echo "Yes, Vlad has nine fingers:)"
    ;;
    *) echo "$1 is not an option. Please use $0 --help"
        exit 1
    ;;
esac
}

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
fi







