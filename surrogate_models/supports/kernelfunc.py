import numpy as np
from scipy.spatial.distance import cdist

def calckernel(XN,XM,theta,nvar,**kwargs):
    """
    Construct a Psi matrix from a defined kernel function
    Available kernels are 'gaussian', 'exponential', 'matern32', 'matern52', and 'cubic'

    Args:
        XN (nparray): First set of sampling points
        XM (nparray): Second set of sampling points
        theta (nparray): Vector of lengthscale (1 x nvar)
        nvar (int): Number of variables

    Kwargs:
        type
    Returns:
        Psi - Covariance matrix

    Author: Pramudita Satria Palar(pramsatriapalar@gmail.com, pramsp@ftmd.itb.ac.id)
    """
    ker = kwargs.get('type', "gaussian")
    pls = kwargs.get('plscoeff', np.array([False]))
    if ker.lower() == "gaussian" or ker.lower() == "iso_gaussian":
        Psi = gaussian(XN,XM,theta,nvar,pls)
    elif ker.lower() == "exponential":
        Psi = exponential(XN, XM, theta, nvar,pls)
    elif ker.lower() == "matern32":
        Psi = matern32(XN, XM, theta, nvar,pls)
    elif ker.lower() == "matern52":
        Psi = matern52(XN, XM, theta, nvar,pls)
    else:
        raise ValueError("Kernel option not available!")
    return Psi

def gaussian(XN,XM,theta,nvar,pls):
    if pls.any() == False:
        mdist = np.zeros((np.size(XN, 0), np.size(XM, 0), nvar))
        for ii in range(0,nvar):
            X1 = np.transpose(np.array([XN[:,ii]]))
            X2 = np.transpose(np.array([XM[:,ii]]))
            mdist[:,:,ii] = (cdist(X1,X2,'euclidean')**2)/(theta[ii]**2)
    else:
        mdisttemp = np.zeros((np.size(XN, 0), np.size(XM, 0), nvar))
        for ii in range(0,nvar):
            X1 = np.transpose(np.array([XN[:,ii]]))
            X2 = np.transpose(np.array([XM[:,ii]]))
            mdisttemp[:,:,ii] = (cdist(X1,X2,'euclidean')**2)
        mdist = np.dot(mdisttemp,pls**2)/(theta**2)
    Psi = np.exp(-0.5*np.sum(mdist,2))
    return Psi

def exponential(XN,XM,theta,nvar,pls):
    mdist = np.zeros((np.size(XN,0),np.size(XM,0),nvar))
    for ii in range(0,nvar):
        X1 = np.transpose(np.array([XN[:,ii]]))
        X2 = np.transpose(np.array([XM[:,ii]]))
        mdist[:,:,ii] = (cdist(X1,X2,'euclidean'))/(theta[ii])
    Psi = np.exp(-np.sum(mdist,2))
    return Psi

def matern32(XN,XM,theta,nvar,pls):
    mdist = np.zeros((np.size(XN,0),np.size(XM,0),nvar))
    for ii in range(0,nvar):
        X1 = np.transpose(np.array([XN[:,ii]]))
        X2 = np.transpose(np.array([XM[:,ii]]))
        mdist[:,:,ii] = (cdist(X1,X2,'euclidean'))/(theta[ii])
    m3f = np.prod(1+np.sqrt(3)*mdist,2)
    m3s = np.exp(-np.sqrt(3)*np.sum(mdist,2))
    Psi = m3f*m3s
    return Psi

def matern52(XN,XM,theta,nvar,pls):
    mdist = np.zeros((np.size(XN,0),np.size(XM,0),nvar))
    for ii in range(0,nvar):
        X1 = np.transpose(np.array([XN[:,ii]]))
        X2 = np.transpose(np.array([XM[:,ii]]))
        mdist[:,:,ii] = (cdist(X1,X2,'euclidean'))/(theta[ii])
    m5f = np.prod(1+np.sqrt(5)*mdist+(5/3)*mdist**2,2)
    m5s = np.exp(-np.sqrt(5)*np.sum(mdist,2))
    Psi = m5f*m5s
    return Psi
