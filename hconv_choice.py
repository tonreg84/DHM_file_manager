def hconv_choice_binary2X(master,input_file):
    import tkinter as tk
    
    alist=input_file.split('.')
    extension=alist[-1]
    
    def is_float(string):
        try:
            float(string)
            return True
        except ValueError:
            return False
    
    def cancel():
        global conv_check
        conv_check=False
        window.destroy()
    def checkit(S):
        #if tik one w box, set the other to false
        if S =='manfact':
            if vmanfact.get() == True:
                vpifact.set(False)
                vdegree.set(False)
                vhconv.set(False)
                vhinv.set(False)
        if S =='pifact':
            if vpifact.get() == True:
                vdegree.set(False)
                vhinv.set(False)
                vhconv.set(False)
                vmanfact.set(False)
        if S =='degree':
            if vdegree.get() == True:
                vpifact.set(False)
                vhinv.set(False)
                vhconv.set(False)
                vmanfact.set(False)
        if S =='hconv':
            if vhconv.get() == True:
                vpifact.set(False)
                vdegree.set(False)
                vhinv.set(False)
                vmanfact.set(False)
        if S =='hinv':
            if vhinv.get() == True:
                vpifact.set(False)
                vdegree.set(False)
                vhconv.set(False)
                vmanfact.set(False)
        if S =='manfact':
            if vmanfact.get() == True:
                vpifact.set(False)
                vhconv.set(False)
                vhinv.set(False)
                vdegree.set(False)

    def ok():
        #check the entries, make conversion factor in float
        nonlocal conversion_factor
        nonlocal conv_check
        if vmanfact.get() == True:
            if manfact_entry.get() == '':
                tk.messagebox.showinfo('Error', 'Manual conversion factor missing.')
            elif is_float(manfact_entry.get())==False:
                tk.messagebox.showinfo('Error', 'Please enter floating point numbers only.')
                manfact_entry.delete(0,tk.END)
            else:
                conversion_factor=float(manfact_entry.get())
                conv_check=True
                window.destroy()
        if vpifact.get() == True:
            conversion_factor=360/6.283185307179586
            conv_check=True        
            window.destroy()
        if vdegree.get() == True:
            conversion_factor=6.283185307179586/360
            conv_check=True        
            window.destroy()
            
        if vhconv.get() == True:
            
            if extension == 'bin':
                import binkoala
                (in_file_image,in_file_header)=binkoala.read_mat_bin(input_file)
                conversion_factor=in_file_header['hconv'][0]
                conv_check=True
                window.destroy()
                
            if extension == 'bnr':
                from numpy import fromfile
                from numpy import single
                #get data from bnr file
                fileID = open(input_file, 'rb')
                nImages = fromfile(fileID, dtype="i4", count=1)
                w = fromfile(fileID, dtype="i4", count=1)
                h = fromfile(fileID, dtype="i4", count=1)
                pz = fromfile(fileID, dtype="f4", count=1)
                wave = fromfile(fileID, dtype="f4", count=1)
                n_1 = fromfile(fileID, dtype="f4", count=1)
                n_2 = fromfile(fileID, dtype="f4", count=1)
                fileID.close
                   
                conversion_factor=single(wave/6.283185307179586/(n_2-n_1))
                conv_check=True
                window.destroy()
            
        if vhinv.get() == True:
            
            if extension == 'bin':
                import binkoala
                (in_file_image,in_file_header)=binkoala.read_mat_bin(input_file)
                conversion_factor=1/in_file_header['hconv'][0]
                conv_check=True
                window.destroy()
                
            if extension == 'bnr':
                from numpy import fromfile
                from numpy import single
                #get data from bnr file
                fileID = open(input_file, 'rb')
                nImages = fromfile(fileID, dtype="i4", count=1)
                w = fromfile(fileID, dtype="i4", count=1)
                h = fromfile(fileID, dtype="i4", count=1)
                pz = fromfile(fileID, dtype="f4", count=1)
                wave = fromfile(fileID, dtype="f4", count=1)
                n_1 = fromfile(fileID, dtype="f4", count=1)
                n_2 = fromfile(fileID, dtype="f4", count=1)
                fileID.close
                   
                conversion_factor=single(6.283185307179586*(n_2-n_1)/wave)
                conv_check=True
                window.destroy()
            
    conv_check=False
    conversion_factor=None
    
    window = tk.Toplevel(master)
    window.title('Choice of conversion factor')
    
    vmanfact=tk.BooleanVar()
    manfact=tk.Checkbutton(window, text="Apply the conversion factor:", variable=vmanfact, command=lambda: checkit('manfact'))
    vmanfact.set(True)
    manfact_entry = tk.Entry(window)
    manfact_entry.insert(0,"1.0")
    vpifact=tk.BooleanVar()
    pifact=tk.Checkbutton(window, text="Conversion from radian to degree [360/2Pi].", variable=vpifact, command=lambda: checkit('pifact'))
    vdegree=tk.BooleanVar()
    degree=tk.Checkbutton(window, text="Conversion from degree to radian [2Pi/360].", variable=vdegree, command=lambda: checkit('degree'))
    vhconv=tk.BooleanVar()
    hconv=tk.Checkbutton(window, text="Conversion from radian to nanometer [wavelength*(2Pi(n_2-n_1)^-1].", variable=vhconv, command=lambda: checkit('hconv'))
    vhinv=tk.BooleanVar()
    hinv=tk.Checkbutton(window, text="Conversion from nanometer to radian [2Pi(n_2-n_1)/wavelength].", variable=vhinv, command=lambda: checkit('hinv'))
    
    okbutton=tk.Button(window, text="Ok", width=16, height=1, command=lambda: ok())
    cancelbutton=tk.Button(window, text="Cancel", width=16, height=1, command=lambda: cancel())
    
    manfact.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
    manfact_entry.grid(row=0, column=1, padx=5, pady=5, sticky="nw")
    pifact.grid(row=1, column=0, padx=5, pady=5, sticky="nw")
    degree.grid(row=2, column=0, padx=5, pady=5, sticky="nw")
    hconv.grid(row=3, column=0, padx=5, pady=5, sticky="nw")
    hinv.grid(row=4, column=0, padx=5, pady=5, sticky="nw")
    
    okbutton.grid(row=5, column=0, padx=5, pady=5, sticky="nw")
    cancelbutton.grid(row=5, column=1, padx=5, pady=5, sticky="nw")
    
    window.protocol("WM_DELETE_WINDOW", lambda: None)  # Disable closing the window using the close button
    window.geometry("+{}+{}".format(master.winfo_rootx() + 50, master.winfo_rooty() + 50))
    window.grab_set()
    master.wait_window(window)
    
    return conv_check, conversion_factor

