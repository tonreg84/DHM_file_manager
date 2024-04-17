def tif2bnr(input_file,timestampsfile,wavelength,output_file):
#this function converts a tiff sequence (data from LynceeTec Koala) into a bnr sequence (LynceeTec format)

#input_file: filepath of the tiff sequence
#timestampsfile: int32 array from 3rd column of Koala timestamps file
#output_file: destination of the bnr sequence file

    import numpy
    import tifffile
    
    import PySimpleGUI as simgui
    
    def is_float(string):
        try:
            float(string)
            return True
        except ValueError:
            return False
    
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
    
   #get some meta data:
    
    #get first image from tiff stack
    phase_map = tifffile.imread(input_file, key=0)
    w = len(phase_map[0,:])
    h = len(phase_map[:,0])
    
    #get pixel size and check if entry is a floating point number -START
    pz_string=simgui.popup_get_text(title='Get pixel size', default_text='1.1520307e-06', size=(10,10), message='Please enter the pixel size in meter (default value for 5X):')
    
    if pz_string==None:
        print("Conversion cancelled.")
    elif is_float(pz_string) == False:
        simgui.popup_auto_close('Error: No floating point number given for pixel size.')
    else:
        pz=float(pz_string)
    #get pixel size and check if entry is a floating point number -END
    
        #choice of height conversion factor "hconv" -START
            # first make the popup window
        Layout = [
            [simgui.Text('Please enter the first refraction index n_1:',font=('Arial Bold', 12)),
             simgui.In(size=(50, 1), default_text='1', enable_events=True, key="n_1")
             ],
            [simgui.Text('Please enter the second refraction index n_2:',font=('Arial Bold', 12)),
             simgui.In(size=(50, 1), default_text='2', enable_events=True, key="n_2")
             ],
            [
            simgui.Text("   "),
            ],
            [simgui.Checkbox("Do not apply the height conversion factor.", font=('Arial Bold', 12), enable_events=True, key='noconv'),
             ],
            [simgui.Checkbox("Apply the height conversion factor wavelength*(2Pi(n_2-n_1)^-1.", default=True, font=('Arial Bold', 12), enable_events=True, key='hconvA'),
             ],
            [simgui.Checkbox("Apply the manual height conversion factor:", font=('Arial Bold', 12), enable_events=True, key='hconvB'),
             simgui.In(size=(50, 1), enable_events=True, key="hconv")
             ],
            [
            simgui.Text("   "),
            ],
            [simgui.Ok(key="ok"), simgui.Button(button_text='Cancel', enable_events=True, key="cancel-button")],
        ]
        hconv_win = simgui.Window('Refraction indices and conversion factor', Layout, size=(500, 250))
        
        #open the popup window and check the entries
        hconv=10**-9
        hconv_check=False
        hconv_win_check=True
        while hconv_win_check==True:
            event, values = hconv_win.read()
            
            if event == simgui.WIN_CLOSED:
                hconv_win_check=False
            
            if event == 'cancel-button':
                hconv_check=False
                hconv_win_check=False
            
            if event == 'noconv':
                if hconv_win['noconv'].get() == True:
                    hconv_win['hconvA'].update(value=False)
                    hconv_win['hconvB'].update(value=False)
            if event == 'hconvA':
                if hconv_win['hconvA'].get() == True:
                    hconv_win['noconv'].update(value=False)
                    hconv_win['hconvB'].update(value=False)
            if event == 'hconvB':
                if hconv_win['hconvB'].get() == True:
                    hconv_win['noconv'].update(value=False)
                    hconv_win['hconvA'].update(value=False)
        
            if event == 'ok':
                if values['n_1']=='' or values['n_2'] == '':
                    simgui.popup_auto_close('Error: refraction index missing.')
                elif is_float(values['n_1'])==False or is_float(values['n_2'])==False:
                    simgui.popup_auto_close('Error: Please enter floating point numbers only.')
                else:
                    if hconv_win['noconv'].get() == False and hconv_win['hconvA'].get() == False and hconv_win['hconvB'].get() == False:
                        simgui.popup_auto_close('Error: Please select an option for the conversion factor.')
                    else:
                        if hconv_win['hconvB'].get() == True and values['hconv']=='':
                            simgui.popup_auto_close('Error: Please enter a manual conversion factor.')
                        elif is_float(values['hconv'])==False and hconv_win['hconvB'].get() == True:
                            simgui.popup_auto_close('Error: Please enter floating point numbers only.')
                        else:
                            
                            n_1=float(values['n_1'])
                            n_2=float(values['n_2'])
                            
                            if hconv_win['noconv'].get() == True: hconv=10**-9
                            if hconv_win['hconvA'].get() == True: hconv=wavelength/(6.283185307179586*(n_2-n_1))*10**-9
                            if hconv_win['hconvB'].get() == True: hconv=float(values['hconv'])
                            
                            hconv_check=True
                            hconv_win_check=False
                            
        hconv_win.close()
        
        if hconv_check == True:
        #choice of height conversion factor "hconv" -END
        
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
                [simgui.ProgressBar(nImages, orientation='h', expand_x=True, size=(30, 10),  key='prog')],
                [simgui.Text('Images converted:', key='out', enable_events=True, font=('Arial Bold', 16), justification='center', expand_x=True)],
            ]
            progwin = simgui.Window('File conversion progress', ProgLayout, size=(450, 75))
            event, values = progwin.read(timeout=100)
            
            #write images to bnr file
            for k in range(0,nImages):
                
                progwin['prog'].update(current_count=k + 1)
                progwin['out'].update('Images converted: '+str(k + 1)+' of '+str(nImages))
                        
                phase_map = tifffile.imread(input_file, key=k)/(hconv*10**9) #wavelength/(2*Pi*(n_1-n_2))*10**-9 = hconv
                
                phase_map.astype(numpy.float32).tofile(fileID)
            
            progwin.close()
            
            fileID.close()