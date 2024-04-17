def tiffS2bin(input_file,timestampsfile,wavelength,output_file):
#this function converts a single tiff files into a tiff sequence

#input_file: filepath of one of the single tiff files, tiff file names: XXXXX_phase.tif
#timestampsfile: int32 array from 3rd column of Koala timestamps file
#output_file -> the tiff files will be saved in the folder "output_file_tiff files"

    import os
    from tifffile import imsave
    from tifffile import imread
    import numpy
    import binkoala
    
    import PySimpleGUI as simgui
    
    def is_float(string):
        try:
            float(string)
            return True
        except ValueError:
            return False

    tifffolder=os.path.dirname(input_file)
    
    #create outputfolder -START
    out_file_name, out_file_extension = os.path.splitext(output_file)
    binfolder = out_file_name+'_Bin files'
    #check if binfolder exists aready
    do_it=False
    if os.path.isdir(binfolder)==True:
        checkfolder=simgui.popup_ok_cancel("Output folder exits already!\n\nPress Ok to proceed", "Press cancel to stop",  title="Output folder exits already!")
        if checkfolder=="OK":
            do_it=True
    else:
        do_it=True
        os.mkdir(binfolder)
    
    if do_it==True:
    #create outputfolder -END
    
        #get some meta data
        
        #get first image from the chosen tiff file
        phase_map = imread(input_file, key=0)
        
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
                [simgui.Checkbox("Apply the height conversion factor [\lambda/(2\Pi(n_2-n_1)]^-1.", default=True, font=('Arial Bold', 12), enable_events=True, key='hconvA'),
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
                                hconv4header=wavelength/(6.283185307179586*(n_2-n_1))*10**-9
                                
                                if hconv_win['noconv'].get() == True: hconv=10**-9
                                if hconv_win['hconvA'].get() == True: hconv=wavelength/(6.283185307179586*(n_2-n_1))*10**-9
                                if hconv_win['hconvB'].get() == True: hconv=float(values['hconv'])
                                
                                hconv_check=True
                                hconv_win_check=False
                                
            hconv_win.close()
            
            if hconv_check == True:
            #choice of height conversion factor "hconv" -END
            
                #Progress bar
                ProgLayout = [
                    [simgui.ProgressBar(nImages, orientation='h', expand_x=True, size=(30, 10),  key='prog')],
                    [simgui.Text('Images converted:', key='out', enable_events=True, font=('Arial Bold', 16), justification='center', expand_x=True)]
                ]
                progwin = simgui.Window('File conversion progress', ProgLayout, size=(450, 75))
                event, values = progwin.read(timeout=100)
                
                #write the tiff sequence
                for k in range(nImages):
                    
                    progwin['prog'].update(current_count=k + 1)
                    progwin['out'].update('Images converted: '+str(k + 1)+' of '+str(nImages))
                
                    input_file_path=tifffolder+'/'+str(k).rjust(5, '0')+'_phase.tif'
                    
                    phase_map=imread(input_file_path, key=0)/(hconv*10**9)
                  
                    #write to binfile #k
                    output_file_path=binfolder+'/'+str(k).rjust(5, '0')+'_phase.bin'
                    
                    binkoala.write_mat_bin(output_file_path, phase_map, w, h, pz, hconv4header, unit_code=1)
                    
                progwin.close()
        