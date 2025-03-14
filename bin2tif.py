def bin2tif(input_file,wavelength,output_file,master):
    '''
    function for the program DHM file manager v04
    
    this function converts LynceeTec Koala bin files from one folder into a tiff stack file
    the bin files need to end with _00000_phase.bin, _00001_phase.bin, _00002_phase.bin, ..
    
    input_file : select any of the bin files, you want to convert, it parent folder becomes "binfolder"
    timestampsfile: filepath of the corresponding Koala timestamps file, from there we will take the int32 array from 3rd column
    wavelength of the DHM laser, float32
    output_file: destination of the tif sequence file
    '''

    from os.path import dirname
    from os import listdir
    import binkoala
    from tifffile import imsave
    from tkinter import ttk, Toplevel, DoubleVar, messagebox, Button
    import threading
    from hconv_choice import hconv_choice_binary2X

    binfolder=dirname(input_file)
    
    #get conversion factor
    (conv_check, conversion_factor)=hconv_choice_binary2X(master,input_file)
    print('Choice of conversion facot:',conv_check, conversion_factor)

    if conv_check == True:
    #choice of conversion factor -END

        # get the list of bin files to process
        bin_files = []
        bin_files = sorted([f for f in listdir(binfolder) if f.endswith(('.bin'))])
        
        cancel = False
        
        #Progress bar
        # Function to update the progress bar 
        def update_progress_bar():
            nonlocal cancel
            k=0
            #convert the bin files to tif files
            for file in bin_files:
                
                if cancel:
                    print(f"File conversion cancelled at frame {k}!")
                    messagebox.showinfo('Cancelled', f"File conversion cancelled at frame {k}!")
                    break
                
                infile=binfolder+'/'+file
                (phase_map,in_file_header)=binkoala.read_mat_bin(infile)
                
                if conversion_factor != 1.0:
                    phase_map=phase_map*conversion_factor
                
                imsave(output_file, phase_map, photometric='minisblack', compression=5, append=True, bitspersample=32, planarconfig=1, subfiletype=3)
        
                progress_var.set(k)  # Update progress bar value
                k+=1
    
            progress_window.destroy()  # Close the progress window when done
    
        def stop_process():
            nonlocal cancel
            cancel = True
    
        # Create a new window for the progress bar
        progress_window = Toplevel(master)
        progress_window.geometry("350x100")
        progress_window.title("Conversion progress bar")
        
        # Create a progress bar widget
        progress_var = DoubleVar()
        progress_bar = ttk.Progressbar(progress_window, maximum=len(bin_files), variable=progress_var)
        progress_bar.place(x=50, y=40, width=250)   
        
        # Add a "Cancel" button to stop the process
        cancel_button = Button(progress_window, text="Cancel", command=stop_process)
        cancel_button.place(x=130, y=70)
    
        # Run the update in a separate thread to avoid blocking the main thread
        threading.Thread(target=update_progress_bar).start()
        
        # Allow closing the window by pressing the close button
        progress_window.protocol("WM_DELETE_WINDOW", stop_process)
        
        progress_window.geometry("+{}+{}".format(master.winfo_rootx() + 50, master.winfo_rooty() + 50))
        progress_window.grab_set()
        master.wait_window(progress_window)