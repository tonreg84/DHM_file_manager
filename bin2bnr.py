def bin2bnr(input_file,timestampsfile,wavelength,output_file,master):
# function for the program DHM file manager v04
    
#this function converts LynceeTec Koala bin files from one folder into a bnr sequence (LynceeTec format)
#the bin files need to end with _00000_phase.bin, _00001_phase.bin, _00002_phase.bin, ..

#input_file : select any of the bin files, you want to convert, it parent folder becomes "binfolder"
#timestampsfile: filepath of the corresponding Koala timestamps file, from there we will take the int32 array from 3rd column
#wavelength of the DHM laser, float32
#output_file: destination of the bnr sequence file

    from os.path import dirname
    import binkoala
    import numpy
    from tkinter import simpledialog
    from tkinter import messagebox
    from tkinter import ttk, Toplevel, DoubleVar
    import threading
    from hconv_choice import hconv_choice_binary2X
    
    def is_float(string):
        try:
            float(string)
            return True
        except ValueError:
            return False
    
    binfolder=dirname(input_file)
        
    #get some meta data    
    n_1 = simpledialog.askstring("Get n_1", "Please enter the first refraction index:")
    if n_1 == '' or is_float(n_1)==False:
        messagebox.showinfo('Error', 'Please enter a non-zero floating point number.')
    else:
        n_2 = simpledialog.askstring("Get n_2", "Please enter the second refraction index:")
        if n_2 == '' or is_float(n_2)==False:
            messagebox.showinfo('Error', 'Please enter a non-zero floating point number.')
        else:
            
            #get conversion factor
            (conv_check, conversion_factor)=hconv_choice_binary2X(master,input_file)
            print('Choice of conversion factor:',conv_check, conversion_factor)
            
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
                
                #Progress bar
                # Function to update the progress bar 
                def update_progress_bar():
                    
                    #write the images of the sequence to bnr file
                    for k in range(0,nImages):
            
                        input_file_path=binfolder+'/'+str(k).rjust(5, '0')+'_phase.bin'
                        (phase_map,in_file_header)=binkoala.read_mat_bin(input_file_path)
                        
                        if conversion_factor != 1.0:
                            phase_map=phase_map*conversion_factor
                            
                        phase_map.astype(numpy.float32).tofile(fileID)
                        
                        progress_var.set(k)  # Update progress bar value
            
                    progress_window.destroy()  # Close the progress window when done
                    fileID.close()
            
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