def hconv_choice_tif2binary(master,wave):
    import tkinter as tk
    
    def is_float(string):
        try:
            float(string)
            return True
        except ValueError:
            return False
    
    def cancel():
        global conv_check
        conv_check=False
        window.destroy()
    def checkit(S):
        #if tik one w box, set the other to false
        if S =='manfact':
            if vmanfact.get() == True:
                vpifact.set(False)
                vdegree.set(False)
                vhconv.set(False)
                vhinv.set(False)
        if S =='pifact':
            if vpifact.get() == True:
                vdegree.set(False)
                vhinv.set(False)
                vhconv.set(False)
                vmanfact.set(False)
        if S =='degree':
            if vdegree.get() == True:
                vpifact.set(False)
                vhinv.set(False)
                vhconv.set(False)
                vmanfact.set(False)
        if S =='hconv':
            if vhconv.get() == True:
                vpifact.set(False)
                vdegree.set(False)
                vhinv.set(False)
                vmanfact.set(False)
        if S =='hinv':
            if vhinv.get() == True:
                vpifact.set(False)
                vdegree.set(False)
                vhconv.set(False)
                vmanfact.set(False)
        if S =='manfact':
            if vmanfact.get() == True:
                vpifact.set(False)
                vhconv.set(False)
                vhinv.set(False)
                vdegree.set(False)

    def ok():
        #check the entries, make conversion factor in float
        nonlocal conversion_factor
        nonlocal conv_check
        nonlocal n_1, n_2, pz
        
        if pz_entry.get()=='':
            tk.messagebox.showinfo('Error', 'Pixel size missing.')
        elif is_float(pz_entry.get())==False:
            tk.messagebox.showinfo('Error', 'Please enter floating point numbers only.')
            pz_entry.delete(0,tk.END)
        else:
            pz=float(pz_entry.get())
            if n1_entry.get()=='' or n2_entry.get() == '':
                tk.messagebox.showinfo('Error', 'Refraction index missing.')
            elif is_float(n1_entry.get())==False or is_float(n2_entry.get())==False:
                tk.messagebox.showinfo('Error', 'Please enter floating point numbers only.')
                if is_float(n1_entry.get())==False:
                    n1_entry.delete(0,tk.END)
                if is_float(n2_entry.get())==False:
                    n2_entry.delete(0,tk.END)
            else:
                n_1=float(n1_entry.get())
                n_2=float(n2_entry.get())
            
                if vmanfact.get() == True:
                    if manfact_entry.get() == '':
                        tk.messagebox.showinfo('Error', 'Manual conversion factor missing.')
                    elif is_float(manfact_entry.get())==False:
                        tk.messagebox.showinfo('Error', 'Please enter floating point numbers only.')
                        manfact_entry.delete(0,tk.END)
                    else:
                        conversion_factor=float(manfact_entry.get())
                        conv_check=True
                        window.destroy()
                if vpifact.get() == True:
                    conversion_factor=360/6.283185307179586
                    conv_check=True        
                    window.destroy()
                if vdegree.get() == True:
                    conversion_factor=6.283185307179586/360
                    conv_check=True        
                    window.destroy()
                if vhconv.get() == True:          
                        conversion_factor=wave/6.283185307179586/(n_2-n_1)
                        conv_check=True
                        window.destroy()
                if vhinv.get() == True:
                        conversion_factor=6.283185307179586*(n_2-n_1)/wave
                        conv_check=True
                        window.destroy()
                
    conv_check=False
    conversion_factor=None
    n_1=None
    n_2=None
    pz=None
    
    window = tk.Toplevel(master)
    window.title('Conversion factor and other parameter')
    
    alabel = tk.Label(window, text= "Conversion from tiff to LynceeTec binary")
    
    pz_label = tk.Label(window, text= "Please enter the pixel size in meter:")
    pz_entry = tk.Entry(window)
    
    n1_label = tk.Label(window, text= "Please enter the first refraction index n_1:")
    n1_entry = tk.Entry(window)
    n2_label = tk.Label(window, text= "Please enter the fsecond refraction index n_2:")
    n2_entry = tk.Entry(window)
    
    vmanfact=tk.BooleanVar()
    manfact=tk.Checkbutton(window, text="Apply the conversion factor:", variable=vmanfact, command=lambda: checkit('manfact'))
    vmanfact.set(True)
    manfact_entry = tk.Entry(window)
    manfact_entry.insert(0,"1.0")
    vpifact=tk.BooleanVar()
    pifact=tk.Checkbutton(window, text="Conversion from radian to degree [360/2Pi].", variable=vpifact, command=lambda: checkit('pifact'))
    vdegree=tk.BooleanVar()
    degree=tk.Checkbutton(window, text="Conversion from degree to radian [2Pi/360].", variable=vdegree, command=lambda: checkit('degree'))
    vhconv=tk.BooleanVar()
    hconv=tk.Checkbutton(window, text="Conversion from radian to nanometer [wavelength*1E9*(2Pi(n_2-n_1)^-1].", variable=vhconv, command=lambda: checkit('hconv'))
    vhinv=tk.BooleanVar()
    hinv=tk.Checkbutton(window, text="Conversion from nanometer to radian [2Pi(n_2-n_1)/wavelength*1E-9].", variable=vhinv, command=lambda: checkit('hinv'))
    
    okbutton=tk.Button(window, text="Ok", width=16, height=1, command=lambda: ok())
    cancelbutton=tk.Button(window, text="Cancel", width=16, height=1, command=lambda: cancel())
    
    alabel.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
    pz_label.grid(row=1, column=0, padx=5, pady=5, sticky="nw")
    pz_entry.grid(row=1, column=1, padx=5, pady=5, sticky="nw")
    n1_label.grid(row=2, column=0, padx=5, pady=5, sticky="nw")
    n1_entry.grid(row=2, column=1, padx=5, pady=5, sticky="nw")
    n2_label.grid(row=3, column=0, padx=5, pady=5, sticky="nw")
    n2_entry.grid(row=3, column=1, padx=5, pady=5, sticky="nw")
    manfact.grid(row=4, column=0, padx=5, pady=5, sticky="nw")
    manfact_entry.grid(row=4, column=1, padx=5, pady=5, sticky="nw")
    pifact.grid(row=5, column=0, padx=5, pady=5, sticky="nw")
    degree.grid(row=6, column=0, padx=5, pady=5, sticky="nw")
    hconv.grid(row=7, column=0, padx=5, pady=5, sticky="nw")
    hinv.grid(row=8, column=0, padx=5, pady=5, sticky="nw")
    
    okbutton.grid(row=9, column=0, padx=5, pady=5, sticky="nw")
    cancelbutton.grid(row=9, column=1, padx=5, pady=5, sticky="nw")
    
    window.protocol("WM_DELETE_WINDOW", lambda: None)  # Disable closing the window using the close button
    window.geometry("+{}+{}".format(master.winfo_rootx() + 50, master.winfo_rooty() + 50))
    window.grab_set()
    master.wait_window(window)
    
    return conv_check, conversion_factor, n_1, n_2, pz

