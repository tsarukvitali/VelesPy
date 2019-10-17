#!/bin/bash

#Copyright 2019 Tsaruk Vitaly
#Licensed under the Apache License, Version 2.0 

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
    egrep -r 'BOX [0-1] l|LCDM: e|BOX [0-1] - u|bill end status|LCDM box [0-1] blocked|answer: Timeout|sensor status|LCDM: read timeout|Counting error|Motor stop status|SOL sensor|Pickup error|Over reject status|Reject tray is not recognized' log/ | sed -r 's!(^[^\(]+\()!(!g' >> $findvariable
    sort --output=$sortstrings $findvariable
    snumber=$(grep -n "BOX [0-1] l" $sortstrings | cut -f1 -d:)
    echo "$snumber" >> $snumberf
    numberoflines=$(wc -l $snumberf | cut -f1 -d\ )
    if [ "$numberoflines" == "2" ]; then
        firstline=$(head -n 1 "$snumberf")
        endline=$(tail -n 1 "$snumberf")
        sed ''$endline',$d' $sortstrings >> $delstrings
        echo "$inkasslegend" >> $inkass_file
        sed '1,'$firstline'd' $delstrings >> $inkass_file
    else
        echo "$inkasslegend" >> $inkass_file
        echo $(<"$sortstrings") >> $inkass_file
    fi
    for file in ./log/*
    do
        grep -A 17 'BOX [0-1] l' $file >> $inkass_file
        grep -B 20 'unload from   cashbox' $file >> $inkass_file
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
    egrep -r ' BD: | BL | BMA: |BEGIN' log/ | sed -r 's!(^[^\(]+\()!(!g' >> $findvariable
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
            echo "$LINE" >> $delstrings
        fi
    done < $findvariable
    grep -v "AddTicketButton" $delstrings >> $keno_file
}

bur_action() {
    burlegend=$(<bur_head)
    
    bur_file="./bur.txt"
    if [ -f $bur_file ] ; then
        rm $bur_file
    fi
    
    findvariable=$(mktemp)
    sortstrings=$(mktemp)
    egrep -r 'Escrow command|Stacked complete|BillAcceptor|CCNet: error read answer|initialize billacceptor on port| BD: 1| BD: 2| BD: 5' log/ | sed -r 's!(^[^\(]+\()!(!g' >>$findvariable
    sort --output=$sortstrings $findvariable
    echo "$burlegend" >> $bur_file
    echo $(<"$sortstrings") >> $bur_file
    for file in ./log/*
    do
        grep -A 41 'BD: EncAcceptorBtn ' $file >> $bur_file
    done
}

case $1 in
    1 | --inkass) inkass_action
        code inkass.txt
    ;;
    2) egrep -r 'Escrow command|Stacked command|BillAcceptor|Transport|jammed status|CCTALK: error read answer' log/ | sed -r 's!(^[^\(]+\()!(!g' >>3.txt
        #grep -B   unload from   cashbox
    ;;
    3 | --bur) bur_action
        code bur.txt
    ;;
    4) egrep -r 'Escrow command|Stacked command|BillAcceptor|total spin|spintotal| BL | TW: | Balance |LUA:|enter double|opened|LCDM: e| SSP: dd |paycenter|exit double' log/ | sed -r 's!(^[^\(]+\()!(!g' >>3.txt
    ;;
    5 | --keno) keno_action
        code keno.txt
    ;;
    7) egrep -r 'LCDM' log/ | sed -r 's!(^[^\(]+\()!(!g' >>LCDM.txt
    ;;
    9) echo "Yes, Vlad has nine fingers:)"
    ;;
    *) echo "Unknown answer"
        exit 1
    ;;
esac







