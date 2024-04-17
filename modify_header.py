def modify_header(binfolder):
    
    import PySimpleGUI as simgui
    import os
    import binkoala
    import numpy
    
    def is_float(string):
        try:
            float(string)
            return True
        except ValueError:
            return False
    
    #get header info and update window
    in_file=binfolder+'/00000_phase.bin'
    (phase_map,file_header)=binkoala.read_mat_bin(in_file)
    hv_in=str(file_header['version'][0])
    end_in=str(file_header['endian'][0])
    hz_in=str(file_header['head_size'][0])
    w_in=str(file_header['width'][0])
    h_in=str(file_header['height'][0])
    pz_in=str(file_header['px_size'][0])
    hconv_in=str(file_header['hconv'][0])
    uc_in=str(file_header['unit_code'][0])
    
    # header_mod_win['hv_in'].update(value=hv_in)
    # header_mod_win['end_in'].update(value=end_in)
    # header_mod_win['hz_in'].update(value=hz_in)
    # header_mod_win['w_in'].update(value=w_in)
    # header_mod_win['h_in'].update(value=h_in)
    # header_mod_win['pz_in'].update(value=pz_in)
    # header_mod_win['hconv_in'].update(value=hconv_in)
    # header_mod_win['uc_in'].update(value=uc_in)
    
    HMLayout = [
        [   simgui.Text("Which elements of the header do you want to change?", font=('Arial Bold', 14)),
        ],
        [simgui.Text("                              ", font=('Arial Bold', 12)),
         ],
        [   simgui.Text("                              ", font=('Arial Bold', 12)),
            simgui.Text("Current header", font=('Arial Bold', 12)),simgui.Text("       ", font=('Arial Bold', 12)),
            simgui.Text("Replace with", font=('Arial Bold', 12)),
        ],
        # [   simgui.Text("Header version    ", font=('Arial Bold', 12)),
        #     simgui.In(size=(15, 1), enable_events=True, key="hv_in", default_text=hv_in),simgui.Text("      ", font=('Arial Bold', 12)),
        #     simgui.In(size=(15, 1), enable_events=True, key="hv_out,")
        # ],
        # [   simgui.Text("Endiannes         ", font=('Arial Bold', 12)),
        #     simgui.In(size=(15, 1), enable_events=True, key="end_in", default_text=end_in),simgui.Text("      ", font=('Arial Bold', 12)),
        #     simgui.In(size=(15, 1), enable_events=True, key="end_out,")
        # ],
        # [   simgui.Text("Header size         ", font=('Arial Bold', 12)),
        #     simgui.In(size=(15, 1), enable_events=True, key="hz_in", default_text=hz_in),simgui.Text("      ", font=('Arial Bold', 12)),
        #     simgui.In(size=(15, 1), enable_events=True, key="hz_out,")
        # ],
        [   simgui.Text("Image width          ", font=('Arial Bold', 12)),
            simgui.In(size=(15, 1), enable_events=True, key="w_in", default_text=w_in),simgui.Text("      ", font=('Arial Bold', 12)),
            simgui.In(size=(15, 1), enable_events=True, key="w_out"),
        ],
        [   simgui.Text("Image hight         ", font=('Arial Bold', 12)),
            simgui.In(size=(15, 1), enable_events=True, key="h_in", default_text=h_in),simgui.Text("      ", font=('Arial Bold', 12)),
            simgui.In(size=(15, 1), enable_events=True, key="h_out"),
        ],
        [   simgui.Text("Pixel size            ", font=('Arial Bold', 12)),
            simgui.In(size=(15, 1), enable_events=True, key="pz_in", default_text=pz_in),simgui.Text("      ", font=('Arial Bold', 12)),
            simgui.In(size=(15, 1), enable_events=True, key="pz_out"),
        ],
        [   simgui.Text("Height conversion", font=('Arial Bold', 12)),
            simgui.In(size=(15, 1), enable_events=True, key="hconv_in", default_text=hconv_in),simgui.Text("      ", font=('Arial Bold', 12)),
            simgui.In(size=(15, 1), enable_events=True, key="hconv_out"),
        ],
        [   simgui.Text("Unit code            ", font=('Arial Bold', 12)),
            simgui.In(size=(15, 1), enable_events=True, key="uc_in", default_text=uc_in),simgui.Text("      ", font=('Arial Bold', 12)),
            simgui.In(size=(15, 1), enable_events=True, key="uc_out"),
        ],
        [simgui.Text("(1=rad, 2=m, 0=no unit)", font=('Arial Bold', 10)),],
        [simgui.Text("                              ", font=('Arial Bold', 12)),
         ],
        [simgui.Button(button_text='Check input', enable_events=True, key="check-button"),
         simgui.Button(button_text='Reset input', enable_events=True, key="reset-button"),
         ],
        [simgui.Button(button_text='Start header modification', disabled=True, enable_events=True, key="start-button"),
         simgui.Text("                                  ", font=('Arial Bold', 12)),
         simgui.Button(button_text='Cancel', enable_events=True, key="cancel-button"),
         ],
        ]
    
    header_mod_win = simgui.Window('Bin-file header modification', HMLayout, size=(500, 350))
    
    timestampsfile=simgui.popup_get_file('Please select a timestamps file:',  title="Get timestamps file")
    if timestampsfile!=None:
        if timestampsfile=='':
            simgui.popup_auto_close('Error: No file selected.')
        elif os.path.isfile(timestampsfile)==False:
                simgui.popup_auto_close('Error: This file doesn\'t exist.')
        else: 
            file_name, file_extension = os.path.splitext(timestampsfile)
            if file_extension!='.txt':
                simgui.popup_auto_close('Error: Wrong timestamps file format.')
            else:
                print('banana')
                hm_win_check=True
                while hm_win_check==True:
                    event, values = header_mod_win.read()

                    if event == simgui.WIN_CLOSED:
                        simgui.popup_auto_close('No header modification!')
                        hm_win_check=False
                    
                    if event == 'cancel-button':
                        simgui.popup_auto_close('No header modification!')
                        hm_win_check=False
                        
                    if event == 'check-button':
                        
                        w_out=values['w_out']
                        if w_out=='':
                            w_out=w_in
                            header_mod_win['w_out'].update(value=w_in)
                        else:
                            if w_out.isdigit()==False:
                                simgui.popup_auto_close('Image width must be a positive integer!')
                                header_mod_win['w_out'].update(value='')
                            else:
                                h_out=values['h_out']
                                if h_out=='':
                                    h_out=h_in
                                    header_mod_win['h_out'].update(value=h_in)
                                else:
                                    if h_out.isdigit()==False:
                                        simgui.popup_auto_close('Image height must be a positive integer!')
                                        header_mod_win['h_out'].update(value='')
                                    else:
                                        pz_out=values['pz_out']
                                        if pz_out=='':
                                            pz_out=pz_in
                                            header_mod_win['pz_out'].update(value=pz_in)
                                        else:
                                            if is_float(pz_out)==False:
                                                simgui.popup_auto_close('Pixel size must be a floating point number!')
                                                header_mod_win['pz_out'].update(value='')
                                            else:
                                                hconv_out=values['hconv_out']
                                                if hconv_out=='':
                                                    hconv_out=hconv_in
                                                    header_mod_win['hconv_out'].update(value=hconv_in)
                                                else:
                                                    if is_float(hconv_out)==False:
                                                        simgui.popup_auto_close('Height conversion must be a floating point number!')
                                                        header_mod_win['hconv_out'].update(value='')
                                                    else:
                                                        uc_out=values['uc_out']
                                                        if uc_out=='':
                                                            uc_out=uc_in
                                                            header_mod_win['uc_out'].update(value=uc_in)
                                                        else:
                                                            if uc_out.isdigit()==False:
                                                                simgui.popup_auto_close('Unit code must be a positive integer!')
                                                                header_mod_win['uc_out'].update(value='')
                                                            else:
                                                                simgui.popup_auto_close('Input ok!')
                                                                header_mod_win['w_out'].update(disabled=True)
                                                                header_mod_win['h_out'].update(disabled=True)
                                                                header_mod_win['pz_out'].update(disabled=True)
                                                                header_mod_win['hconv_out'].update(disabled=True)
                                                                header_mod_win['uc_out'].update(disabled=True)
                                                                
                                                                header_mod_win['start-button'].update(disabled=False)
                                                         
                    if event == 'reset-button':
                        header_mod_win['start-button'].update(disabled=True)
                        header_mod_win['w_out'].update(disabled=False)
                        header_mod_win['h_out'].update(disabled=False)
                        header_mod_win['pz_out'].update(disabled=False)
                        header_mod_win['hconv_out'].update(disabled=False)
                        header_mod_win['uc_out'].update(disabled=False)
                        
                    if event == 'start-button':
                                                
                        w=int(w_out)
                        h=int(h_out)
                        pz=float(pz_out)
                        hconv=float(hconv_out)
                        uc=int(uc_out)
                        
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
                        
                        for k in range(nImages):
                            
                            file_path=binfolder+'/'+str(k).rjust(5, '0')+'_phase.bin'
                            
                            (phase_map,file_header_placeholder)=binkoala.read_mat_bin(file_path)
                            
                            binkoala.write_mat_bin(file_path, phase_map, w, h, pz, hconv, uc)

                        hm_win_check=False
                        
                header_mod_win.close()  
                
                        