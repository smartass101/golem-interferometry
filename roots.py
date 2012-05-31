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
input_fname='data/160833/ch1.csv'#file with the sine signal, shot 5745 #FIXME this shot has no other DAS data
output_fname="phase-roots.csv"
debug=True
target_sampling_f=25e6 #frequency at which it's the easiest to calculate the roots

################################################################
####              FILE OPENING AND DATA LOADING             ####
################################################################

output_file = open(output_fname, 'w')
if globals().has_key('x'): #want to load data only once, so let's check if it's defined
    print "Data have been loaded already"
else: #first run in session, must load data
    print "Loading data"
    data_file=open(input_fname, 'r') #open data file read-only
    x, y=loadtxt(data_file, delimiter=',', unpack=True) #load and unpack the data
    print "Data loaded"

################################################################
####                  INITIAL ANALYSIS                      ####
################################################################

dt=x[1] - x[0] #calculate the time step
if 1/dt > target_sampling_f: #not the right sampling, resample
    resampler = (1 / dt) / target_sampling_f
    x = x[::resampler]
    y = y[::resampler]
    dt *= resampler
max_distance = 1 / f_base /8 # minimum distance of roots, as a fraction of the period length

################################################################
####                  DATA EXTRACTION                       ####
################################################################
discard_close_roots = True
roots = [] #root array
iterator = nditer((x[1:], y[1:]), flags=['c_index']) #generate an iterator object that will store the index in C order
x_last = x[0]
y_last = y[0]
root = 0
root_last = x[0] * 4
while not iterator.finished:
    if iterator[1] * y_last <= 0:#root found 
        root = iterator[0] - iterator[1] * (iterator[0] - x_last) / (iterator[1] - y_last) #calculate the precise root in between through the secant method
        if discard_close_roots and root - root_last < max_distance: #too close (bad data sample)
            roots[-1] = (root + root_last) / 2 #recalculate the root
        else:
            roots.append(root)
        root_last = root
    x_last, y_last = iterator[0], iterator[1]#:2]
    iterator.iternext()
roots = array(roots)

################################################################
####                 DATA GENERATION                        ####
################################################################

dt = diff(roots) # time steps
w = pi / dt # calculate angular frequencies (1. derivation of phase)
dt = dt[1:] # not using first time step anymore
eps = diff(w) / dt # calculate rate of change of ang. freq. (2. derivation of phase)
w_integr = cumsum(eps) * dt
phase = cumsum(w_integr) * dt #double integral to get phase

output_file.close()

import matplotlib.pylab as plt
axes = plt.subplot(511)
plt.title("Angular frequency (1.derivation of phase)")
plt.plot(roots[1:], w)
axes = plt.subplot(512, sharex=axes)
plt.title("Frequency")
plt.plot(roots[1:], w/2/pi) #frequency
axes = plt.subplot(513, sharex=axes)
plt.title("Rate of chagne of ang. freq. (2. derivation of phase")
plt.plot(roots[2:], eps)
axes = plt.subplot(514, sharex=axes)
plt.title("Integrated ang. freq.")
plt.plot(roots[2:], w_integr)
axes = plt.subplot(515, sharex=axes)
plt.title("Integrated phase")
plt.plot(roots[2:], phase)
plt.show()
