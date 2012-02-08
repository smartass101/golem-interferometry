#!/usr/bin/python2
"""fit the sine signal with a sine function using the least squares method"""


################################################################
####                        IMPORTING                       ####
################################################################

from scipy import pi #used in sin() funcs
from numpy import loadtxt, nditer #for loadidng the file and for sin() and rounding, nditer() for looping over data
################################################################
####                        PARAMETERS                      ####
################################################################

f_base=5e5 #the modulation frequency, the base frequancy of the sine signal
A_base=0.05 #the expected amplitude of the singal
input_fname='sin.csv'#file with the sine signal
output_fname="phase-roots.csv"
debug=True

################################################################
####              FILE OPENING AND DATA LOADING             ####
################################################################

data_file=open(input_fname, 'r') #open data file read-only
if globals().has_key('x'): #want to load data only once, so let's check if it's defined
    print "Data have been loaded already"
else: #first run in session, must load data
    x, y=loadtxt(data_file, delimiter=',', unpack=True) #load and unpack the data
    print "Data loaded"

output_file = open(output_fname, 'w')

################################################################
####                  INITIAL ANALYSIS                      ####
################################################################

dt=x[1] - x[0] #calculate the time step
max_distance = 8 / f_base # minimum distance of roots, as a fraction of the period length

################################################################
####                  DATA GENERATION                       ####
################################################################

roots = 0 #root count
phase_integr = 0 #phase calculated by integrating phace changes
t = 0 # occurrence of the current root
t_last = 0 #storing occurrence of the last root
t_first = 0 #occurrence of the first root
iterator = nditer(y, flags=['c_index']) #generate an iterator object that will store the index in C order
D_phase = 0 #calculated phase change
phase = 0 #calculated phase
try: #will catch IndexError on last point
    while not iterator.finished :
        if  iterator[0] * y[iterator.index + 1] <= 0: # root found
            if x[iterator.index + 1] - x[iterator.index] > max_distance: #roots too far
                continue #TODO or could use this second "root" to calculate an even more precise root occurence
            else: #seems to be a legit root
                roots += 1
                t = x[iterator.index +1] - y[iterator.index +1] * (x[iterator.index +1] - x[iterator.index]) / (y[iterator.index +1] - y[iterator.index]) #calculate the precise root in between through the secant method
                if roots > 1:
                    D_phase = pi - f_base * (t - t_last) #phase change
                    phase_integr += D_phase #integrate
                    if D_phase < 0: #implies that a whole period was skipped
                        roots += 1
                    phase = (roots-1) * pi - f_base * (t - t_first)
                    output_file.write("{:e},{:e},{:e}\n".format(t, phase, phase_integr)) #write to output file as CVS format
                elif roots == 1: #this is the first root occurrence
                    t_first = t
                else: #that would be strange as the root count is incremented before this
                    raise RuntimeError("root count out of range: {:d} maybe integer overrun -- too many roots?".format(roots))
                t_last = t #store for future use
        iterator.iternext() #DO NOT forget this
except IndexError:
    pass #this is expected
    
