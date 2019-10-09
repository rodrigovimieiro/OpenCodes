#=========================================================================
#Author: Rodrigo de Barros Vimieiro
#Date: October, 2019
#rodrigo.vimieiro@gmail.com
#=========================================================================

#!/bin/bash

make

FILE=jacobipar.bin

rank=5

if [ -f "$FILE" ]; then
     echo "$FILE exist"
     for i in {1..100}
          do
               echo === Test $i ====
               ./jacobiseq.bin $rank 1;
               ./jacobipar.bin $rank 2;
               ./jacobipar.bin $rank 4;
               ./jacobipar.bin $rank 8;
          done

     python3 jacobiparCalcTime.py

     rm -R output

else 
    echo "$FILE does not exist. Please compile it"
fi



