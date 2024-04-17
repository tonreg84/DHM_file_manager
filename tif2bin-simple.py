"""
 Autor: Gernot Scheerer, team UMI, CNP-CHUV Lausanne
 gernot.scheerer@hotmail.de

 this function converts a tiff sequence (data from LynceeTec Koala) into single bin files (LynceeTec format) and applies the famous factor hconv
"""

import binkoala
import os
import tifffile
import numpy

wavelength=665.8

input_file='...test data/aligned.tif' #input_file: filepath of the tiff sequence

timestampsfile='filepath of the Koala timestamps file'

binfolder='...test data/Phase_test' #the bin files will be saved in this folder
os.mkdir(binfolder)

#read timestamps from timestampsfile (int32 array from 3rd column of Koala timestamps file)
with open(timestampsfile, 'r') as infile:
    
    k=0
    timelist=[]
    for line in infile:
        # Split the line into a list of numbers
        numbers = line.split()
        time=numpy.single(float(numbers[3]))
        timelist.append(time)
        k=k+1          
    timestamps=numpy.array(timelist)

nImages=len(timestamps) #sequence length

#get some meta data

#get first image from tiff stack
phase_map = tifffile.imread(input_file, key=0)

w = len(phase_map[0,:])
h = len(phase_map[:,0])

pz=1 #'Please enter the pixel size in meter'

n_1 =1 #'Please enter the first refraction index:'
n_2 =2 #'Please enter the second refraction index:'

hconv=wavelength/(2*3.14159*(n_2-n_1))*10**-9

#write the bin files file
for k in range(nImages):

    #get image k from tiff stack
    phase_map = tifffile.imread(input_file, key=k)/(wavelength/(2*3.14159*(n_2-n_1))) #wavelength/(2*3.14159*(n_1-n_2)) = 1/hcon*10^-9
    
    #write to binfile #i
    output_file_path=binfolder+'/'+str(k).rjust(5, '0')+'_phase.bin'
    
    binkoala.write_mat_bin(output_file_path, phase_map, w, h, pz, hconv, unit_code=1)