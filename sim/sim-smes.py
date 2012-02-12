#!/usr/bin/python2


import numpy as np #for ndarray support
import matplotlib.pyplot as plt #for drawings
import scipy.constants as spc #for constants 
#---------PARAMETERS--------
fbase=75e9 #frequency of the microwaves const
fmod=5e5 #modulation frequency 
fmod_band=20e3 #half width of the amplified band
Df=25e6 #modulation amplitude ???const???
samp=1000000  #number of point in simulated sample
dt=1/fbase*20 #time distance between points
p_phase=0#np.pi/6 #constant phase from plasma const
L=spc.c/Df #the length will not change


#TODO TODO
#MAKE IT LIKE THE GEN.PL, THE FBASE CHANGES
#---Func---

#def dispers(t,p):
#    """microwave traveling through plasma and longer dispersion line
#
#    The phase p is given by plasma,
#    frequcny is smaller by fmod in comp with refline(), but this is implemented in refline
#    to make sure freq won't go under fbas"""
#    return np.sin(t*2*np.pi*fbase+p)
#def refline(t,f_mod):
#    """microwave traveling through short refline
#
#    frequency is bigger by fmod in comparison with dispers(), calculated by cross multiplication
#    T=1/fmod ... Df
#    t=L/c ... x=fmod"""
#    return np.sin(t*2*np.pi*(fbase+L*Df*f_mod/spc.c)

#-----DATA GEN ----
#data=np.empty((smap,2)) #data array: first (for resource ecology) [time, freq] -> [time,amplitude]
time=np.linspace(0,samp*dt,samp) #time data generation
freq=np.empty(samp)#freq data gen container
freq[:]=fmod #assign value
freq[500000:600000]=5.1e5
#PLACEHOLDER Df could have a data space too, if it is expected to change
freq_d=np.empty(samp) #freq data for the fbase for dispersion line
freq_r=np.empty(samp) #freq data for the fbase for refline
#f1=dispers #store functions as objects, to call them less often
#f2=refline

#for row in data: #generate sine wave interf data
#    row[1]=f1(row[0],phase)+f2(row[0],row[1])
#phases=[]
#for i in range(1,samp-2): #find places with lowest amplitude...root points
#    if(np.abs(data[i-1,1])>np.abs(data[i,1]) and np.abs(data[i,1])<np.abs(data[i+1,1]):
#        data[i,0] #and multiply it by fmod or freq ???

#-----SAW-TOOTH DATA freq GEN-----
f_d=fbase
f_r=fbase+L/spc.c*Df*freq[1] #initial freq refline is ahead freq dispers
for i in xrange(samp):
    df_saw=Df*dt*freq[i] #calculate freq mod diff in step
    f_r+=df_saw
    if(f_r>=fbase+Df): #if modulation peak reached
            f_r=fbase
    f_d+=df_saw
    if(f_d>=fbase+Df): #if modulation peak reached
            f_d=fbase
    freq_d[i]=f_d
    freq_r[i]=f_r

#-----MIXING DIODE-----
mixer=np.sin(time*2*np.pi*freq_r)+np.sin(time*2*np.pi*freq_d+p_phase) #refline()+dispers()
#plt.plot(time[:],mixer[:])
#plt.show()

#------SELECTIVE FREQ AMPLIFY----
fft=np.fft.rfft(mixer) #approximated through FFT for real values 
ffq=np.fft.fftfreq(samp,dt) #frequency spectrum
amp=np.where((ffq>=fmod-fmod_band) & (ffq<=fmod+fmod_band))[0] #find indices for freq band
amp_fft=fft[amp] #store the band
fft[:]=0 #cut off all other freqs
fft[amp]=amp_fft #put back freq band
#fft[amp[len(amp)/2]]*=1000 #extra amplification of center band
mix2=np.fft.irfft(fft) #inverse , clean data
#plt.plot(time,mix2)
#plt.show()

