def bnr2tif(input_file,timestampsfile,wavelength,output_file,master):
# function for the program DHM file manager v04
    
#this function converts LynceeTec Possum bnr sequence into a tiff stack file

#input_file: filepath of the bnr sequence
#timestampsfile: filepath of the corresponding Koala timestamps file, from there we will take the int32 array from 3rd column
#wavelength of the DHM laser, float32
#output_file: destination file of the tiff stack

    from numpy import fromfile, single, zeros
    from tifffile import imsave
    from tkinter import ttk, Toplevel, DoubleVar
    import threading
    from hconv_choice import hconv_choice_binary2X
    
    def is_float(string):
        try:
            float(string)
            return True
        except ValueError:
            return False
    
    #get conversion factor
    (conv_check, conversion_factor)=hconv_choice_binary2X(master,input_file)
    print('Choice of conversion factor:',conv_check, conversion_factor)
    
    if conv_check == True:
            
        #get data from bnr file
        fileID = open(input_file, 'rb')
        
        #open bnr file and run trought header
        nImages = fromfile(fileID, dtype="i4", count=1)
        nImages = nImages[0]
        w = fromfile(fileID, dtype="i4", count=1)
        w=w[0]
        h = fromfile(fileID, dtype="i4", count=1)
        h=h[0]
        pz_placeholder = fromfile(fileID, dtype="f4", count=1)
        wavelength = fromfile(fileID, dtype="f4", count=1)
        n_1 = fromfile(fileID, dtype="f4", count=1)
        n_2 = fromfile(fileID, dtype="f4", count=1)
        
        timestamps = [0] * nImages
        for k in range(0,nImages):
            timestamps[k] = fromfile(fileID, dtype="f4", count=1)

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
                
                imsave(output_file, phase_map, photometric='minisblack', compression=5, append=True, bitspersample=32, planarconfig=1, subfiletype=3)

                progress_var.set(k)  # Update progress bar value
                
            progress_window.destroy()  # Close the progress window when done
            fileID.close

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
