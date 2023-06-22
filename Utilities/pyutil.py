#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 30 11:25:18 2021

@author: rodrigo
"""

import numpy as np
import pydicom
import pydicom._storage_sopclass_uids

def writeDicom(dcmFileName, dcmImg):
    '''
    
    Description: Write empty Dicom file
    
    Input:
        - dcmFileName = File name, e.g. "myDicom.dcm".
        - dcmImg = image np array
    
    Output:
        - 
            
    
    Source:
    
    '''
    
    dcmImg = dcmImg.astype(np.uint16)

    # print("Setting file meta information...")

    # Populate required values for file meta information
    meta = pydicom.Dataset()
    meta.MediaStorageSOPClassUID = pydicom._storage_sopclass_uids.MRImageStorage
    meta.MediaStorageSOPInstanceUID = pydicom.uid.generate_uid()
    meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian  
    
    ds = pydicom.Dataset()
    ds.file_meta = meta
    
    ds.is_little_endian = True
    ds.is_implicit_VR = False
    
    ds.SOPClassUID = pydicom._storage_sopclass_uids.MRImageStorage
    ds.PatientName = "Test^Firstname"
    ds.PatientID = "123456"
    
    ds.Modality = "MR"
    ds.SeriesInstanceUID = pydicom.uid.generate_uid()
    ds.StudyInstanceUID = pydicom.uid.generate_uid()
    ds.FrameOfReferenceUID = pydicom.uid.generate_uid()
    
    ds.BitsStored = 16
    ds.BitsAllocated = 16
    ds.SamplesPerPixel = 1
    ds.HighBit = 15
    
    ds.ImagesInAcquisition = "1"
    
    ds.Rows = dcmImg.shape[0]
    ds.Columns = dcmImg.shape[1]
    ds.InstanceNumber = 1
    
    ds.ImagePositionPatient = r"0\0\1"
    ds.ImageOrientationPatient = r"1\0\0\0\-1\0"
    ds.ImageType = r"ORIGINAL\PRIMARY\AXIAL"
    
    ds.RescaleIntercept = "0"
    ds.RescaleSlope = "1"
    ds.PixelSpacing = r"1\1"
    ds.PhotometricInterpretation = "MONOCHROME2"
    ds.PixelRepresentation = 1
    
    pydicom.dataset.validate_file_meta(ds.file_meta, enforce_standard=True)
    
    # print("Setting pixel data...")
    ds.PixelData = dcmImg.tobytes()
    
    ds.save_as(dcmFileName)
    
    return