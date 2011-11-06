#!/usr/bin/python2
"""fit the sine signal with a sine function using the least squares method"""

################ IMPORTING ################

from scipy import pi #used in sin() funcs
from scipy.optimize import leastsq #the least square analyzer
from numpy import loadtxt, sin, floor #for loadidng the file and for sin() and rounding

################ PARAMETERS ################

f_base=5e5 #the modulation frequency, the base frequancy of the sine signal
A_base=0.05 #the expected amplitude of the singal
fname='ch1.csv'#file with the sine signal
start_per=5 #how many periods to scan to obtain first approximation of parameters
p0=[A_base, fbase, 0] #initial parameter sequnce to be passed to the leastsq

################ FILE OPENING ################

data_file=open(fname, 'r') #open data file read-only
x, y=loadtxt(data_file, delimiter=',', unpack=True) #load and unpack the data

################ CALCULATED PARAMETERS ################

dt=x[1] - x[0] #calculate the time step
period_len=len(x) * dt * f_base #calculate the number of points in one period

################ HELPER FUNCTIONS ################

def rephase(phase):
    """rephase(phase) -> phase0

    return the phase without the k*2PI period
    """
    periods=floor(phase / (2 * pi)) #get the number of periods in phase
    return phase - periods * 2 *pi #return the pahse without the periods 

################ FUNCTIONS ################

def fitfunc(params, xdata, ydata):
    """fitfunc(parameters, xdata, ydata) -> ydelta

    return the difference of the ydata and the calculated data using xdata and parameters sequence
    the parameters sequence consists of: [amplitude, frequency, phase]
    """
    return ydata - params[0] * sin(2 * pi * params[1] * xdata + params[2])

def fit_sample(params0, start, length=period_len/4):
    """fit_sample(params0, start, length) -> params

    fits a sample begining at start of specified data point length (defaults to one forth of the period length), including the starting point
    with initial parameters sequence params0 and returns a sequence of obtained parameters
    params and params0 sequence: [amplitude, frequency, phase]
    """
    params, ok = leastsq(fitfunc, params0, args(x[start:start + length], y[start:start + length]))
    if ok > 4 : #if the fitting didn't succeed
        raise RuntimeError 
    else :
        params[2]=rephase(params[2]) #make sure it's the base phase
        if params[0] < 0 : #if the fitting resulted in negative amplitude
            params[2] += pi #add PI to cncel out the fitting to negative amplitude
        return params

################ INITIAL ANALYSIS ################

p0=fit_sample(p0, 0, period_len * start_per) #update the initial parametrs 
