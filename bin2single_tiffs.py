def bin2tiffS(input_file,timestampsfile,wavelength,output_file):
#this function converts a tiff sequence into single tiff files

#input_file: filepath of one of the bin files
#timestampsfile: int32 array from 3rd column of Koala timestamps file
#output_file -> the tiff files will be saved in the folder "output_file_tiff files"

    import os
    import binkoala
    from tifffile import imsave
    import numpy
    
    import PySimpleGUI as simgui
    
    def is_float(string):
        try:
            float(string)
            return True
        except ValueError:
            return False
    
    binfolder=os.path.dirname(input_file)
    
    #create outputfolder -START
    out_file_name, out_file_extension = os.path.splitext(output_file)
    tifffolder = out_file_name+'_tiff files'
    #check if tifffolder exists aready
    do_it=False
    if os.path.isdir(tifffolder)==True:
        checkfolder=simgui.popup_ok_cancel("Output folder exits already!\nPress Ok to proceed", "Press cancel to stop",  title="Output folder exits already!")
        if checkfolder=="OK":
            do_it=True
    else:
        do_it=True
        os.mkdir(tifffolder)
    
    if do_it==True:
    #create outputfolder -END
    
        #choice of conversion factor -START
        # first make the popup window
        Layout = [
            [simgui.Checkbox("Do not apply a conversion factor.", default=True, font=('Arial Bold', 12), enable_events=True, key='nofact'),
             ],
            [simgui.Checkbox("Conversion from rad to degree: x360/2\Pi.", font=('Arial Bold', 12), enable_events=True, key='pifact'),
             ],
            [simgui.Checkbox("Apply the height conversion factor wavelength*(2Pi(n_2-n_1)^-1.", font=('Arial Bold', 12), enable_events=True, key='hconv'),
             ],
            [simgui.Checkbox("Apply the manual conversion factor:", font=('Arial Bold', 12), enable_events=True, key='manfact'),
             simgui.In(size=(50, 1), enable_events=True, key="manual_factor")
             ],
            [
            simgui.Text("   "),
            ],
            [simgui.Ok(key="ok"), simgui.Button(button_text='Cancel', enable_events=True, key="cancel-button")],
            ]
        conv_fact_win = simgui.Window('Choice of conversion factor', Layout, size=(550, 250))
        
        #open the popup window and check the entries
        fact_check=False
        fact_win_check=True
        while fact_win_check==True:
            event, values = conv_fact_win.read()
            
            if event == simgui.WIN_CLOSED:
                fact_win_check=False
            
            if event == 'cancel-button':
                fact_check=False
                fact_win_check=False
            
            if event == 'nofact':
                if conv_fact_win['nofact'].get() == True:
                    conv_fact_win['pifact'].update(value=False)
                    conv_fact_win['hconv'].update(value=False)
                    conv_fact_win['manfact'].update(value=False)
            if event == 'pifact':
                if conv_fact_win['pifact'].get() == True:
                    conv_fact_win['nofact'].update(value=False)
                    conv_fact_win['hconv'].update(value=False)
                    conv_fact_win['manfact'].update(value=False)
            if event == 'hconv':
                if conv_fact_win['hconv'].get() == True:
                    conv_fact_win['nofact'].update(value=False)
                    conv_fact_win['pifact'].update(value=False)
                    conv_fact_win['manfact'].update(value=False)
            if event == 'manfact':
                if conv_fact_win['manfact'].get() == True:
                    conv_fact_win['nofact'].update(value=False)
                    conv_fact_win['hconv'].update(value=False)
                    conv_fact_win['pifact'].update(value=False)
        
            if event == 'ok':
                
                if conv_fact_win['nofact'].get() == False and conv_fact_win['pifact'].get() == False and conv_fact_win['hconv'].get() == False and conv_fact_win['manfact'].get() == False:
                    simgui.popup_auto_close('Error: Please select an option for the conversion factor.')
                else:
                    if conv_fact_win['manfact'].get() == True:
                        if values['manual_factor'] == '':
                            simgui.popup_auto_close('Error: Manual conversion factor missing.')
                        elif is_float(values['manual_factor'])==False:
                            simgui.popup_auto_close('Error: Please enter floating point numbers only.')
                        else:
                            conversion_factor=float(values['manual_factor'])
                            fact_win_check=False
                            fact_check=True
                            
                    elif conv_fact_win['pifact'].get() == True:
                        conversion_factor=360/6.283185307179586
                        fact_win_check=False
                        fact_check=True                        
                        
                    elif conv_fact_win['hconv'].get() == True:
                        (in_file_image,in_file_header)=binkoala.read_mat_bin(input_file)
                        conversion_factor=in_file_header['hconv'][0]
                        fact_win_check=False
                        fact_check=True
                    
                    else:
                        conversion_factor=None
                        fact_win_check=False
                        fact_check=True
                        
        conv_fact_win.close()
        
        if fact_check == True:
        #choice of conversion factor -END

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
            
            #Progress bar
            ProgLayout = [
                [simgui.ProgressBar(nImages, orientation='h', expand_x=True, size=(30, 10),  key='prog')],
                [simgui.Text('Images converted:', key='out', enable_events=True, font=('Arial Bold', 16), justification='center', expand_x=True)]
            ]
            progwin = simgui.Window('File conversion progress', ProgLayout, size=(450, 75))
            event, values = progwin.read()
            
            #write the tiff files file
            for k in range(0,nImages):
                
                progwin['prog'].update(current_count=k + 1)
                progwin['out'].update('Images converted: '+str(k + 1)+' of '+str(nImages))
            
                input_file_path=binfolder+'/'+str(k).rjust(5, '0')+'_phase.bin'
                (phase_map,in_file_header)=binkoala.read_mat_bin(input_file_path)
                
                if conversion_factor != None:
                    phase_map=phase_map*conversion_factor
            
                #write to tiff file #k
                output_file_path=tifffolder+'/'+str(k).rjust(5, '0')+'_phase.tif'
                
                imsave(output_file_path, phase_map, photometric='minisblack', compression=5, append=True, bitspersample=32, planarconfig=1, subfiletype=3)
                
            progwin.close()