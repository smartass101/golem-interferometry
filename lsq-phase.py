#!/usr/bin/python2

import numpy as np
from scipy.optimize import curve_fit

#------------PARAMETERS-----------
freq_mod=500e3*2*np.pi #the base modulation freq
def fsin(time,A,phase):
    """the primitive func for fitting"""
    return A*np.sin(freq_mod*time+phase)

def get_phase(buff,last_phase=0): 
    """extracts phase from buffer conatining a part of the sine wave"""
    params,garbage=curve_fit(fsin,buff[:,0],buff[:,1],[buff.argmax(),last_phase]) #fits data 
    #TODO FREQ IS NOT FITTED, WILL IT MATTER ?
    if(params[0]<0): #if the amplitude is negative, phase needs offset
        if(np.abs(params[1]+np.pi-last_phase)<np.abs(params[1]-np.pi-last_phase)): 
            #check which offset is appropriate based on the diff from the last known phase
            params[1]+=np.pi
        else:
            params[1]-=np.pi
    elif(params[0]==0): #hmm, data bad...apmlitude 0??
        params[1]=0 # at least make it easily detectable
    return params[1]


