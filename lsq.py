#!/usr/bin/python2
"""fit the sine signal with a sine function using the least squares method"""
debug=False
################ IMPORTING ################

from scipy import pi #used in sin() funcs
from scipy.optimize import leastsq #the least square analyzer
from numpy import loadtxt, sin, floor, empty #for loadidng the file and for sin() and rounding, empty() for data 

################ PARAMETERS ################

f_base=5e5 #the modulation frequency, the base frequancy of the sine signal
A_base=0.05 #the expected amplitude of the singal
fname='sin.csv'#file with the sine signal
output_name='phase.csv'
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

def unpack(line):
    """unpack(line) -> time, value

    Unpack a line from a CSV formatted file and return it as a point pair.
    """
    time, value = line.split(',') #first get the strings
    return float(time), float(value) #make them into floats
    
def update_line(line):
    """update_line(line)

    Push a line from the CSV formatted file into the points_buffer array
    and pop out the last point in the array
    """
    points_buffer.pop(0) #let the last (chronologically speaking, actually it's the first one in the stack)  point go 
    points_buffer.append(unpack(line)) #append the new point list

def update_lines(count):
    """update_lines(count)

    Call :func:`update_line` for the number of lines specified by the integer count argument
    """
    for i in xrange(count):
        update_line(data_file.readline())

def append_lines(count):
    """append_lines(count)

    Similiar to :func:`update_lines`, but does not call pop().
    Used mainly for initial population of the points_buffer array.
    """
    for i in xrange(count):
        points_buffer.append(unpack(data_file.readline())) #append the new point list
        
################ FUNCTIONS ################

def fitfunc(params, xdata, ydata):
    """fitfunc(parameters, xdata, ydata) -> ydelta

    return the difference of the ydata and the calculated data using xdata and parameters sequence
    the parameters sequence consists of: [amplitude, frequency, phase]
    """ 
    return [ y - params[0] * sin(2 * pi * params[1] * x + params[2]) for y in ydata for x in xdata]

def fit_sample(params0):
    """fit_sample(params0) -> params

    fits a sample in the points_buffer arrays with initial parameters sequence params0 and returns a sequence of obtained parameters
    
    params and params0 sequence: [amplitude, frequency, phase]
    """
    params, ok= leastsq(fitfunc, params0, args=(points_buffer[:][0], points_buffer[:][1])) #fit with the points_buffer
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

################ FILE OPENING ################

data_file=open(fname, 'r') #open data file read-only
output_file = open(output_name, 'w') #open output file write-only
points_buffer = [] # initialize an empty list

################ INITIAL ANALYSIS ################

append_lines(2) #for the first two points, to determine dt
dt = points_buffer[1][0] - points_buffer[0][0] #calculate the time step
period_len = round(1 / dt / f_base) #calculate the number of points in one period
fit_distance=int(round(period_len * fit_per_frac)) #max distance of fitted points from root

append_lines(2 * fit_distance - 1) #read in so many lines, so that the points_buffer has a length of 2*fit_distance + 1 point for root (the two last points are subtracted
p0=fit_sample(p0) #update the initial parametrs 
print "Initial parameters [amplitude, frequency, phase]: ",p0

################ DATA GENERATION ################
            
after_root = fit_distance +1  #points filled into points_buffer array after root
# initialized like this so that initially only the last test case is triggered

for line in data_file: #loop over each line in file
    if  after_root < fit_distance: # just adding the points after root
        after_root += 1 #increment filling up
    elif after_root == fit_distance:
        after_root += 1 #increment filling up, to make sure that it jumps to the last test case in next cycle
        p1=fit_sample(p0)
        output_file.write(str(points_buffer[-1 - fit_sample][0]) + ',' + str(p1[2]) + "\n") #write the phase with the time of the root occurrence
    elif points_buffer[-1][1] * points_buffer[-2][1] <= 0: #if not just filling up, check if a root could be between
        after_root = 0 #reset filling
        
    update_line(line) #add the new point
