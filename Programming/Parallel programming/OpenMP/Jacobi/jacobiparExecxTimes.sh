#=========================================================================
#Author: Rodrigo de Barros Vimieiro
#Date: October, 2019
#rodrigo.vimieiro@gmail.com
#=========================================================================

#!/bin/bash

FILE=jacobipar.bin

if [ -f "$FILE" ]; then
     echo "$FILE exist"
     for i in {1..30}
          do
               echo === Test $i ====
               ./jacobipar.bin 3 1;
               ./jacobipar.bin 3 2;
               ./jacobipar.bin 3 4;
               ./jacobipar.bin 3 8;
          done

     python3 jacobiparCalcTime.py

     rm -R output

else 
    echo "$FILE does not exist. Please compile it"
fi



