def tif2bnr(input_file,timestampsfile,wavelength,output_file,master):
#this function converts a tiff sequence (data from LynceeTec Koala) into a bnr sequence (LynceeTec format)

#input_file: filepath of the tiff sequence
#timestampsfile: int32 array from 3rd column of Koala timestamps file
#output_file: destination of the bnr sequence file

    import numpy
    from tifffile import imread
    
    from tkinter import ttk, Toplevel, DoubleVar
    import threading
    from hconv_choice import hconv_choice_tif2binary
    
    def is_float(string):
        try:
            float(string)
            return True
        except ValueError:
            return False
    
    #get conversion factor
    (conv_check, conversion_factor, n_1, n_2, pz)=hconv_choice_tif2binary(master,wavelength)
    print('Choice of conversion factor:',conv_check, conversion_factor, n_1, n_2, pz)
    
    if conv_check == True:
    
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
    
        #get image width and height from first image of tiff stack
        phase_map = imread(input_file, key=0)
        
        w = len(phase_map[0,:])
        h = len(phase_map[:,0])
    
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
        # Function to update the progress bar 
        def update_progress_bar():
            
            #write the bin files
            for k in range(nImages):
            
                #get image k from tiff stack                                     
                if conversion_factor != 1.0:
                    phase_map = imread(input_file, key=k)*conversion_factor
                else:
                    phase_map = imread(input_file, key=k)
                    
                phase_map.astype(numpy.float32).tofile(fileID)
                
                progress_var.set(k)  # Update progress bar value
                
            progress_window.destroy()  # Close the progress window when done
            fileID.close()
            
        # Create a new window for the progress bar
        progress_window = Toplevel()
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