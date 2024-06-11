def tiffS2bin(input_file,timestampsfile,wavelength,output_folder, master):
# function for the program DHM file manager v04
    
#this function converts single-image tiff files into LynceeTec single-image bin files
#the input tiff files need to end with _00000_phase.tif, _00001_phase.tif, _00002_phase.tif, ..

#input_file: filepath of one of the single tiff files, tiff file names: XXXXX_phase.tif
#timestampsfile: filepath of the corresponding Koala timestamps file, from there we will take the int32 array from 3rd column
#wavelength of the DHM laser, float32
#output_file -> the tiff files will be saved in the folder "output_file_tiff files"

    from os.path import isdir, basename, dirname
    from os import mkdir
    from tifffile import imread
    import numpy
    import binkoala
    
    from tkinter import ttk, Toplevel, DoubleVar, messagebox
    import threading
    from hconv_choice import hconv_choice_tif2binary
    
    def is_float(string):
        try:
            float(string)
            return True
        except ValueError:
            return False
        
    def onlyname(file_path):
        basenam=basename(file_path)
        alist=basenam.split('.')
        namebase=''
        for k in range(len(alist)-2):
            namebase=namebase+alist[k]+'.'
        namebase=namebase+alist[len(alist)-2]
        return namebase

    tifffolder=dirname(input_file)
    
    #get conversion factor
    (conv_check, conversion_factor, n_1, n_2, pz)=hconv_choice_tif2binary(master,wavelength)
    print('Choice of conversion factor:',conv_check, conversion_factor, n_1, n_2, pz)
    hconv=wavelength/(6.283185307179586*(n_2-n_1))*10**-9
    
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
        
            #get first image from the chosen tiff file
            phase_map = imread(input_file, key=0)
            
            w = len(phase_map[0,:])
            h = len(phase_map[:,0])
            
            #Progress bar
            # Function to update the progress bar 
            def update_progress_bar():
                
                #write the bin files
                for k in range(nImages):
                
                    input_file_path=tifffolder+'/'+str(k).rjust(5, '0')+'_phase.tif'
                    
                    #get image k from tiff stack                                     
                    if conversion_factor != 1.0:
                        phase_map = imread(input_file_path, key=0)*conversion_factor
                    else:
                        phase_map = imread(input_file_path, key=0)
                    
                    #write to binfile #k
                    output_file_path=binfolder+'/'+str(k).rjust(5, '0')+'_phase.bin'
                    
                    binkoala.write_mat_bin(output_file_path, phase_map, w, h, pz, hconv, unit_code=1)
                    
                    progress_var.set(k)  # Update progress bar value
                    
                progress_window.destroy()  # Close the progress window when done
            
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