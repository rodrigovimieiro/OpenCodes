#=========================================================================
#Author: Rodrigo de Barros Vimieiro
#Date: October, 2019
#rodrigo.vimieiro@gmail.com
#=========================================================================

#!/bin/bash

make

FILE1=jacobipar.bin
FILE2=jacobiseq.bin

rank=20000

if [[ -f "$FILE1" && -f "$FILE2" ]]; then
     
     for i in {1..50}
     do
          echo === Test $i ====
          ./jacobiseq.bin $rank 1;
          ./jacobipar.bin $rank 2;
          ./jacobipar.bin $rank 4;
          ./jacobipar.bin $rank 8;
     done

     python3 jacobiCalcTime.py

     rm -R output

else 
    echo "$FILE does not exist. Please compile it"
fi



