"""
module for the program DHM file manager v04

the functions are called when pushing on of the "modify header" buttons in the main window

modify_bin_header: allows to modify the header of all bin files of a choosen folder

modify_bnr_header: allows to modify the header of a bnr file

opens a GUI
"""

import tkinter as tk
from tkinter import filedialog
import binkoala
import numpy
import struct

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
            return False

def modify_bin_header(master):
    #to modify the header of all bin files of a choosen folder
    
    
    binfolder=filedialog.askdirectory(title="Select a folder with DHM bin files")
    timestampsfile=filedialog.askopenfilename(title="Select a timestamps file")
    
    #get header
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
    
    def cancel():
        tk.messagebox.showinfo('No header modification!', 'No header modification!')
        window.destroy()
        
    def check_input():
        # hecks the input fields of the window one by one,
        # disables the input field and enables the start button, when everything is ok
        
        w_out=Ewout.get()
        if w_out=='':
            w_out=w_in
            Ewout.delete(0,tk.END)
            Ewout.insert(0,w_in)
        else:
            if w_out.isdigit()==False:
                tk.messagebox.showinfo('Error', 'Image width must be a positive integer!')
                Ewout.delete(0,tk.END)
                Ewout.insert(0,'')
            else:
                h_out=Ehout.get()
                if h_out=='':
                    h_out=h_in
                    Ehout.delete(0,tk.END)
                    Ehout.insert(0,h_in)
                else:
                    if h_out.isdigit()==False:
                        tk.messagebox.showinfo('Error', 'Image height must be a positive integer!')
                        Ehout.delete(0,tk.END)
                        Ehout.insert(0,'')
                    else:
                        pz_out=Epout.get()
                        if pz_out=='':
                            pz_out=pz_in
                            Epout.delete(0,tk.END)
                            Epout.insert(0,pz_in)
                        else:
                            if is_float(pz_out)==False:
                                tk.messagebox.showinfo('Error', 'Pixel size must be a floating point number!')
                                Epout.delete(0,tk.END)
                                Epout.insert(0,'')
                            else:
                                hconv_out=Ecout.get()
                                if hconv_out=='':
                                    hconv_out=hconv_in
                                    Ecout.delete(0,tk.END)
                                    Ecout.insert(0,hconv_in)
                                else:
                                    if is_float(hconv_out)==False:
                                        tk.messagebox.showinfo('Error', 'Height conversion must be a floating point number!')
                                        Ecout.delete(0,tk.END)
                                        Ecout.insert(0,'')
                                    else:
                                        uc_out=Euout.get()
                                        if uc_out=='':
                                            uc_out=uc_in
                                            Euout.delete(0,tk.END)
                                            Euout.insert(0,uc_in)
                                        else:
                                            if uc_out.isdigit()==False:
                                                tk.messagebox.showinfo('Error', 'Unit code must be a positive integer!')
                                                Euout.delete(0,tk.END)
                                                Euout.insert(0,'')
                                            else:
                                                tk.messagebox.showinfo('-_-', 'Input ok!')
                                                Ewout.config(state= "disabled")
                                                Ehout.config(state= "disabled")
                                                Epout.config(state= "disabled")
                                                Ecout.config(state= "disabled")
                                                Euout.config(state= "disabled")
                                                
                                                start_button.config(state= "normal")

    def reset_input():
        #resets the start button to disabled and the input fields to enabled
        Ewout.config(state= "normal")
        Ehout.config(state= "normal")
        Epout.config(state= "normal")
        Ecout.config(state= "normal")
        Euout.config(state= "normal")
        
        start_button.config(state= "disabled")
        
    def start():
        #when pushing the start button, starts the header modification
        w=int(Ewout.get())
        h=int(Ehout.get())
        pz=float(Epout.get())
        hconv=float(Ecout.get())
        uc=int(Euout.get())
        
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
        
        # modify the header of all bin files
        for k in range(nImages):
            
            file_path=binfolder+'/'+str(k).rjust(5, '0')+'_phase.bin'
            
            (phase_map,file_header_placeholder)=binkoala.read_mat_bin(file_path)
            
            binkoala.write_mat_bin(file_path, phase_map, w, h, pz, hconv, uc)

        tk.messagebox.showinfo('-_-', 'Header mofification done.')
        window.destroy()
    
    ################################################################
    # define the GUI window and it's layout

    window = tk.Toplevel(master)
    window.title('Bin-file header modification')
    
    ###################################
    # define the widgets:
    
    #toplabel = tk.Label(window, text= "Which elements of the header do you want to change?")
    current = tk.Label(window, text= "Current header")
    replace = tk.Label(window, text= "Replace with")
    Lw = tk.Label(window, text= "Image width")
    Ewin = tk.Entry(window, width=15)
    Ewin.insert(0,w_in)
    Ewout = tk.Entry(window, width=15)
    Lh = tk.Label(window, text= "Image height")
    Ehin = tk.Entry(window, width=15)
    Ehin.insert(0,h_in)
    Ehout = tk.Entry(window, width=15)
    Lp = tk.Label(window, text= "Pixel size")
    Epin = tk.Entry(window, width=15)
    Epin.insert(0,pz_in)
    Epout = tk.Entry(window, width=15)
    Lc =tk.Label(window, text= "Height conversion")
    Ecin = tk.Entry(window, width=15)
    Ecin.insert(0,hconv_in)
    Ecout = tk.Entry(window, width=15)
    Lu = tk.Label(window, text= "Unit code")
    Euin = tk.Entry(window, width=15)
    Euin.insert(0,uc_in)
    Euout = tk.Entry(window, width=15)
    Luexp = tk.Label(window, text= "(1=rad, 2=m, 0=no unit)")
    
    check_button = tk.Button(window, text='Check input', command=check_input)
    reset_button = tk.Button(window, text='Reset input', command=reset_input)
    start_button = tk.Button(window, text='Start header modification', command=start)
    start_button.config(state= "disabled")
    cancel_button = tk.Button(window, text='Cancel', command=cancel)
    
    ##################################
    # positionning of the widgets

    #toplabel.grid(row=0, column=1, padx=5, pady=5, sticky="nw")
    current.grid(row=1, column=1, padx=5, pady=5, sticky="nw")
    replace.grid(row=1, column=2, padx=5, pady=5, sticky="nw")
    Lw.grid(row=2, column=0, padx=5, pady=5, sticky="nw")
    Ewin.grid(row=2, column=1, padx=5, pady=5, sticky="nw")
    Ewout.grid(row=2, column=2, padx=5, pady=5, sticky="nw")
    Lh.grid(row=3, column=0, padx=5, pady=5, sticky="nw")
    Ehin.grid(row=3, column=1, padx=5, pady=5, sticky="nw")
    Ehout.grid(row=3, column=2, padx=5, pady=5, sticky="nw")
    Lp.grid(row=4, column=0, padx=5, pady=5, sticky="nw")
    Epin.grid(row=4, column=1, padx=5, pady=5, sticky="nw")
    Epout.grid(row=4, column=2, padx=5, pady=5, sticky="nw")
    Lc.grid(row=5, column=0, padx=5, pady=5, sticky="nw")
    Ecin.grid(row=5, column=1, padx=5, pady=5, sticky="nw")
    Ecout.grid(row=5, column=2, padx=5, pady=5, sticky="nw")
    Lu.grid(row=6, column=0, padx=5, pady=5, sticky="nw")
    Euin.grid(row=6, column=1, padx=5, pady=5, sticky="nw")
    Euout.grid(row=6, column=2, padx=5, pady=5, sticky="nw")
    Luexp.grid(row=7, column=0, padx=5, pady=5, sticky="nw")
    
    check_button.grid(row=8, column=0, padx=5, pady=5, sticky="nw")
    reset_button.grid(row=8, column=1, padx=5, pady=5, sticky="nw")
    start_button.grid(row=9, column=0, padx=5, pady=5, sticky="nw")
    cancel_button.grid(row=9, column=1, padx=5, pady=5, sticky="nw")
    
    ##################################
    # some tkinter window configuration:
    
    window.protocol("WM_DELETE_WINDOW", lambda: None)  # Disable closing the window using the close button
    window.geometry("+{}+{}".format(master.winfo_rootx() + 50, master.winfo_rooty() + 50))
    window.grab_set()
    master.wait_window(window)
    
