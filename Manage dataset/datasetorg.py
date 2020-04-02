#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 18:35:40 2020

@author: rodrigo
"""

import pathlib
import pydicom

#%%
def organizeDicom(dcmFiles, rootDir2Write):
    
    if not(rootDir2Write.exists() and rootDir2Write.is_dir()):
        rootDir2Write.mkdir() 
        pathlib.Path(str(rootDir2Write) + "/Raw").mkdir() 
        pathlib.Path(str(rootDir2Write) + "/Processed").mkdir()         

    countRaw = 0
    countPresentation = 0

    # Run over dicom files
    for dcmFile in dcmFiles:
        
        dcmH = pydicom.dcmread(dcmFile) # read dicom
            
        dcmH.PatientName= "XXX" # Anonymize dicom
        
        protocolName = dcmH.ProtocolName.split(sep=" ", maxsplit=2)
        
        examType = "Mammo"
        
        if "FOR PROCESSING" in dcmH.PresentationIntentType:
            countRaw += 1
            presentationIntentType = "Raw"
        else:
            countPresentation += 1
            presentationIntentType = "Processed"
            
        patientPath = str(rootDir2Write) + "/" + presentationIntentType + "/" + dcmH.PatientID + "/"
        
        patientPathLib = pathlib.Path(patientPath)
        
        if not(patientPathLib.exists() and patientPathLib.is_dir()):
            patientPathLib.mkdir() 
        
        patientFilename = dcmH.PatientID + "_" + examType +  "_" + protocolName[0] +  "_" + protocolName[1] + ".dcm"
        
        pydicom.dcmwrite(patientPath + patientFilename,dcmH,write_like_original=True)   # write dicom

    return countRaw, countPresentation



def countDicom(rootDir2Read):
    
    nProjections = 0
    nMammograms2D = 0
    
    database = dict()
    
    for cancertypeDir in rootDir2Read.iterdir():
        
        if cancertypeDir.is_dir():
            
            cancerType = str(cancertypeDir).split('/')[-1]
                    
            database[cancerType] = dict()
            
            for pacientDir in cancertypeDir.iterdir():   # Run over each patient
                
                if pacientDir.is_dir():
                    
                    pacientID = str(pacientDir).split('/')[-1]
                
                    database[cancerType][pacientID] = dict(projections=0, mammograms2D=0)
                
                    for examsFiles in pacientDir.iterdir():    #Run over exames of each patient
                        
                        if 'Proj' in str(examsFiles):
                            database[cancerType][pacientID] ["projections"] += 1
                            nProjections += 1
                        
                        if 'Mammo' in str(examsFiles):  #Run over 2D-mammo of each patient
                            
                            for mammoFiles in examsFiles.glob('*.dcm'):
                                database[cancerType][pacientID] ["mammograms2D"] += 1
                                nMammograms2D += 1
    #print("Number of projections:%d and 2D mammograms:%d" % (nProjections, nMammograms2D))                          
    return nProjections, nMammograms2D
        
