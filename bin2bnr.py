def bin2bnr(input_file,timestampsfile,wavelength,output_file):
#this function converts LynceeTec Koala bin files from one folder into a bnr sequence (LynceeTec format)
#the bin files need to end with _00000_phase.bin, _00001_phase.bin, _00002_phase.bin, ..

#input_file : select any of the bin files, you want to convert, it parent folder becomes "binfolder"
#timestampsfile: int32 array from 3rd column of Koala timestamps file
#wavelength of the DHM laser, float32
#output_file: destination of the bnr sequence file

    import os
    import binkoala
    import numpy
    from PySimpleGUI import ProgressBar
    from PySimpleGUI import Text
    from PySimpleGUI import Window
    from PySimpleGUI import popup_get_text
    
    #binfolder='//HOME/ge1582/Mes Documents/09_Python/Env DHM_tools/test data/Phase/Float/Bin'
    #wavelength=666
    #n_1=1
    #n_2=2
    #output_file='//HOME/ge1582/Mes Documents/09_Python/Env DHM_tools/test data/Phase/Float/Bin/output.bnr'
    
    binfolder=os.path.dirname(input_file)
    
    #read timestamps from timestampsfile
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
    n_1 = float(popup_get_text(title='Get n_1', default_text='1', size=(10,10), message='Please enter the first refraction index:'))
    n_2 = float(popup_get_text(title='Get n_2', default_text='2', size=(10,10), message='Please enter the second refraction index:'))
    
    (phase_map,in_file_header)=binkoala.read_mat_bin(input_file)
    w=in_file_header['width'][0]
    h=in_file_header['height'][0]
    pz=in_file_header['px_size'][0]
    
    #write meta data to bnr file
    fileID=open(output_file,'w')
    numpy.array(nImages, dtype=numpy.int32).tofile(fileID)
    numpy.array(w, dtype=numpy.int32).tofile(fileID)
    numpy.array(h, dtype=numpy.int32).tofile(fileID)
    numpy.array(pz, dtype=numpy.float32).tofile(fileID)
    numpy.array(wavelength, dtype=numpy.float32).tofile(fileID)
    numpy.array(n_1, dtype=numpy.float32).tofile(fileID)
    numpy.array(n_2, dtype=numpy.float32).tofile(fileID)
    for k in range(0,nImages):
        numpy.array(timestamps[k], dtype=numpy.float32).tofile(fileID)
    #or timestamps.astype(numpy.int32).tofile(fileID)
    
    #Progress bar
    ProgLayout = [
       [ProgressBar(nImages, orientation='h', expand_x=True, size=(30, 10),  key='prog')],
       [Text('Images converted:', key='out', enable_events=True, font=('Arial Bold', 16), justification='center', expand_x=True)]
    ]
    progwin = Window('File conversion progress', ProgLayout, size=(450, 75))
    event, values = progwin.read(timeout=100)
    
    #write the images of the sequence to bnr file
    for k in range(0,nImages):
        
        progwin['prog'].update(current_count=k + 1)
        progwin['out'].update('Images converted: '+str(k + 1)+' of '+str(nImages))
    
        input_file_path=binfolder+'/'+str(k).rjust(5, '0')+'_phase.bin'
        (phase_map,in_file_header)=binkoala.read_mat_bin(input_file_path)
        
        phase_map.astype(numpy.float32).tofile(fileID)
    
    progwin.close()
    
    fileID.close()