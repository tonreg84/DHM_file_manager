def bin2bnr(input_file,timestampsfile,wavelength,output_file,master):
    '''
    function for the program DHM file manager v04
        
    this function converts LynceeTec Koala bin files from one folder into a bnr sequence (LynceeTec format)
    the bin files need to end with _00000_phase.bin, _00001_phase.bin, _00002_phase.bin, ..
    
    input_file : select any of the bin files, you want to convert, it parent folder becomes "binfolder"
    timestampsfile: filepath of the corresponding Koala timestamps file, from there we will take the int32 array from 3rd column
    wavelength of the DHM laser, float32
    output_file: destination of the bnr sequence file
    '''

    from os.path import dirname
    from os import listdir
    import binkoala
    import numpy
    from tkinter import ttk, Toplevel, DoubleVar, Button, simpledialog, messagebox
    import threading
    from hconv_choice import hconv_choice_binary2X
    
    def is_float(string):
        try:
            float(string)
            return True
        except ValueError:
            return False
    
    binfolder = dirname(input_file)
        
    #get some meta data    
    n_1 = simpledialog.askstring("Get n_1", "Please enter the first refraction index:")
    if is_float(n_1)==False:
        messagebox.showinfo('Error', 'Please enter a non-zero floating point number.')
    else:
        n_2 = simpledialog.askstring("Get n_2", "Please enter the second refraction index:")
        if is_float(n_2)==False:
            messagebox.showinfo('Error', 'Please enter a non-zero floating point number.')
        else:
            
            #get conversion factor
            (conv_check, conversion_factor)=hconv_choice_binary2X(master,input_file)
            print('Choice of conversion factor:',conv_check, conversion_factor)
            
            if conv_check == True:
                
                # get the list of bin files to process
                bin_files = []
                bin_files = sorted([f for f in listdir(binfolder) if f.endswith(('.bin'))])
                
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
            
                (phase_map,in_file_header)=binkoala.read_mat_bin(input_file)
                w=in_file_header['width'][0]
                h=in_file_header['height'][0]
                pz=in_file_header['px_size'][0]
                
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
                
                cancel = False
                
                #Progress bar
                # Function to update the progress bar 
                def update_progress_bar():
                    nonlocal cancel
                               
                    k = 0
                    #write the images of the sequence to bnr file
                    for file in bin_files:
                        
                        if cancel:
                            print(f"File conversion cancelled at frame {k}!")
                            messagebox.showinfo('Cancelled', f"File conversion cancelled at frame {k}!")
                            break
            
                        infile=binfolder+'/'+file
                        (phase_map,in_file_header)=binkoala.read_mat_bin(infile)
                        
                        if conversion_factor != 1.0:
                            phase_map=phase_map*conversion_factor
                            
                        phase_map.astype(numpy.float32).tofile(fileID)
                        
                        progress_var.set(k)  # Update progress bar value
                        k += 1
            
                    progress_window.destroy()  # Close the progress window when done
                    fileID.close()
                
                def stop_process():
                    nonlocal cancel
                    cancel = True
                
                # Create a new window for the progress bar
                progress_window = Toplevel(master)
                progress_window.geometry("350x100")
                progress_window.title("Conversion progress bar")
                
                # Create a progress bar widget
                progress_var = DoubleVar()
                progress_bar = ttk.Progressbar(progress_window, maximum=nImages, variable=progress_var)
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