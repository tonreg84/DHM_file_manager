def bnr2bin(input_file,timestampsfile,wavelength,output_folder,master):
# function for the program DHM file manager v04
    
#this function converts LynceeTec Possum bnr sequence to single-image bin files (LynceeTec format)

#input_file: filepath of the bnr sequence
#timestampsfile: filepath of the corresponding Koala timestamps file, from there we will take the int32 array from 3rd column
#wavelength of the DHM laser, float32
#output_folder -> the bin files will be saved in the folder "output_file_Bin files

    from os.path import isdir, basename
    from os import mkdir
    from numpy import fromfile, single, zeros
    import binkoala
    from tkinter import messagebox
    from tkinter import ttk, Toplevel, DoubleVar
    import threading
    from hconv_choice import hconv_choice_binary2X
    
    def onlyname(file_path):
        basenam=basename(file_path)
        alist=basenam.split('.')
        namebase=''
        for k in range(len(alist)-2):
            namebase=namebase+alist[k]+'.'
        namebase=namebase+alist[len(alist)-2]
        return namebase
    
    #get conversion factor
    (conv_check, conversion_factor)=hconv_choice_binary2X(master,input_file)
    print('Choice of conversion factor:',conv_check, conversion_factor)
    
    if conv_check == True:
    
        #outputfolder:
        binfolder = output_folder+'/'+onlyname(input_file)+'_bin files'
        #check if binfolder exists aready
        do_it=False
        if isdir(binfolder)==True:
            result = messagebox.askquestion('Output folder exits already!', 'Do you want to proceed?')
            if result == 'yes':
                do_it=True
        else:
            do_it=True
            mkdir(binfolder)
        
        if do_it==True:
        
            #get data from bnr file
            fileID = open(input_file, 'rb')
            nImages = fromfile(fileID, dtype="i4", count=1)
            nImages = nImages[0]
            w = fromfile(fileID, dtype="i4", count=1)
            w=w[0]
            h = fromfile(fileID, dtype="i4", count=1)
            h=h[0]
            pz = fromfile(fileID, dtype="f4", count=1)
            pz=pz[0]
            wavelength = fromfile(fileID, dtype="f4", count=1)
            wavelength=wavelength[0]
            n_1 = fromfile(fileID, dtype="f4", count=1)
            n_2 = fromfile(fileID, dtype="f4", count=1)
               
            hconv=single(wavelength*10**-9/(6.283185307179586*(n_2-n_1)))
            
            #timestamps = numpy.fromfile(fileID, dtype="i4", count=nImages)
            timestamps = [0] * nImages
            for k in range(0,nImages):
                timestamps[k] = fromfile(fileID, dtype="i4", count=1)
            
            #Progress bar
            # Function to update the progress bar 
            def update_progress_bar():
                
                phase_map = zeros((h,w))
                
                #write the bin files file
                for i in range(nImages):
                
                    #get image k from sequence
                    for k in range(h):
                        
                        phase_map[k,:] = fromfile(fileID, dtype="f4", count=w)
                                        
                    if conversion_factor != 1.0:
                        phase_map=single(phase_map)*conversion_factor
                    else:
                        phase_map=single(phase_map)
                    
                    #write to binfile #i
                    output_file_path=binfolder+'/'+str(i).rjust(5, '0')+'_phase.bin'
                    
                    binkoala.write_mat_bin(output_file_path, phase_map, w, h, pz, hconv, unit_code=1)
                    progress_var.set(k)  # Update progress bar value
                    
                progress_window.destroy()  # Close the progress window when done
                fileID.close
    
            # Create a new window for the progress bar
            progress_window = Toplevel(master)
            progress_window.geometry("350x100")
            progress_window.title("Conversion progress bar")
            
            # Create a progress bar widget
            progress_var = DoubleVar()
            progress_bar = ttk.Progressbar(progress_window, maximum=nImages, variable=progress_var)
            progress_bar.place(x=50, y=40, width=250) 
    
            # Run the update in a separate thread to avoid blocking the main thread
            threading.Thread(target=update_progress_bar).start()
            
            progress_window.protocol("WM_DELETE_WINDOW", lambda: None)  # Disable closing the window using the close button
            progress_window.geometry("+{}+{}".format(master.winfo_rootx() + 50, master.winfo_rooty() + 50))
            progress_window.grab_set()
            master.wait_window(progress_window)