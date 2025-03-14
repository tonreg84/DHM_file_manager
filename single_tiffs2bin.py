def tiffS2bin(input_file,wavelength,output_folder, master):
    '''
    function for the program DHM file manager v04
        
    this function converts single-image tiff files into LynceeTec single-image bin files
    the input tiff files need to end with _00000_phase.tif, _00001_phase.tif, _00002_phase.tif, ..
    
    input_file: filepath of one of the single tiff files, tiff file names: XXXXX_phase.tif
    wavelength of the DHM laser, float32
    output_file -> the tiff files will be saved in the folder "output_file_tiff files"
    '''

    from os.path import isdir, dirname
    from os import mkdir, listdir
    from tifffile import imread
    import binkoala
    
    from tkinter import ttk, Toplevel, DoubleVar, messagebox, Button
    import threading
    from hconv_choice import hconv_choice_tif2binary
    
    def is_float(string):
        try:
            float(string)
            return True
        except ValueError:
            return False
        
    def onlyname(file_path):
        from os.path import basename
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
                if len(listdir(binfolder)) != 0:
                    answ = messagebox.askquestion('Output folder is not empty!', 'Do you want to proceed?')
                    if answ == "yes":
                        do_it=True
                else: do_it = True
        else:
            do_it=True
            mkdir(binfolder)
        
        if do_it==True:
        
            #get first image from the chosen tiff file
            phase_map = imread(input_file, key=0)
            
            w = len(phase_map[0,:])
            h = len(phase_map[:,0])
            
            # get the list of bin files to process
            tif_files = []
            tif_files = sorted([f for f in listdir(tifffolder) if f.endswith(('.tif'))])
            
            cancel = False
            
            #Progress bar
            # Function to update the progress bar 
            def update_progress_bar():
                nonlocal cancel
                k=0
                #write the bin files
                for file in tif_files:
                    
                    if cancel:
                        print(f"File conversion cancelled at frame {k}!")
                        messagebox.showinfo('Cancelled', f"File conversion cancelled at frame {k}!")
                        break
                
                    infile=tifffolder+'/'+file
                    
                    #get image k from tiff stack                                     
                    if conversion_factor != 1.0:
                        phase_map = imread(infile, key=0)*conversion_factor
                    else:
                        phase_map = imread(infile, key=0)
                    
                    #write to binfile #k
                    outfile=binfolder +'/'+ onlyname(file) + '.bin'
                    
                    binkoala.write_mat_bin(outfile, phase_map, w, h, pz, hconv, unit_code=1)
                    
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
            progress_bar = ttk.Progressbar(progress_window, maximum=len(tif_files), variable=progress_var)
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