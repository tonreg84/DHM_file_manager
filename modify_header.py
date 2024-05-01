import PySimpleGUI as simgui
import os
import binkoala
import numpy
import struct

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
            return False

def modify_bin_header(binfolder):
    
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
            simgui.popup_auto_close('Error: No timestamps file selected.')
        elif os.path.isfile(timestampsfile)==False:
                simgui.popup_auto_close('Error: The file doesn\'t exist.')
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
                        simgui.auto_close('Header mofification done.')
                header_mod_win.close()  
                
def modify_bnr_header(bnrfile):
    
    #get data from bnr file
    fileID = open(bnrfile, 'rb')
    nImages = numpy.fromfile(fileID, dtype="i4", count=1)
    nImages = nImages[0]
    w = numpy.fromfile(fileID, dtype="i4", count=1)
    w_in=w[0]
    h = numpy.fromfile(fileID, dtype="i4", count=1)
    h_in=h[0]
    pz = numpy.fromfile(fileID, dtype="f4", count=1)
    pz_in=pz[0]
    wavelength = numpy.fromfile(fileID, dtype="f4", count=1)
    wave_in=wavelength[0]
    n_1 = numpy.fromfile(fileID, dtype="f4", count=1)
    n_1_in=n_1[0]
    n_2 = numpy.fromfile(fileID, dtype="f4", count=1)
    n_2_in=n_2[0]
    fileID.close
    
    HMLayout = [
        [simgui.Text('File name: '+os.path.basename(bnrfile), font=('Arial Bold', 14)),
        ],
        [simgui.Text("Which elements of the header do you want to change?", font=('Arial Bold', 14)),
        ],
        [simgui.Text("                              ", font=('Arial Bold', 12)),
         ],
        [simgui.Text("                              ", font=('Arial Bold', 12)),
         simgui.Text("Current header", font=('Arial Bold', 12)),simgui.Text("       ", font=('Arial Bold', 12)),
         simgui.Text("Replace with", font=('Arial Bold', 12)),
        ],
        [simgui.Text("Image width          ", font=('Arial Bold', 12)),
         simgui.In(size=(15, 1), enable_events=True, key="w_in", default_text=w_in),simgui.Text("      ", font=('Arial Bold', 12)),
         simgui.In(size=(15, 1), enable_events=True, key="w_out"),
        ],
        [simgui.Text("Image hight         ", font=('Arial Bold', 12)),
         simgui.In(size=(15, 1), enable_events=True, key="h_in", default_text=h_in),simgui.Text("      ", font=('Arial Bold', 12)),
         simgui.In(size=(15, 1), enable_events=True, key="h_out"),
        ],
        [simgui.Text("Pixel size            ", font=('Arial Bold', 12)),
         simgui.In(size=(15, 1), enable_events=True, key="pz_in", default_text=pz_in),simgui.Text("      ", font=('Arial Bold', 12)),
         simgui.In(size=(15, 1), enable_events=True, key="pz_out"),
        ],
        [simgui.Text("Wavelength", font=('Arial Bold', 12)),
         simgui.In(size=(15, 1), enable_events=True, key="wave_in", default_text=wave_in),simgui.Text("      ", font=('Arial Bold', 12)),
         simgui.In(size=(15, 1), enable_events=True, key="wave_out"),
        ],
        [simgui.Text("n_1            ", font=('Arial Bold', 12)),
         simgui.In(size=(15, 1), enable_events=True, key="n_1_in", default_text=n_1_in),simgui.Text("      ", font=('Arial Bold', 12)),
         simgui.In(size=(15, 1), enable_events=True, key="n_1_out"),
        ],
        [simgui.Text("n_2            ", font=('Arial Bold', 12)),
         simgui.In(size=(15, 1), enable_events=True, key="n_2_in", default_text=n_2_in),simgui.Text("      ", font=('Arial Bold', 12)),
         simgui.In(size=(15, 1), enable_events=True, key="n_2_out"),
         ],
        [simgui.Button(button_text='Check input', enable_events=True, key="check-button"),
          simgui.Button(button_text='Reset input', enable_events=True, key="reset-button"),
          ],
        [simgui.Button(button_text='Start header modification', disabled=True, enable_events=True, key="start-button"),
          simgui.Text("                                  ", font=('Arial Bold', 12)),
          simgui.Button(button_text='Cancel', enable_events=True, key="cancel-button"),
          ],
        ]
    
    header_mod_win = simgui.Window('Bnr-file header modification', HMLayout, size=(500, 350))
    
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
                                    wave_out=values['wave_out']
                                    if wave_out=='':
                                        wave_out=wave_in
                                        header_mod_win['wave_out'].update(value=wave_in)
                                    else:
                                        if is_float(wave_out)==False:
                                            simgui.popup_auto_close('Wavelength must be a floating point number!')
                                            header_mod_win['wave_out'].update(value='')
                                        else:
                                            n_1_out=values['n_1_out']
                                            if n_1_out=='':
                                                n_1_out=n_1_in
                                                header_mod_win['n_1_out'].update(value=n_1_in)
                                            else:
                                                if is_float(n_1_out)==False:
                                                    simgui.popup_auto_close('n_1 must be a floating point number!')
                                                    header_mod_win['n_1_out'].update(value='')
                                                else:
                                                    n_2_out=values['n_2_out']
                                                    if n_2_out=='':
                                                        n_2_out=n_2_in
                                                        header_mod_win['n_2_out'].update(value=n_2_in)
                                                    else:
                                                        if is_float(n_2_out)==False:
                                                            simgui.popup_auto_close('n_2 must be a floating point number!')
                                                            header_mod_win['n_2_out'].update(value='')
                                                        else:
                                                            simgui.popup_auto_close('Input ok!')
                                                            header_mod_win['w_out'].update(disabled=True)
                                                            header_mod_win['h_out'].update(disabled=True)
                                                            header_mod_win['pz_out'].update(disabled=True)
                                                            header_mod_win['wave_out'].update(disabled=True)
                                                            header_mod_win['n_1_out'].update(disabled=True)
                                                            header_mod_win['n_2_out'].update(disabled=True)
                                                            
                                                            header_mod_win['start-button'].update(disabled=False)
                                             
        if event == 'reset-button':
            header_mod_win['start-button'].update(disabled=True)
            header_mod_win['w_out'].update(disabled=False)
            header_mod_win['h_out'].update(disabled=False)
            header_mod_win['pz_out'].update(disabled=False)
            header_mod_win['wave_out'].update(disabled=False)
            header_mod_win['n_1_out'].update(disabled=False)
            header_mod_win['n_2_out'].update(disabled=False)
            
        if event == 'start-button':
                                    
            w=int(w_out)
            h=int(h_out)
            pz=float(pz_out)
            wave=float(wave_out)
            n_1=float(n_1_out)
            n_2=float(n_2_out)
            
            x=struct.pack('iii', nImages, w, h)
            y=struct.pack('ffff', pz, wave, n_1, n_2)
            
            with open(bnrfile, 'rb+') as fileID:
                fileID.seek(0)
                fileID.write(x)
                fileID.write(y)
            
            fileID.close()
                
            simgui.popup_auto_close('Header mofification done.')
            
            hm_win_check=False
            
    header_mod_win.close()  
                
                        
