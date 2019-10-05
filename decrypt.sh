#!/bin/bash


echo -n "What you need to decrypt now? (1/2/3): "
read decrypt

inkasslegend=$(<inkass_head)

case $decrypt in
    1)  file="./inkass.txt"
        if [ -f $file ] ; then
            rm $file
        fi
        echo -n "Enter start date: "
        read sdata
        echo -n "Enter end date: "
        read edata
        findvariable=$(mktemp)
        sortstrings=$(mktemp)
        delstrings=$(mktemp)
        egrep -r 'BOX 0 l|BOX 1 l|LCDM: e|BOX 0 - u|BOX 1 - u|bill end status|LCDM box 1 blocked|LCDM box 0 blocked|answer: Timeout|sensor status|LCDM: read timeout|Counting error|Motor stop status|SOL sensor|Pickup error|Over reject status' log/ | sed -r 's!(^[^\(]+\()!(!g' >> $findvariable
        sort --output=$sortstrings $findvariable
        sdata="(${sdata}"
        edata="(${edata}"
        # echo $sdata
        snumber=$(grep -n "$sdata" $sortstrings | cut -f1 -d:)
        #number=$(($number-1))
        #echo $snumber
        sed '1,'$snumber'd' $sortstrings >> $delstrings
        enumber=$(grep -n "$edata" $delstrings | cut -f1 -d:)
        echo "$inkasslegend" >> $file
        sed ''$enumber',$d' $delstrings >> $file
        for file in ./log/*
        do
            grep -A 17 'BOX 0 l' $file >> $file
            grep -B 20 'unload from   cashbox' $file >> $file
        done
    ;;
    2) egrep -r 'Escrow command|Stacked command|BillAcceptor|Transport|jammed status|CCTALK: error read answer' log/ | sed -r 's!(^[^\(]+\()!(!g' >>3.txt
        #grep -B   unload from   cashbox
    ;;
    3) egrep -r 'Escrow command|Stacked complete|BillAcceptor|CCNet: error read answer| BD: 1| BD: 2| BD: 5' log/ | sed -r 's!(^[^\(]+\()!(!g' >>3.txt
    ;;
    4) egrep -r 'Escrow command|Stacked command|BillAcceptor|total spin|spintotal| BL | TW: | Balance |LUA:|enter double|opened|LCDM: e| SSP: dd |paycenter|exit double' log/ | sed -r 's!(^[^\(]+\()!(!g' >>3.txt
    ;;
    5) egrep -r ' BD: | BL | BMA: |BEGIN' log/ | sed -r 's!(^[^\(]+\()!(!g' >>3.txt
        #(2019-09-26 11:16:01) | 21892.147056 | INFO   | GRAPH:85 | t:139950792034368 | BD: AddTicketButton : 305,524 - эти нужно удалять
    ;;
    7) egrep -r 'LCDM' log/ | sed -r 's!(^[^\(]+\()!(!g' >>LCDM.txt
    ;;
    9) echo "Yes, Vlad has nine fingers:)"
    ;;
    *) echo "Unknown answer"
        exit 1
    ;;
esac





