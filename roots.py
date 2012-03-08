#!/usr/bin/python2
"""fit the sine signal with a sine function using the least squares method"""


################################################################
####                        IMPORTING                       ####
################################################################

from numpy import pi, loadtxt, savetxt, nditer, empty, array #for loadidng the file and for sin() and rounding, nditer() for looping over data
################################################################
####                        PARAMETERS                      ####
################################################################

f_base=5e5 #the modulation frequency, the base frequency of the sine signal
A_base=0.05 #the expected amplitude of the singal
omega_base = f_base * 2 * pi #base angula frequency of the sine signal
input_fname='data/160833/ch1.csv'#file with the sine signal
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

################################################################
####                  INITIAL ANALYSIS                      ####
################################################################

dt=x[1] - x[0] #calculate the time step
max_distance = 8 / f_base # minimum distance of roots, as a fraction of the period length

################################################################
####                  DATA EXTRACTION                       ####
################################################################

roots = [] #root array
iterator = nditer((x, y), flags=['c_index']) #generate an iterator object that will store the index in C order
x_last = x[0]
y_last = y[0]
root_last = x[0]
while not iterator.finished:
    if iterator[1] * y_last <= 0 and iterator[0] - root_last > max_distance: # root found and is far enough
        root_last = iterator[0] - iterator[1] * (iterator[0] - x_last) / (iterator[1] - y_last) #calculate the precise root in between through the secant method
        roots.append(root_last)
        x_last, y_last = iterator[0:2]
    iterator.iternext()
roots = array(roots)
phase = empty(len(roots) - 1)

################################################################
####                 DATA GENERATION                        ####
################################################################

w_extra = phase[-1,1] / (phase[-1,0] - phase[0,0])

for sample in phase:
    sample[1] += sample[0] * w_extra

savetxt(output_fname, phase)