def hconv_choice_tif2tif(master,wave):
    import tkinter as tk
    
    def is_float(string):
        try:
            float(string)
            return True
        except ValueError:
            return False
    
    def cancel():
        global conv_check
        conv_check=False
        window.destroy()
    def checkit(S):
        #if tik one w box, set the other to false
        if S =='manfact':
            if vmanfact.get() == True:
                vpifact.set(False)
                vdegree.set(False)
                vhconv.set(False)
                vhinv.set(False)
        if S =='pifact':
            if vpifact.get() == True:
                vdegree.set(False)
                vhinv.set(False)
                vhconv.set(False)
                vmanfact.set(False)
        if S =='degree':
            if vdegree.get() == True:
                vpifact.set(False)
                vhinv.set(False)
                vhconv.set(False)
                vmanfact.set(False)
        if S =='hconv':
            if vhconv.get() == True:
                vpifact.set(False)
                vdegree.set(False)
                vhinv.set(False)
                vmanfact.set(False)
        if S =='hinv':
            if vhinv.get() == True:
                vpifact.set(False)
                vdegree.set(False)
                vhconv.set(False)
                vmanfact.set(False)
        if S =='manfact':
            if vmanfact.get() == True:
                vpifact.set(False)
                vhconv.set(False)
                vhinv.set(False)
                vdegree.set(False)

    def ok():
        #check the entries, make conversion factor in float
        nonlocal conversion_factor
        nonlocal conv_check
        nonlocal n_1, n_2, pz
        
        if pz_entry.get()=='':
            tk.messagebox.showinfo('Error', 'Pixel size missing.')
        elif is_float(pz_entry.get())==False:
            tk.messagebox.showinfo('Error', 'Please enter floating point numbers only.')
            pz_entry.delete(0,tk.END)
        else:
            pz=float(pz_entry.get())
            if n1_entry.get()=='' or n2_entry.get() == '':
                tk.messagebox.showinfo('Error', 'Refraction index missing.')
            elif is_float(n1_entry.get())==False or is_float(n2_entry.get())==False:
                tk.messagebox.showinfo('Error', 'Please enter floating point numbers only.')
                if is_float(n1_entry.get())==False:
                    n1_entry.delete(0,tk.END)
                if is_float(n2_entry.get())==False:
                    n2_entry.delete(0,tk.END)
            else:
                n_1=float(n1_entry.get())
                n_2=float(n2_entry.get())
            
                if vmanfact.get() == True:
                    if manfact_entry.get() == '':
                        tk.messagebox.showinfo('Error', 'Manual conversion factor missing.')
                    elif is_float(manfact_entry.get())==False:
                        tk.messagebox.showinfo('Error', 'Please enter floating point numbers only.')
                        manfact_entry.delete(0,tk.END)
                    else:
                        conversion_factor=float(manfact_entry.get())
                        conv_check=True
                        window.destroy()
                if vpifact.get() == True:
                    conversion_factor=360/6.283185307179586
                    conv_check=True        
                    window.destroy()
                if vdegree.get() == True:
                    conversion_factor=6.283185307179586/360
                    conv_check=True        
                    window.destroy()
                if vhconv.get() == True:          
                        conversion_factor=wave/6.283185307179586/(n_2-n_1)
                        conv_check=True
                        window.destroy()
                if vhinv.get() == True:
                        conversion_factor=6.283185307179586*(n_2-n_1)/wave
                        conv_check=True
                        window.destroy()
                
    conv_check=False
    conversion_factor=None
    n_1=None
    n_2=None
    pz=None
    
    window = tk.Toplevel(master)
    window.title('Conversion factor and other parameter')
    
    alabel = tk.Label(window, text= "Conversion from tiff to LynceeTec binary")
    
    pz_label = tk.Label(window, text= "Please enter the pixel size in meter:")
    pz_entry = tk.Entry(window)
    
    n1_label = tk.Label(window, text= "Please enter the first refraction index n_1:")
    n1_entry = tk.Entry(window)
    n2_label = tk.Label(window, text= "Please enter the fsecond refraction index n_2:")
    n2_entry = tk.Entry(window)
    
    vmanfact=tk.BooleanVar()
    manfact=tk.Checkbutton(window, text="Apply the conversion factor:", variable=vmanfact, command=lambda: checkit('manfact'))
    vmanfact.set(True)
    manfact_entry = tk.Entry(window)
    manfact_entry.insert(0,"1.0")
    vpifact=tk.BooleanVar()
    pifact=tk.Checkbutton(window, text="Conversion from radian to degree [360/2Pi].", variable=vpifact, command=lambda: checkit('pifact'))
    vdegree=tk.BooleanVar()
    degree=tk.Checkbutton(window, text="Conversion from degree to radian [2Pi/360].", variable=vdegree, command=lambda: checkit('degree'))
    vhconv=tk.BooleanVar()
    hconv=tk.Checkbutton(window, text="Conversion from radian to nanometer [wavelength*1E9*(2Pi(n_2-n_1)^-1].", variable=vhconv, command=lambda: checkit('hconv'))
    vhinv=tk.BooleanVar()
    hinv=tk.Checkbutton(window, text="Conversion from nanometer to radian [2Pi(n_2-n_1)/wavelength*1E-9].", variable=vhinv, command=lambda: checkit('hinv'))
    
    okbutton=tk.Button(window, text="Ok", width=16, height=1, command=lambda: ok())
    cancelbutton=tk.Button(window, text="Cancel", width=16, height=1, command=lambda: cancel())
    
    alabel.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
    pz_label.grid(row=1, column=0, padx=5, pady=5, sticky="nw")
    pz_entry.grid(row=1, column=1, padx=5, pady=5, sticky="nw")
    n1_label.grid(row=2, column=0, padx=5, pady=5, sticky="nw")
    n1_entry.grid(row=2, column=1, padx=5, pady=5, sticky="nw")
    n2_label.grid(row=3, column=0, padx=5, pady=5, sticky="nw")
    n2_entry.grid(row=3, column=1, padx=5, pady=5, sticky="nw")
    manfact.grid(row=4, column=0, padx=5, pady=5, sticky="nw")
    manfact_entry.grid(row=4, column=1, padx=5, pady=5, sticky="nw")
    pifact.grid(row=5, column=0, padx=5, pady=5, sticky="nw")
    degree.grid(row=6, column=0, padx=5, pady=5, sticky="nw")
    hconv.grid(row=7, column=0, padx=5, pady=5, sticky="nw")
    hinv.grid(row=8, column=0, padx=5, pady=5, sticky="nw")
    
    okbutton.grid(row=9, column=0, padx=5, pady=5, sticky="nw")
    cancelbutton.grid(row=9, column=1, padx=5, pady=5, sticky="nw")
    
    window.protocol("WM_DELETE_WINDOW", lambda: None)  # Disable closing the window using the close button
    window.geometry("+{}+{}".format(master.winfo_rootx() + 50, master.winfo_rooty() + 50))
    window.grab_set()
    master.wait_window(window)
    
    return conv_check, conversion_factor, n_1, n_2, pz
