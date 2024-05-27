def bin2tif(input_file,timestampsfile,wavelength,output_file,master):
#this function converts LynceeTec Koala bin files from one folder into a tif sequence
#the bin files need to end with _00000_phase.bin, _00001_phase.bin, _00002_phase.bin, ..

#input_file : select any of the bin files, you want to convert, it parent folder becomes "binfolder"
#timestampsfile: int32 array from 3rd column of Koala timestamps file
#wavelength of the DHM laser, float32
#output_file: destination of the tif sequence file

    from os.path import dirname
    import binkoala
    from tifffile import imsave
    from numpy import array, single
    from tkinter import ttk, Toplevel, DoubleVar
    import threading
    from hconv_choice import hconv_choice_binary2X

    binfolder=dirname(input_file)
    
    #get conversion factor
    (conv_check, conversion_factor)=hconv_choice_binary2X(master,input_file)
    print('Choice of conversion facot:',conv_check, conversion_factor)

    if conv_check == True:
    #choice of conversion factor -END

        #read timestamps from timestampsfile
        with open(timestampsfile, 'r') as infile:
            
            k=0
            timelist=[]
            for line in infile:
                # Split the line into a list of numbers
                numbers = line.split()
                time=single(float(numbers[3]))
                timelist.append(time)
                k=k+1          
            timestamps=array(timelist)
            
        nImages=len(timestamps) #sequence length
        
        #Progress bar
        # Function to update the progress bar 
        def update_progress_bar():
            
            #write the images of the sequence to tif file
            for k in range(0,nImages):
                input_file_path=binfolder+'/'+str(k).rjust(5, '0')+'_phase.bin'
                (phase_map,in_file_header)=binkoala.read_mat_bin(input_file_path)
                
                if conversion_factor != 1.0:
                    phase_map=phase_map*conversion_factor
                
                imsave(output_file, phase_map, photometric='minisblack', compression=5, append=True, bitspersample=32, planarconfig=1, subfiletype=3)
        
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