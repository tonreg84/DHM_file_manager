def bnr2bin(input_file,timestampsfile,wavelength,output_file):
#this function converts LynceeTec Possum bnr sequence to single bin files (LynceeTec format)

#input_file: filepath of the bnr sequence
#timestampsfile: int32 array from 3rd column of Koala timestamps file
#output_file -> the bin files will be saved in the folder "output_file_Bin files

    import os
    import numpy
    import binkoala
    
    import PySimpleGUI as simgui
    
    #create outputfolder -START
    out_file_name, out_file_extension = os.path.splitext(output_file)
    binfolder = out_file_name+'_Bin files'
    #check if binfolder exists aready
    do_it=False
    if os.path.isdir(binfolder)==True:
        checkfolder=simgui.popup_ok_cancel("Output folder exits already!\nPress Ok to proceed", "Press cancel to stop",  title="Output folder exits already!")
        if checkfolder=="OK":
            do_it=True
    else:
        do_it=True
        os.mkdir(binfolder)
    
    if do_it==True:
    #create outputfolder -END
    
        #get data from bnr file
        
        fileID = open(input_file, 'rb')
        
        #get header
        nImages = numpy.fromfile(fileID, dtype="i4", count=1)
        nImages = nImages[0]
        w = numpy.fromfile(fileID, dtype="i4", count=1)
        w=w[0]
        h = numpy.fromfile(fileID, dtype="i4", count=1)
        h=h[0]
        pz = numpy.fromfile(fileID, dtype="f4", count=1)
        pz=pz[0]
        wavelength_placeholder = numpy.fromfile(fileID, dtype="f4", count=1)
        n_1_placeholder = numpy.fromfile(fileID, dtype="f4", count=1)
        n_2_placeholder = numpy.fromfile(fileID, dtype="f4", count=1)
    
        n_1 = float(simgui.popup_get_text(title='Get n_1', default_text='1', size=(10,10), message='Please enter the first refraction index:'))
        n_2 = float(simgui.popup_get_text(title='Get n_2', default_text='2', size=(10,10), message='Please enter the second refraction index:'))    
    
        hconv=numpy.single(wavelength/(2*3.14159*(n_2-n_1))*10**-9)
        
        #timestamps = numpy.fromfile(fileID, dtype="i4", count=nImages)
        timestamps = [0] * nImages
        for k in range(0,nImages):
            timestamps[k] = numpy.fromfile(fileID, dtype="i4", count=1)
        
        phase_map = numpy.zeros((h,w))
        
        #Progress bar
        ProgLayout = [
            [simgui.ProgressBar(nImages, orientation='h', expand_x=True, size=(30, 10),  key='prog')],
            [simgui.Text('Images converted:', key='out', enable_events=True, font=('Arial Bold', 16), justification='center', expand_x=True)]
        ]
        progwin = simgui.Window('File conversion progress', ProgLayout, size=(450, 75))
        event, values = progwin.read(timeout=100)
        
        #write the bin files file
        for i in range(nImages):
            
            progwin['prog'].update(current_count=i + 1)
            progwin['out'].update('Images converted: '+str(i + 1)+' of '+str(nImages))
        
            #get image k from sequence
            for k in range(h):
                
                phase_map[k,:] = numpy.fromfile(fileID, dtype="f4", count=w)
            
            phase_map=numpy.single(phase_map)
            
            #write to binfile #i
            output_file_path=binfolder+'/'+str(i).rjust(5, '0')+'_phase.bin'
            
            binkoala.write_mat_bin(output_file_path, phase_map, w, h, pz, hconv, unit_code=1)
            
        progwin.close()
        fileID.close