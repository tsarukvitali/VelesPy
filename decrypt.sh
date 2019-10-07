#!/bin/bash


echo -n "What you need to decrypt now? (1/2/3): "
read decrypt

inkasslegend=$(<inkass_head)

case $decrypt in
    1)  inkass_file="./inkass.txt"
        if [ -f $inkass_file ] ; then
            rm $inkass_file
        fi
        findvariable=$(mktemp)
        sortstrings=$(mktemp)
        snumberf=$(mktemp)
        delstrings=$(mktemp)
        egrep -r 'BOX [0-1] l|LCDM: e|BOX [0-1] - u|bill end status|LCDM box [0-1] blocked|answer: Timeout|sensor status|LCDM: read timeout|Counting error|Motor stop status|SOL sensor|Pickup error|Over reject status' log/ | sed -r 's!(^[^\(]+\()!(!g' >> $findvariable
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
            grep -A 17 'BOX 0 l' $file >> $inkass_file
            grep -B 20 'unload from   cashbox' $file >> $inkass_file
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





