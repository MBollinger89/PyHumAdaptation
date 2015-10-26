#!/usr/bin/python
import PyHum

import numpy as np

import matplotlib.pyplot as plt

import os

from scipy.io import loadmat

import sys

import sonar_file_path as sfp
import platform

#=================================================
# Read sonar data. Do it first
def read_sondata(hmf,sonDir,c1,f1,model1,chunk1):
    PyHum.read(hmf,sonDir,c=c1,f=f1,model=model1,chunk=chunk1)


#=================================================
# correct scans
def correct(humfiles,sonpath,cww):
    PyHum.correct(humfiles,sonpath,correct_withwater=cww)

    
#=================================================
# Define a function to put chunks together and crop by depth 
def custom_save(figdirec,root):
    # Save the figure
    plt.savefig(os.path.normpath(os.path.join(figdirec,root)),bbox_inches='tight',dpi=800)

#=================================================


#=================================================


def process(humfile,sonpath,depth):
    # Process the chunks and crop

    # if son path name supplied has no separator at end, put one on
    maxy = depth
    print 'Crop size '+str(maxy)+' meters'
    if sonpath[-1]!=os.sep:
        sonpath = sonpath + os.sep


    base = humfile.split('.DAT') # get base of file name for output

    base = base[0].split(os.sep)[-1]



    # remove underscores, negatives and spaces from basename

    if base.find('_')>-1:

        base = base[:base.find('_')]

    if base.find('-')>-1:

        base = base[:base.find('-')]

    if base.find(' ')>-1:

	base = base[:base.find(' ')]

    if base.find('.')>-1:
        base = base[:base.find('.')]

    

    #load metadata file in
    
    meta = loadmat(os.path.normpath(os.path.join(sonpath,base+'meta.mat')))

    shape_port = np.squeeze(meta['shape_port'])
    shape_star = np.squeeze(meta['shape_star'])

    with open(os.path.normpath(os.path.join(sonpath,base+'_data_port_lw.dat')), 'r') as ff:
        port_fpw = np.memmap(ff, dtype='float32', mode='r', shape=tuple(shape_port))
	
    with open(os.path.normpath(os.path.join(sonpath,base+'_data_star_lw.dat')), 'r') as ff:
        star_fpw = np.memmap(ff, dtype='float32', mode='r', shape=tuple(shape_star))

    Zdist = meta['dist_m']
    extent = shape_port[0]
    ft = np.squeeze(1/meta['pix_m'])

    fig = plt.figure()
    plt.imshow(np.vstack((np.flipud(port_fpw), star_fpw)), cmap='gray', extent=[np.min(Zdist), np.max(Zdist), -extent*(1/ft), extent*(1/ft)])
    plt.ylabel('Range (m)'), plt.xlabel('Distance along track (m)')

    plt.axis('normal'); plt.axis('tight')
    plt.ylim(-maxy, maxy)

    imagepath = os.path.basename(humfile)
    imagename = os.path.splitext(imagepath)[0]


    plt.savefig(os.path.normpath(os.path.join(sonpath,imagename+'.png')),bbox_inches='tight',dpi=800)
    del fig
    

    print 'image name =', imagename
        
   

if __name__=="__main__":
    
    if len(sys.argv)==1:
        dataName = raw_input("please put your data set name\n")
        depth = raw_input("please put the depth of the water in meters\n")
        #dist = raw_input ("please put the distance of the scan in meteres\n")
        
    elif len(sys.argv)==2 and sys.argv[1].isdigit():
        distFlag = raw_input("Is this the distance of your scan? (yes/no)")
        
        #if distFlag.upper()=='YES' or distFlag.upper()=='Y':
        #    depth = raw_input("please put the depth of the water in meters\n")
        #    dist = sys.argv[1]

        #elif distFlag.upper()=='NO' or distFlag.upper()=='N':
        #    #dist = raw_input ("please put the distance of the scan in meteres\n")
        #    depth = sys.argv[1]
            
        dir=raw_input("please put your directory path\n")
        
        
    elif  len(sys.argv)==2 and not sys.argv[1].isdigit():
        depth = raw_input("please put the depth of the water in meters\n")
        #dist = raw_input ("please put the distance of the scan in meteres\n")
        dir = sys.argv[1]
    
    else:
        #dist = sys.argv[3]
        
        depth = sys.argv[2]

        dir = sys.argv[1]
        
    depth = float(depth)
    if platform.system()=='Windows':
        pathfile = 'filepathWin.txt' 
    elif platform.system()=='Darwin':
        pathfile = 'filepathMac.txt'
    else:
        raise OSError('Unknown operating system')

    dir = sfp.find_path(dataName,pathfile)
    humfiles = [each for each in os.listdir(dir) if each.endswith('.DAT')]
    if not dir[-2:]==os.sep:
        dir=dir+os.sep 
    
    humfiles = [dir+fname for fname in humfiles]
    
    sonDir = [filename[:-4] for filename in humfiles ]

    #Read Parameters
    c1 = 1560 # speed of sound Salt water (m/s)
    f1 = 455 # frequency kHz of sidescan sonar
    model1 = 1198 # humminbird model
    chunk1 = 1
    
    
    # Correct Parameters
    cww = 1 #correct with water; 0=No water, 1=water
    
    
    testFlag = raw_input("Is this a testing run?(yes/no)")
   
    #For Single File test.....
    if testFlag.upper()=='YES' or testFlag.upper()=='Y':
        print "Runing test for file "+humfiles[0]
        mat = [each for each in os.listdir(sonDir[0]) if each.endswith('.mat')]
        if mat ==[]:
            print "Read data first!"
            print "Reading....."  
            read_sondata(humfiles[0],sonDir[0],c1,f1,model1,chunk1)
            print "Finish reading"
            
        print "Correcting : "+humfiles[0]
        correct(humfiles[0],sonDir[0],cww)
        print "Finished Correcting"
        
        print "Processing : "+humfiles[0]
        process(humfiles[0],sonDir[0],depth)
    
    elif testFlag.upper()=='NO' or testFlag.upper()=='N':
        #For all files in directory, use.....
        for humf,sonD in zip(humfiles,sonDir):
            print "Start Process humfile:"+humf
            print "Read file :"+humf
            read_sondata(humf,sonD,c1,f1,model1,chunk1)
        
	    print "Correcting : "+humf
            correct(humf,sonD,cww)
            print "Finished Correcting"  

    	    process(humf,sonD,depth)
            print "Processing for Humfile:"+ humf +" finished."
    else:
        print "Unknown input! bye!"
        sys.exit(0)

    print "All done. Beer!"