############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################

def modify_bnr_header(master):
    # to modify the header of a bnr file
    
    bnrfile=filedialog.askopenfilename(title="Select a bnr file")

    #get header from bnr file
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
    
    def cancel():
        tk.messagebox.showinfo('No header modification!', 'No header modification!')
        window.destroy()
        
    def check_input():
    	# checks the input fields of the window one by one,
     # disables the input field and enables the start button, when everything is ok
     
        w_out=Ewout.get()
        if w_out=='':
            w_out=w_in
            Ewout.delete(0,tk.END)
            Ewout.insert(0,w_in)
        else:
            if w_out.isdigit()==False:
                tk.messagebox.showinfo('Error', 'Image width must be a positive integer!')
                Ewout.delete(0,tk.END)
                Ewout.insert(0,'')
            else:
                h_out=Ehout.get()
                if h_out=='':
                    h_out=h_in
                    Ehout.delete(0,tk.END)
                    Ehout.insert(0,h_in)
                else:
                    if h_out.isdigit()==False:
                        tk.messagebox.showinfo('Error', 'Image height must be a positive integer!')
                        Ehout.delete(0,tk.END)
                        Ehout.insert(0,'')
                    else:
                        pz_out=Epout.get()
                        if pz_out=='':
                            pz_out=pz_in
                            Epout.delete(0,tk.END)
                            Epout.insert(0,pz_in)
                        else:
                            if is_float(pz_out)==False:
                                tk.messagebox.showinfo('Error', 'Pixel size must be a floating point number!')
                                Epout.delete(0,tk.END)
                                Epout.insert(0,'')
                            else:
                                wave_out=Ewvout.get()
                                if wave_out=='':
                                    wave_out=wave_in
                                    Ewvout.delete(0,tk.END)
                                    Ewvout.insert(0,wave_in)
                                else:
                                    if is_float(wave_out)==False:
                                        tk.messagebox.showinfo('Error', 'Wavelength must be a floating point number!')
                                        Ewvout.delete(0,tk.END)
                                        Ewvout.insert(0,'')
                                    else:
                                        n_1_out=En1out.get()
                                        if n_1_out=='':
                                            n_1_out=n_1_in
                                            En1out.delete(0,tk.END)
                                            En1out.insert(0,n_1_in)
                                        else:
                                            if is_float(n_1_out)==False:
                                                tk.messagebox.showinfo('Error', 'n_1 must be a floating point number!')
                                                En1out.delete(0,tk.END)
                                                En1out.insert(0,'')
                                            else:
                                                n_2_out=En2out.get()
                                                if n_2_out=='':
                                                    n_2_out=n_2_in
                                                    En2out.delete(0,tk.END)
                                                    En2out.insert(0,n_2_in)
                                                else:
                                                    if is_float(n_2_out)==False:
                                                        tk.messagebox.showinfo('Error', 'n_2 must be a floating point number!')
                                                        En2out.delete(0,tk.END)
                                                        En2out.insert(0,'')
                                                    else:
                                                        tk.messagebox.showinfo('-_-', 'Input ok!')
                                                        Ewout.config(state= "disabled")
                                                        Ehout.config(state= "disabled")
                                                        Epout.config(state= "disabled")
                                                        Ewvout.config(state= "disabled")
                                                        En1out.config(state= "disabled")
                                                        En2out.config(state= "disabled")
                                                
                                                        start_button.config(state= "normal")
    
    def reset_input():
        #resets the start button to disabled and the input fields to enabled
        Ewout.config(state= "normal")
        Ehout.config(state= "normal")
        Epout.config(state= "normal")
        Ewvout.config(state= "normal")
        En1out.config(state= "normal")
        En2out.config(state= "normal")
        
        start_button.config(state= "disabled")
        
    def start():
        w=int(Ewout.get())
        h=int(Ehout.get())
        pz=float(Epout.get())
        wave=float(Ewvout.get())
        n_1=float(En1out.get())
        n_2=float(En2out.get())
        
        x=struct.pack('iii', nImages, w, h)
        y=struct.pack('ffff', pz, wave, n_1, n_2)
        
        with open(bnrfile, 'rb+') as fileID:
            fileID.seek(0)
            fileID.write(x)
            fileID.write(y)
        
        fileID.close()
        
        tk.messagebox.showinfo('-_-', 'Header mofification done.')
        window.destroy()
    
    ################################################################
    # define the GUI window and it's layout
    
    window = tk.Toplevel(master)
    window.title('Bin-file header modification')
    
    ###################################
    # define the widgets:
        
    #toplabel = tk.Label(window, text= "Which elements of the header do you want to change?")
    current = tk.Label(window, text= "Current header")
    replace = tk.Label(window, text= "Replace with")
    Lw = tk.Label(window, text= "Image width")
    Ewin = tk.Entry(window, width=15)
    Ewin.insert(0,w_in)
    Ewout = tk.Entry(window, width=15)
    Lh = tk.Label(window, text= "Image height")
    Ehin = tk.Entry(window, width=15)
    Ehin.insert(0,h_in)
    Ehout = tk.Entry(window, width=15)
    Lp = tk.Label(window, text= "Pixel size")
    Epin = tk.Entry(window, width=15)
    Epin.insert(0,pz_in)
    Epout = tk.Entry(window, width=15)
    Lwv = tk.Label(window, text= "Wavelength")
    Ewvin = tk.Entry(window, width=15)
    Ewvin.insert(0,wave_in)
    Ewvout = tk.Entry(window, width=15)
    Ln1 = tk.Label(window, text= "n_1")
    En1in = tk.Entry(window, width=15)
    En1in.insert(0,n_1_in)
    En1out = tk.Entry(window, width=15)
    Ln2 = tk.Label(window, text= "n_2")
    En2in = tk.Entry(window, width=15)
    En2in.insert(0,n_2_in)
    En2out = tk.Entry(window, width=15)
    
    check_button = tk.Button(window, text='Check input', command=check_input)
    reset_button = tk.Button(window, text='Reset input', command=reset_input)
    start_button = tk.Button(window, text='Start header modification', command=start)
    start_button.config(state= "disabled")
    cancel_button = tk.Button(window, text='Cancel', command=cancel)
    
    ##################################
    # positionning of the widgets
    
    #toplabel.grid(row=0, column=1, padx=5, pady=5, sticky="nw")
    current.grid(row=1, column=1, padx=5, pady=5, sticky="nw")
    replace.grid(row=1, column=2, padx=5, pady=5, sticky="nw")
    Lw.grid(row=2, column=0, padx=5, pady=5, sticky="nw")
    Ewin.grid(row=2, column=1, padx=5, pady=5, sticky="nw")
    Ewout.grid(row=2, column=2, padx=5, pady=5, sticky="nw")
    Lh.grid(row=3, column=0, padx=5, pady=5, sticky="nw")
    Ehin.grid(row=3, column=1, padx=5, pady=5, sticky="nw")
    Ehout.grid(row=3, column=2, padx=5, pady=5, sticky="nw")
    Lp.grid(row=4, column=0, padx=5, pady=5, sticky="nw")
    Epin.grid(row=4, column=1, padx=5, pady=5, sticky="nw")
    Epout.grid(row=4, column=2, padx=5, pady=5, sticky="nw")
    Lwv.grid(row=5, column=0, padx=5, pady=5, sticky="nw")
    Ewvin.grid(row=5, column=1, padx=5, pady=5, sticky="nw")
    Ewvout.grid(row=5, column=2, padx=5, pady=5, sticky="nw")
    Ln1.grid(row=6, column=0, padx=5, pady=5, sticky="nw")
    En1in.grid(row=6, column=1, padx=5, pady=5, sticky="nw")
    En1out.grid(row=6, column=2, padx=5, pady=5, sticky="nw")
    Ln2.grid(row=7, column=0, padx=5, pady=5, sticky="nw")
    En2in.grid(row=7, column=1, padx=5, pady=5, sticky="nw")
    En2out.grid(row=7, column=2, padx=5, pady=5, sticky="nw")
    
    check_button.grid(row=8, column=0, padx=5, pady=5, sticky="nw")
    reset_button.grid(row=8, column=1, padx=5, pady=5, sticky="nw")
    start_button.grid(row=9, column=0, padx=5, pady=5, sticky="nw")
    cancel_button.grid(row=9, column=1, padx=5, pady=5, sticky="nw")
    
    ##################################
    # some tkinter window configuration:
        
    window.protocol("WM_DELETE_WINDOW", lambda: None)  # Disable closing the window using the close button
    window.geometry("+{}+{}".format(master.winfo_rootx() + 50, master.winfo_rooty() + 50))
    window.grab_set()
    master.wait_window(window)