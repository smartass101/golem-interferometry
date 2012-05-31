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

data_file=open(input_fname, 'r') #open data file read-only
output_file = open(output_fname, 'w')
if globals().has_key('x'): #want to load data only once, so let's check if it's defined
    print "Data have been loaded already"
else: #first run in session, must load data
    print "Loading data"
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

################ FIRST PASS ################
D_root = (roots[-1] - roots[0]) / roots.size#better approximation
phase = empty(len(roots) - 2)
iterator = nditer((roots[2:], phase), ['c_index'], [['readonly'], ['readwrite']])
t_expected = roots[1] + D_root
w_base = pi / D_root

while not iterator.finished:
    iterator[1] = (t_expected - iterator[0]) * w_base
    t_expected += D_root * int((iterator[0] - t_expected ) / D_root) #add the right number of D_roots a there could have been some weird phase shift
    iterator.iternext()

################ SECOND PASS ################
edge = int(3e-3 / D_root) #expecting no plasma up to 3 ms
w_extra = (phase[edge] - phase[0]) / (roots[edge] - roots[2])
phase_0 = roots[2] * w_extra
phase -= roots[2:] * w_extra - phase_0 #easier
iterator = nditer((roots[2:], phase), ['c_index'], [['readonly'], ['readwrite']])
while not iterator.finished:
    #iterator[1] += iterator[0] * w_base - phase_0
    #output_file.write("{},{}\n".format(iterator[0], iterator[1]))
    iterator.iternext()


data_file.close()
output_file.close()

import matplotlib.pylab as plt
plt.plot(roots[2:], phase)
plt.show()
