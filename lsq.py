#!/usr/bin/python2
"""fit the sine signal with a sine function using the least squares method"""

################ IMPORTING ################

from scipy import pi #used in sin() funcs
from scipy.optimize import leastsq #the least square analyzer
from numpy import loadtxt, sin #for loadidng the file and for sin()

################ PARAMETERS ################

f_base=5e5 #the modulation frequency, the base frequancy of the sine signal
A_base=0.05 #the expected amplitude of the singal
fname='ch1.csv'#file with the sine signal
start_per=5 #how many periods to scan to obtain first approximation of parameters
p0=[A_base, fbase, 0] #initial parameter sequnce to be passed to the leastsq
