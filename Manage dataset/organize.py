#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 12:10:02 2020

@author: rodrigo
"""

#%%
import pathlib
from datasetorg import organizeDicom

rootDir2Read = pathlib.Path("/media/rodrigo/")
rootDir2Write = pathlib.Path("/media/rodrigo/")

paths = list(rootDir2Read.glob('**/*'))

dcmFiles = []

dircount = 0
filecount = 0
for path in paths:
    if path.is_dir():
        dircount +=1
    else:  
        if "MG" in str(path):
            filecount += 1
            dcmFiles.append(str(path))
        else:
            print(path)


nRaw, nProc = organizeDicom(dcmFiles, rootDir2Write)
    

                

