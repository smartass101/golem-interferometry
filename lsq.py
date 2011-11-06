#!/usr/bin/python2
"""fit the sine signal with a sine function using the least squares method"""

################ IMPORTING ################

from scipy import pi #used in sin() funcs
from scipy.optimize import leastsq #the least square analyzer
from numpy import loadtxt, sin #for loadidng the file and for sin()
