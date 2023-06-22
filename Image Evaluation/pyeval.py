#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Rodrigo
"""

import numpy as np
import scipy.optimize as opt
import scipy.stats as st
import matplotlib.pyplot as plt
import cv2

from scipy.signal import fftconvolve
from scipy.ndimage.filters import uniform_filter1d

def constrast2NoiseRatio(RoiForeGround, RoiBackGround):
    '''
    
    Description: Calculates the CNR of two Region of Interest (ROI)
    
    Input:
        - RoiForeGround = ROI of object, e.g. MicroCalcification.
    
    Output:
        - RoiBackGround = ROI of the backgorund
            
    
    Source: https://doi.org/10.1002/sca.21179
    
    '''
    
    mu1 = RoiForeGround.mean()
    mu2 = RoiBackGround.mean()
    
    var1 = RoiForeGround.var()
    var2 = RoiBackGround.var()
    
    cnr = np.abs(mu1 - mu2) / np.sqrt(var1 + var2)
    
    return cnr

def NRMSE(roiNoise, roiNoiseLess):
    '''
    
    Description: Calculates the Normalized Root Mean Squared Error between an
    a noise ROI and a noiseless ROI. The normalization is done by the standard
    deviation of the noiseless signal.
    
    Input:
        - roiNoise = Region of Interest with noise
        - roiNoiseLess = Region of Interest without noise
    
    Output:
        - nrmse = NRMSE between the ROIs
            
    
    Source: https://doi.org/10.1117/12.2255058
    
    '''
    
    nrmse = np.sqrt(np.mean((roiNoise - roiNoiseLess) ** 2)) / np.std(roiNoiseLess)
    
    return nrmse

def MNSE(rlzs_GT, rlzs):
    '''
    
    Description: Mean normalized squared error (MNSE), which we compute as 
    follows: first, for every pixel, we compute the normalized quadratic error
    as the squared difference from the ground-truth divided by the ground-
    truth; second, the MNSE is obtained as the average of the pixelwise 
    normalized quadratic errors on the breast over the entire image. 
    
    Input:
        - rlzs_GT = Realizations of the ground-truth
        - rlzs = Realizations of non-ground-truth images
    
    Output:
        - mnse = (Mean normalized squared error (MNSE), CI)
        - resNoiseVar = (Normalized residual noise variance, CI)
        - bias2 = (Normalized bias squared, CI)
        - proof = Proof of the decomposition
            
    
    Source: https://doi.org/10.1088/1361-6501/aab2f6
    
    Code by Lucas Borges
    
    '''
    
    n_rlzs_GT = rlzs_GT.shape[-1]   # Number of ground-truth realizations
    n_rlzs = rlzs.shape[-1]         # Number of non-ground-truth realizations
    
    # Generate the ground-truth from the realizations
    groundTruth = np.mean(rlzs_GT, axis=-1)
    
    # There are a limited number of images to estimate the GT, so there is an 
    # error associated with the measurements. This Factor will cancel out this
    # error (The factor is basically (ResidualNoiseSTD*1/sqrt(N))^2
    resNoiseVar_GT = np.mean(np.var(rlzs_GT, ddof=1, axis=-1) / groundTruth)
    factor1 = (resNoiseVar_GT / n_rlzs_GT)
    
    #  Estimate the Mean Normalized Squared Error (MNSE) from each realization
    # the 'normalization' term here is the signal expectation
    mnse = np.empty(shape=n_rlzs)
    for r in range(n_rlzs):
        nqe = ((rlzs[...,r] - groundTruth) ** 2) / groundTruth
        mnse[r] = nqe.mean() - factor1
    
    # Estimate the normalized residual noise variance
    resNoiseVar = np.var(rlzs, ddof=1, axis=-1) / groundTruth
    
    # Calculate the confidence interval
    resNoiseVar_CI = st.t.interval(0.95, resNoiseVar.size-1, 
                                   loc=np.mean(resNoiseVar), 
                                   scale=st.sem(resNoiseVar.ravel()))
    
    resNoiseVar = resNoiseVar.mean()


    # Estimate the normalized bias squared
    bias2 = ((np.mean(rlzs, axis=-1) - groundTruth) ** 2) / groundTruth
    
    # Again, there is an error associated with the limited number of realiza-
    # tions that we used to estimate the bias. This second factor is related 
    # to the number of realizations used for the bias estimation (n_rlzs), 
    # while Factor 1 is related to the number of realizations used for the 
    # GT (n_rlzs_GT). 
    factor2 = (resNoiseVar / n_rlzs)
    
    # The bias must now be adjusted by two factors: one of them due to the 
    # 'imperfect' GT (Factor1) and the second one due to the limited number of 
    # realizations used to estimate the bias itself (Factor2)
    bias2 = bias2 - factor1 - factor2 
    
    # Calculate the confidence interval
    bias2_CI = st.t.interval(0.95, bias2.size-1, 
                                   loc=np.mean(bias2), 
                                   scale=st.sem(bias2.ravel()))
    
    bias2 = bias2.mean()  
    
    # Since the bias squared and the residual noise variance are the decompo-
    # sitions of the MNSE, the sum of bias^2 + Residual Variance must be equal 
    # to the MNSE
    mnse_CI = st.t.interval(0.95, mnse.size-1, 
                                   loc=np.mean(mnse), 
                                   scale=st.sem(mnse))
    mnse = mnse.mean() 
    proof = mnse - resNoiseVar - bias2
    
    # print('==================================')
    # print('Total MNSE: {:.2f}%'.format(100*mnse))
    # print('Residual Noise: {:.2f}%'.format(100*resNoiseVar))
    # print('Bias Squared: {:.2f}%'.format(100*bias2))
    # print('Proof (must be ~0%): {:.2e}%'.format(100*proof))
    # print('==================================')
    
    return np.hstack([mnse,mnse_CI]), np.hstack([resNoiseVar,resNoiseVar_CI]), np.hstack([bias2,bias2_CI]), proof

def signal2NoiseRatio(roi, GT=None, mode='local'):
    '''
    
    Description: Calculates the SNR of a Region of Interest (ROI)
    
    Input:
        - roi = Region of Interest
        - GT = If Ground-Truth is provided, dont calculate the mean value.
        - mode = local or depth. Local calculates the SNR in a mooving ROI and 
        depth calculates with n-realizations. In depth mode, the functions ex-
        pects the roi in [H,W,C] format. 
    
    Output:
        - snr = SNR of each pixel
            
    
    Source: 
    
    '''
    
    if mode == 'local':
        # Mean and Variance calculation
        # Calculate variance through the whole image:
        # https://en.wikipedia.org/wiki/Variance
        
        exp = cv2.blur(roi, (15, 15), cv2.BORDER_REPLICATE)
        exp2 = cv2.blur(roi**2, (15, 15), cv2.BORDER_REPLICATE)
        
        var_estimated = exp2-exp**2
        if GT is None:
            mean_estimated = exp
        else:
            mean_estimated = GT
        
    elif mode == 'depth':
        
        var_estimated = np.var(roi, ddof=1, axis=-1)
        if GT is None:
            mean_estimated = np.mean(roi, axis=-1)
        else:
            mean_estimated = GT
    else:
        raise ValueError("Invalid mode. Try 'local' or 'depth'.")
        
    # SNR calculation
    snr = mean_estimated / np.sqrt(var_estimated)
    
    return snr

def calc_digital_nps(I, n, px = 1, use_window = 0, average_stack = 0, use_mean = 0):
    '''
    
    Description: Calculates the digital noise-power spectrum (NPS) noise-only
    realizations.
    
    Input:
        - I = stack of ROIs
        - n = n-dimensional noise realizations, e.g. 2
        - px = pixel/detector size
        - use_window = Useful for avoiding spectral leakage?
        - average_stack = mean on all ROIs?
        - use_mean = subtract mean or not?
    
    Output:
        - nps = noise-power spectrum (NPS)
        - f = frequency vector
            
    
    Source: https://www.mathworks.com/matlabcentral/fileexchange/
    36462-noise-power-spectrum?s_tid=prof_contriblnk
    
    -----------------
    
    Calculates the digital noise-power spectrum (NPS) noise-only
    realizations. The following rference provides a good overview of NPS
    calculations:
    I. A. Cunningham, in Handbook of Medical Imaging (SPIE Press,
    Bellingham, USA, 2000), vol. 1.
    
    I is a stack of symmetric n-dimensional noise realizations. The
    realizations are stacked along the last array dimension of I. If
    average_stack is set, the calculated NPS is averaged over the stack to
    reduce uncertainty. 
    
    px is the pixel size of the image.
    
    If use_window is set, the data is multiplied with a Hann tapering window
    prior to NPS calculation. Windowing is useful for avoiding spectral
    leakage in case the NPS increases rapidly towards lower spatial
    frequencies (e.g. power-law behaviour).
    
    nps is the noise-power spectrum of I in units of px^n, and f is the
    corresponding frequency vector.
    
    Erik Fredenberg, Royal Institute of Technology (KTH) (2010).
    Please reference this package if you find it useful.
    Feedback is welcome: fberg@kth.se.
    
    '''
    
    size_I = I.shape
    
    if size_I[0] != size_I[1]:
        raise ValueError("ROI must be symmetric.")
    
    roi_size = size_I[0]
    
    # Cartesian coordinates
    x = np.linspace(-roi_size / 2, roi_size / 2, roi_size)
    _, x = np.meshgrid(x,x)
    
    # frequency vector
    f = np.linspace(-0.5, 0.5, roi_size) / px
    
    # radial coordinates
    r = np.sqrt(x**2 + np.transpose(x)**2)
    
    # Hann window to avoid spectral leakage
    if use_window:
        hann = 0.5 * (1 + np.cos(np.pi * r / (roi_size / 2)))
        hann[r > roi_size / 2] = 0
        hann = np.expand_dims(hann, axis=-1)
    else:
        hann = 1
    
 
    # detrending by subtracting the mean of each ROI
    # more advanced schemes include subtracting a surface, but that is
    # currently not included
    if use_mean: 
        S = np.mean(I, axis=(0,1))
        S = np.expand_dims(np.expand_dims(S, axis=0), axis=0)
    else:
        S = 0

    F = (I - S) * hann
        
    # equivalent to fftn
    F = np.fft.fftshift(np.fft.fft2(F, axes=(0,1))) 
    
    # cartesian NPS
    # NPS in units of px^n
    # the normalization with h is according to Gang 2010
    nps = np.abs(F) ** 2 / roi_size ** n * px ** n / (np.sum(hann**2) / hann.size)  


    # averaging the NPS over the ROIs assuming ergodicity
    if average_stack:
        nps = np.mean(nps, axis=2)
        
    # nps *= roi_size ** 2 * px ** 2
    
    return nps, f

def noisePowerSpectrum(img, roiSize = [], pixelSize = []):
    '''
    
    Description: Calculates the digital noise-power spectrum (NPS) noise-only
    realizations.
    
    Input:
        - img = image to calculate NPS
        - roiSize = Size of ROI that will be extracted
        - pixelSize = pixel/detector size
    
    Output:
        - nps2D = 2D NPS
        - nps1D = 1D NPS (radial)
        - f1D = frequency vector
        
    '''
    
    img = img.astype('float64')
    
    M, N = img.shape

    if not roiSize:
        roiSize = M
    
    if roiSize <= 0 or roiSize > M:
        roiSize = M

    if not pixelSize:
        raise ValueError("No pixel size input")


    # Sub-images Selection (processing each sub-image)
    # Size of each ROI
    nRoi = (M // roiSize) * (N // roiSize) # Number of sub-images
    rois = np.empty((roiSize,roiSize,nRoi), dtype='float64')
    k = 0

    for i in range(M // roiSize):
        for j in range(N // roiSize):
            
            rois[:,:,k] = img[i*roiSize:(i+1)*roiSize,j*roiSize:(j+1)*roiSize]
                
            #las = img.mean()   # Large Area Signal
            
            rois[:,:,k] -= rois[:,:,k].mean()         
            
            k += 1

    # NPS 2D
    nps2D, _ = calc_digital_nps(rois, 2, pixelSize, 1, 1, 0)
    
    # Normalization
    nps2D /= img.mean() ** 2
 
    # NPS 1D - RADIAL - Euclidean Distance
    cx = roiSize//2
    
    nFreqSample = cx + 1
    nyquist = 1/(2*pixelSize)
    
    # Distance matrix (u, v) plane
    x = np.arange(-cx,roiSize-cx)
    xx, yy = np.meshgrid(x,x)  
    radialDst = np.round(np.sqrt(xx**2 + yy**2))
    
    # Generate 1D NPS
    nps1D = np.empty(shape=(nFreqSample))
    for k in range(nFreqSample):
        nps1D[k] = nps2D[radialDst == k].mean()
    
    f1D = np.linspace(0, nyquist, nFreqSample) 
        
    return nps2D, nps1D, f1D

def calc_digital_ps(I, n, px = 1, use_window = 0, average_stack = 0, use_mean = 0):
    '''
    
    Description: Calculates the digital power spectrum (PS) realizations.
    
    Input:
        - I = stack of ROIs
        - n = n-dimensional noise realizations, e.g. 2
        - px = pixel/detector size
        - use_window = Useful for avoiding spectral leakage?
        - average_stack = mean on all ROIs?
        - use_mean = subtract mean or not?
    
    Output:
        - nps = noise-power spectrum (NPS)
        - f = frequency vector
            
    
    -----------------
    
    
    '''
    
    size_I = I.shape
    
    if size_I[0] != size_I[1]:
        raise ValueError("ROI must be symmetric.")
    
    roi_size = size_I[0]
    
    # Cartesian coordinates
    x = np.linspace(-roi_size / 2, roi_size / 2, roi_size)
    _, x = np.meshgrid(x,x)
    
    # frequency vector
    f = np.linspace(-0.5, 0.5, roi_size) / px
    
    # radial coordinates
    r = np.sqrt(x**2 + np.transpose(x)**2)
    
    # Hann window to avoid spectral leakage
    if use_window:
        hann = 0.5 * (1 + np.cos(np.pi * r / (roi_size / 2)))
        hann[r > roi_size / 2] = 0
        hann = np.expand_dims(hann, axis=-1)
    else:
        hann = 1
    
 
    # detrending by subtracting the mean of each ROI
    # more advanced schemes include subtracting a surface, but that is
    # currently not included
    if use_mean: 
        S = np.mean(I, axis=(0,1))
        S = np.expand_dims(np.expand_dims(S, axis=0), axis=0)
    else:
        S = 0

    F = (I - S) * hann
        
    # equivalent to fftn
    F = np.fft.fftshift(np.fft.fft2(F, axes=(0,1))) 
    
    # PS
    ps = np.abs(F) ** 2 #/ roi_size ** n * px ** n / (np.sum(hann**2) / hann.size)  


    # averaging the NPS over the ROIs assuming ergodicity
    if average_stack:
        ps = np.mean(ps, axis=2)
        
    ps = ((px**2)/(size_I[0]**2)) * ps
            
    return ps, f

def powerSpectrum(img, roiSize = [], pixelSize = []):
    '''
    
    Description: Calculates the digital power spectrum (PS). Image must be 
    segmented, i.e., 0 in the backgorund and the signal in the foreground
    
    Input:
        - img = image to calculate NPS
        - roiSize = Size of ROI that will be extracted
        - pixelSize = pixel/detector size
    
    Output:
        - nps2D = 2D PS
        - nps1D = 1D PS (radial)
        - f1D = frequency vector
        
    '''
    
    img = img.astype('float64')
    
    M, N = img.shape

    if not roiSize:
        roiSize = M
    
    if roiSize <= 0 or roiSize > M:
        roiSize = M

    if not pixelSize:
        raise ValueError("No pixel size input")
        
    rois = []
        
    for i in range(0, M-roiSize, roiSize):
        for j in range(0, N-roiSize, roiSize):
            roi = img[i:i+roiSize, j:j+roiSize]
            
            if np.sum(roi == 0) < 1:
                roi -= roi.mean() 
                rois.append(roi)
                
    rois = np.stack(rois, axis=-1)

    # NPS 2D
    nps2D, _ = calc_digital_ps(rois, 2, pixelSize, 1, 1, 0)
    
    # Normalization (consireding segmented img)
    nps2D /= img[img>0].mean()** 2
 
    # NPS 1D - RADIAL - Euclidean Distance
    cx = roiSize//2
    
    nFreqSample = cx + 1
    nyquist = 1/(2*pixelSize)
    
    # Distance matrix (u, v) plane
    x = np.arange(-cx,roiSize-cx)
    xx, yy = np.meshgrid(x,x)  
    radialDst = np.round(np.sqrt(xx**2 + yy**2))
    
    # Generate 1D NPS
    nps1D = np.empty(shape=(nFreqSample))
    for k in range(nFreqSample):
        nps1D[k] = nps2D[radialDst == k].mean()
    
    f1D = np.linspace(0, nyquist, nFreqSample) 
        
    return nps2D, nps1D, f1D

def calc_beta_PS(f1D, ps1D):
    '''
    
    Description: Calculate beta of PS curve.
    
    Input:
        - f1D = frequencies
        - ps1D = 1D power spectrum
    
    Output:
        - Beta value
        
    Source: https://doi.org/10.1109/TMI.2020.2991295
        
    '''
    
    # Find freqs greater than 0.1mm-1 and smaller than 1mm-1
    ind = np.where((f1D >= 0.1) & (f1D <= 1)) 
    
    # Change to log-log scale
    log_nps1D = np.log10(ps1D[ind])
    log_f1D = np.log10(f1D[ind])
    
    # Fit first order polynomial
    # mx + b
    m,b = np.polyfit(log_f1D, log_nps1D, 1)
    
    return m

def __gauss1D(x, p): 
    '''
    
    Description: Generate a 1D Gaussian PDF.
    
    Input:
        - x = x axis values
        - p = tuple -> p[0]=mean, p[1]=stdev
    
    Output:
        - Gaussian PDF
        
    Source: https://stackoverflow.com/a/10605108/8682939
        
    '''
    
    return 1.0/(p[1]*np.sqrt(2*np.pi))*np.exp(-(x-p[0])**2/(2*p[1]**2))

def __gauss2D(roi_size, stdev):
    '''
    Description: Generate a 1D Gaussian PDF.
    
    Input:
        - roi_size = Tuple of ROI size
        - stdev = standard deviation of the gaussian
    
    Output:
        - 2D Gaussian PDF
        
    Source: https://stackoverflow.com/a/25723181/8682939
    
    '''
    
    mu = [x // 2 for x in roi_size]
    
    xx, yy = np.meshgrid(np.linspace(0,roi_size[0]-1,roi_size[0]), 
                         np.linspace(0,roi_size[1]-1,roi_size[1]))
    
    xy = np.column_stack([xx.flat, yy.flat])

    mean_gauss_2d = np.array([mu[0],mu[1]])
    cov_gauss_2d = np.diagflat([stdev**2,stdev**2])

    z = st.multivariate_normal.pdf(xy, mean=mean_gauss_2d, cov=cov_gauss_2d)
    
    z = z.reshape(xx.shape)
    
    z /= z.sum()
    
    return z

def __preProcessFWHM(signal, plotFig = False):
    
    '''
    
    Description: Find the Gaussian "borders" and crop it to pass to the FWHM
    function
    
    Input:
        - signal = 1D signal
        - plotFig = Boolean var to plot figure
    
    Output:
        - signal = Cropped signal
        
    Source: 
        
    '''
    
    firstDv = np.gradient(uniform_filter1d(signal, size=10))
    secondDv = np.gradient(uniform_filter1d(firstDv, size=2))
    aux_secondDv = secondDv.copy()
    max1 = np.argmax(secondDv)
    aux_secondDv[max1-5:max1+5] = 0
    max2 = np.argmax(aux_secondDv)
    
    if max1 > max2:
        maxR = max1
        maxL = max2
    else:
        maxR = max2
        maxL = max1
        
    if plotFig:
        plt.figure()
        plt.plot(signal, label="Signal")
        plt.plot(uniform_filter1d(signal, size=10), label="Smooth Signal")
        plt.plot(uniform_filter1d(firstDv, size=2), label="1st Grad")
        plt.plot(secondDv, label="2nd Grad")
        plt.legend(loc="upper right")
    
    return signal[maxL:maxR]
        
def FWHM(signal, px, preProcess = False, plotFig = False):
    '''
    
    Description: Fit a Gaussian to the data and extract the Full width at 
    half maximum (FWHM).
    
    Input:
        - signal = 1D signal
        - px = Pixel size
        - preProcess = Boolean var to pre-process signal
        - plotFig = Boolean var to plot figure
    
    Output:
        - FWHM_value = FWHM value
        
    Source: https://stackoverflow.com/a/10605108/8682939
        
    '''
    
    Y = signal.copy()
    
    # Bring signal to the X axis
    Y -= np.min(Y)
    
    # Pre process the signal if necessary (crop it)
    if preProcess:
        Y = __preProcessFWHM(Y, plotFig=plotFig)
        
    X = np.linspace(0,Y.shape[0],Y.shape[0])
    
    # Normalize to a proper PDF (area = 1)
    normFactor = Y.sum()
    Y /= normFactor
    
    # Fit a guassian
    p0 = [0,1] # Inital guess is a normal distribution
    errfunc = lambda p, x, y: __gauss1D(x, p) - y # Distance to the target function
    p1, success = opt.leastsq(errfunc, p0[:], args=(X, Y))
    
    fit_mu, fit_stdev = p1
    
    FWHM_value = 2*px*np.sqrt(2*np.log(2))*fit_stdev
    
    if plotFig:
        plt.figure()
        plt.plot(X,Y,label="Signal")
        plt.plot(X,__gauss1D(X, (fit_mu,fit_stdev)),label="Approx")
        plt.legend(loc="upper right")

    return FWHM_value, tuple((fit_mu, fit_stdev))

def imhist(img, nBins = 50):
    '''
    
    Description: Shows the image histogram
    
    Input:
        - img = 2D image
        - nBins = Number of histogram bins
    
    Output:
        - None 
        
    Source: https://stackoverflow.com/a/5328669/8682939
        
    '''
    
    hist, bins = np.histogram(img, bins=nBins)
    width = 0.7 * (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    plt.figure()
    plt.bar(center, hist, align='center', width=width)
    plt.xlabel("Gray levels")
    plt.ylabel("Counts")

    return

def MTF(edgeSignal, pixelSize):
    '''
    
    Description: 
    
    --------------------------------------------------------------------------
    Compute the Modulation Transfer Function (MTF) through the edge spread 
    function. 
    
    "For systems with a rotationally symmetric Impulse-response function (IRF), 
    MTF(u, v) is also rotationally symmetric and can be expressed in terms of 
    a single radial spatial frequency u without loss of generality." [1]
    
    
    So we can evaluate the 2D MTF, through the 1D MTF.
    
    
    The Edge Spread Function (ESF) can be differentiated to produce the 
    corresponding Line-Spread Function (LSF). [2]
    
    "The LSF describes the response of the system to a "line" delta 
    function" [1]
    
    
    "The one-dimensional OTF in Eq. (2.44) and the line-spread function are 
    Fourier pairs:
        OTF(u) = F{lsf(x)} " [1]
    
    "The optical transfer function (OTF) is related to the MTF as: 
        
        MTF(u) = |OTF(u)|, 
    
    and is similar to the MTF although it retains phase-transfer 
    information." [1]
    
    --------------------------------------------------------------------------
    Input:
        - edgeSignal = Edge Spread Function (ESF)
        - pixelSize = Pixel size
    
    Output:
        - mtf = dictonary
            - mtf_real = MTF(u) 
            - mtf_fit = MTF(u) fitted through a Gaussian
            - fit_mu = Gaussian mean
            - fit_stdev = Gaussian std
            - f1D = frequency vector up to Nyquist
        
    Source: 
    [1] Handbook of Medical Imaging, Volume 1. Physics and Psychophysics
    [2] https://dx.doi.org/10.1118%2F1.4800795
    [3] https://github.com/habi/GlobalDiagnostiX/blob/master/MTF.py
    [4] http://is.gd/uSC5Ve
    
    
    Demo:
        
    N = 251
    esf = np.zeros(N)
    esf[N // 2:] = 1
    
    lsf = __LSF(esf)
    mtf = MTF(esf)
    
    plt.figure(figsize=(12,4))
    plt.subplot(1, 3, 1)
    plt.plot(esf)
    plt.title("Edge Spread Function")
    plt.subplot(1, 3, 2)
    plt.plot(lsf)
    plt.title("Line Spread Function")
    plt.subplot(1, 3, 3)
    plt.plot(mtf)
    plt.title("Modulation Transfer Function")
        
    '''
    
    edgeSpreadFunction = edgeSignal
    
    if edgeSpreadFunction[0] > edgeSpreadFunction[-1]:
        edgeSpreadFunction = np.flip(edgeSpreadFunction)

    lineSpreadFunction = __LSF(edgeSpreadFunction) # [2]
    
    otf = np.fft.fftshift(np.fft.fft(lineSpreadFunction))
    
    mtf = np.abs(otf) 
    
    mtf /= mtf[0]
    
    # Fit a Gaussian
    y = mtf
    x = np.arange(0, y.shape[0])
    
    y_min = np.min(y)
    y_sum = y.sum() 
    
    # Normalize to a proper PDF (area = 1)
    y = (y-y_min) / y_sum
    
    # Inital guess is a normal distribution
    p0 = [0,1] 
    errfunc = lambda p, x, y: __gauss1D(x, p) - y # Distance to the target function
    p1, success = opt.leastsq(errfunc, p0[:], args=(x, y))
    
    fit_mu, fit_stdev = p1
    
    mtf_fit = __gauss1D(np.linspace(0, x[-1], 10*x.shape[0]), p1)
    
    # Return mtf to previus range
    mtf_fit = mtf_fit * y_sum + y_min
    
    zeroFreqInd = mtf.shape[0]//2
    
    mtf_real = mtf[zeroFreqInd::-1]
    mtf_fit = mtf_fit[(mtf_fit.shape[0]//2)::-1]
    
    # Generate freq vector
    nFreqSample = zeroFreqInd + 1
    nyquist = 1/(2*pixelSize)
    
    f1D = np.linspace(0, nyquist, nFreqSample)
    
    mtf = {}
    mtf['real'] = mtf_real
    mtf['fit'] = mtf_fit
    mtf['f1D'] = f1D
    mtf['fit_mu'] = fit_mu
    mtf['fit_stdev'] = fit_stdev
    
    return mtf

def __LSF(edgeSignal):
    
    edgeSpreadFunction = edgeSignal
    
    # Response of the system to a "line" delta function [1]
    linespreadfunction = np.diff(edgeSpreadFunction)
    
    return linespreadfunction

def fspecial_gauss(size, sigma):
    """Function to mimic the 'fspecial' gaussian MATLAB function
    Source: https://stackoverflow.com/a/27928469/8682939
    """

    x, y = np.mgrid[-size // 2 + 1:size // 2 + 1, -size // 2 + 1:size // 2 + 1]
    g = np.exp(-((x ** 2 + y ** 2) / (2.0 * sigma ** 2)))
    return g / g.sum()

def quality_index_local_variance(I, I2, Ws, raw=False, mask=None):
    '''
    # QILV()
    # ==================================================================
    # Quality Index based on Local Variance
    # Santiago Aja-Fernandez
    #
    # santi@bwh.harhard.edu
    # Accorging to
    #
    # S. Aja-Fernández, R. San José Estépar, C. Alberola-López and C.F. Westin,
    # "Image quality assessment based on local variance", EMBC 2006,
    # New York, Sept. 2006.
    #
    # https://www.mathworks.com/matlabcentral/fileexchange/36950-quality-index-based-on-local-variance-qilv
    # ------------------------------------------------------------------
    #
    # The function calculates a global compatibility measure
    # between two images, based on their local variance distribution.
    #
    # ------------------------------------------------------------------
    #
    # INPUT:   (1) I: The first image being compared
    #          (2) I2: the second image being compared
    #          (3) Ws: window for the estimation of statistics:
    #		If Ws=0: default gaussian window
    #               If Ws=[M N] MxN square window
    #
    #
    # OUTPUT:
    #          (1) ind: Quality index (between 0 and 1)
    #
    # Default usage:
    #
    #   ind=s_correct(I,I2,0);
    # ==================================================================      
    '''


    I = I.astype(np.float64)
    I2 = I2.astype(np.float64)

    # Data type maximum range
    L = 4095

    K = [0.01, 0.03]
    C1 = (K[0] * L) ** 2
    C2 = (K[1] * L) ** 2

    if Ws == 0:
        window = fspecial_gauss(11, 1.5)
    else:
        window = fspecial_gauss(Ws, 1.5)

    window = window / np.sum(window)

    # Local means
    M1 = fftconvolve(I, window, mode='same')
    M2 = fftconvolve(I2, window, mode='same')

    # Local Variances
    V1 = fftconvolve(I ** 2, window, mode='same') - M1 ** 2
    V2 = fftconvolve(I2 ** 2, window, mode='same') - M2 ** 2

    if mask is not None:

        # Global statistics:
        m1 = np.mean(V1[mask])
        m2 = np.mean(V2[mask])
        s1 = np.std(V1[mask], ddof=1)
        s2 = np.std(V2[mask], ddof=1)
        s12 = np.mean((V1[mask] - m1) * (V2[mask] - m2))

    else:
        # Global statistics:
        m1 = np.mean(V1)
        m2 = np.mean(V2)
        s1 = np.std(V1, ddof=1)
        s2 = np.std(V2, ddof=1)
        s12 = np.mean((V1 - m1) * (V2 - m2))

    # Index
    ind1 = ((2 * m1 * m2 + C1) / (m1 ** 2 + m2 ** 2 + C1))
    ind2 = (2 * s1 * s2 + C2) / (s1 ** 2 + s2 ** 2 + C2)
    ind3 = (s12 + C2 / 2) / (s1 * s2 + C2 / 2)
    ind = ind1 * ind2 * ind3

    return ind
