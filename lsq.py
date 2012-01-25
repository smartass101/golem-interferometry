#!/usr/bin/python2
"""fit the sine signal with a sine function using the least squares method"""
debug=True
################ IMPORTING ################

from scipy import pi #used in sin() funcs
from scipy.optimize import leastsq #the least square analyzer
from numpy import loadtxt, sin, floor, nditer #for loadidng the file and for sin() and rounding, nditer() for looping over data

################ PARAMETERS ################

f_base=5e5 #the modulation frequency, the base frequancy of the sine signal
A_base=0.05 #the expected amplitude of the singal
input_fname='sin.csv'#file with the sine signal
start_per=5 #how many periods to scan to obtain first approximation of parameters
fit_per_frac= 1./4 #maximum time distance from root to points in fitted sample given by the fraction of the period
p0=[A_base, f_base, 0] #initial parameter sequnce to be passed to the leastsq

################ HELPER FUNCTIONS ################

def rephase(phase):
    """rephase(phase) -> phase0

    Return the phase without the k*2PI period.

    The phase is expected to be in radians.
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

def fit_sample(params0, start, length):
    """fit_sample(params0, start, length) -> params

    fits a sample begining at start of specified data point length, including the starting point
    with initial parameters sequence params0 and returns a sequence of obtained parameters
    params and params0 sequence: [amplitude, frequency, phase]
    """
    params, ok= leastsq(fitfunc, params0, args=(x[start:start + length], y[start:start + length]))
    if ok > 4 : #if the fitting didn't succeed
        raise RuntimeError("fit exited with error "+str(ok)+" at fit from point "+str(start)+" to "+str(length))
    else :
        params[2]=rephase(params[2]) #make sure it's the base phase
        if params[0] < 0 : #if the fitting resulted in negative amplitude
            params[0] *= -1 #negate the amplitude
            if params[2] < pi: 
                params[2] += pi #add PI to cancel out the fitting to negative amplitude
            else: #phase is greater than PI
                params[2] -= pi #substract pi to cansel out negative amplitude
        return params

################ DEBUGGING WRAPPERS ################

if debug:
    import matplotlib.pyplot as plt
    def compare_fit(start,length):
        plt.plot(x[start:start + length], y[start:start + length], 'r+')
        parms=fit_sample(p0,start,length)
        plt.plot(x[start:start + length], y[start:start + length] - fitfunc(parms,x[start:start + length], y[start:start + length] ) , 'b+')
        plt.show()

################ FILE OPENING AND DATA LOADING ################

data_file=open(input_fname, 'r') #open data file read-only
if globals().has_key('x'): #want to load data only once, so let's check if it's defined
    print "Data have been loaded already"
else: #first run in session, must load data
    x, y=loadtxt(data_file, delimiter=',', unpack=True) #load and unpack the data
    print "Data loaded"

################ INITIAL ANALYSIS ################

dt=x[1] - x[0] #calculate the time step
period_len=round(1 / dt / f_base) #calculate the number of points in one period
p0=fit_sample(p0, 0, period_len * start_per) #update the initial parametrs 
fit_distance=int(round(period_len * fit_per_frac)) #max distance of fitted points from root
print "Initial parameters [amplitude, frequency, phase]: ",p0

################ DATA GENERATION ################



iterator = nditer(y, flags=['c_index']) #generate an iterator object that will store the index in C order
maxidx_y = len(y) -1 #use a static value, so len() is not called so often
while not iterator.finished : #until we find them all
    if iterator.index < maxidx_y and iterator[0] * y[iterator.index + 1] <= 0: # root found, the previous check is a cut-off safety check for index overflow
        p1 = fit_sample(p0, iterator.index))
