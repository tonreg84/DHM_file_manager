def tif2bin(input_file,wavelength,output_folder,master):
    '''
    function for the program DHM file manager v04
    
    this function converts a tiff stack (data from LynceeTec Koala) into single-image bin files (LynceeTec format)
    
    input_file: filepath of the tiff sequence
    wavelength of the DHM laser, float32
    output_file -> the bin files will be saved in the folder "output_file_Bin files"
    '''

    import binkoala
    from os.path import isdir
    from os import mkdir
    from tifffile import imread
    from tkinter import messagebox, ttk, Toplevel, DoubleVar, Button
    import threading
    from hconv_choice import hconv_choice_tif2binary
        
    def onlyname(file_path):
        from os.path import basename
        basenam=basename(file_path)
        alist=basenam.split('.')
        namebase=''
        for k in range(len(alist)-2):
            namebase=namebase+alist[k]+'.'
        namebase=namebase+alist[len(alist)-2]
        return namebase
    
    #get conversion factor
    (conv_check, conversion_factor, n_1, n_2, pz)=hconv_choice_tif2binary(master,wavelength)
    print('Choice of conversion factor:',conv_check, conversion_factor, n_1, n_2, pz)
    hconv=wavelength/(6.283185307179586*(n_2-n_1))*10**-9
    
    if conv_check == True:
    
        #outputfolder:
        binfolder = output_folder+'/'+onlyname(input_file)+'_bin files'
        #check if tifffolder exists aready
        do_it=False
        if isdir(binfolder)==True:
            result = messagebox.askquestion('Output folder exits already!', 'Do you want to proceed?')
            if result == 'yes':
                do_it=True
        else:
            do_it=True
            mkdir(binfolder)
        
        if do_it==True:
    
            # Get sequence length
            l = 0
            while True:

                try:
                    imread(input_file, key=l)
                    l+=1
                except:
                    nImages = l
                    print("Seqeuence lenght:",nImages)
                    break

            #get image width and height from first image of tiff stack
            phase_map = imread(input_file, key=0)
            
            w = len(phase_map[0,:])
            h = len(phase_map[:,0])
        
            cancel = False
            
            #Progress bar
            # Function to update the progress bar 
            def update_progress_bar():
                nonlocal cancel
                
                #write the bin files
                for k in range(nImages):
                    
                    if cancel:
                        print(f"File conversion cancelled at frame {k}!")
                        messagebox.showinfo('Cancelled', f"File conversion cancelled at frame {k}!")
                        break
                
                    #get image k from tiff stack                                     
                    if conversion_factor != 1.0:
                        phase_map = imread(input_file, key=k)*conversion_factor
                    else:
                        phase_map = imread(input_file, key=k)
                    
                    #write to binfile #k
                    output_file_path=binfolder+'/'+str(k).rjust(5, '0')+'_phase.bin'
                    
                    binkoala.write_mat_bin(output_file_path, phase_map, w, h, pz, hconv, unit_code=1)
                    
                    progress_var.set(k)  # Update progress bar value
                    
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