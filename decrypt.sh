#!/bin/bash


echo -n "What you need to decrypt now? (1/2/3): "
read decrypt
inkasslegend="Добрый день!

Информация за указанный промежуток времени о выданных купюрах и ошибках описана ниже:


LCDM: e5 r0 c5 n1000.00 0 - e* - кол-во купюр прошедших через EXIT SENSOR, r* - кол-во купюр скинутых в реджект, c* - кол-во купюр прошедших через CHK SENSOR, n - номинал купюр
BOX 0 - u5 r0 c325 n1000 - u* - кол-во купюр вытащенных с кассеты, r* - кол-во купюр скинутых в реджект, с* - кол-во купюр оставшихся в диспенсере(в кассете + в реджект трее)
LCDM: command '45', answer: Jam at EXIT sensor or EJT sensor status: '35' - ошибка диспенсера, при выдаче с верхней кассеты(command '45'), пришел ответ о замятии купюры в районе EXIT-сенсора или EJT-сенсора( Jam at EXIT sensor or EJT sensor status: '35')
LCDM: command '44', answer: Normal stop status: '31' - диспенсер успешно(Normal stop status: '31') очистил транспорт(command '44')
LCDM: command '44', answer: Jam at DIV sensor status: '36' - диспенсер не успешно очистил транспорт(command '44'), замятие купюры в районе DIV-сенсора (Jam at DIV sensor status: '36' )
LCDM: command '45', answer: Jam at CHK 1,2 sensor status: '33' - ошибка диспенсера, при выдаче с верхней кассеты(command '45'), пришел ответ о замятии купюры в районе CHK-сенсора( Jam at CHK 1,2 sensor status: '33')
LCDM: command '45', answer: Timeout (from DIV TO EJT sensors) status: '43' - ошибка диспенсера, при выдаче с верхней кассеты(command '45'), пришел ответ таймаут прохождения купюры между сенсорами DIV и EJT( Timeout (from DIV TO EJT sensors) status: '43' )
LCDM: command '45', answer: Pickup error status: '32' - ошибка диспенсера, при выдаче с верхней кассеты(command '45'), пришел ответ о ошибке захвата купюры из кассеты (Pickup error status: '32')
LCDM: command '45', answer: Upper bill end status: '38' - ошибка диспенсера, при выдаче с верхней кассеты(command '45'), пришел ответ, что в кассете отсутствуют купюры (Upper bill end status: '38')
LCDM box 0 blocked - диспенсер заблокировал верхнюю кассету для выдачи(блокировка снимается при перезагрузке терминала)')"

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
        echo "$inkasslegend" >> inkass.txt
        sed ''$enumber',$d' $delstrings >> inkass.txt
        for file in ./log/*
        do
	        grep -A 17 'BOX 0 l' $file >> inkass.txt
            grep -B 20 'unload from   cashbox' $file >> inkass.txt
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





