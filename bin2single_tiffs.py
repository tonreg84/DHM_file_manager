def bin2tiffS(input_file,timestampsfile,wavelength,output_folder,master):
#this function converts a tiff sequence into single-image tiff files

#input_file: filepath of one of the bin files
#timestampsfile: int32 array from 3rd column of Koala timestamps file
#output_file -> the tiff files will be saved in the folder "output_file_tiff files"

    from os.path import dirname, isdir, basename
    from os import mkdir
    import binkoala
    from tifffile import imsave
    from numpy import array, single
    from tkinter import ttk, Toplevel, DoubleVar, messagebox
    import threading
    from hconv_choice import hconv_choice_binary2X
    
    def onlyname(file_path):
        basenema=basename(file_path)
        alist=basenema.split('.')
        namebase=''
        for k in range(len(alist)-2):
            namebase=namebase+alist[k]+'.'
        namebase=namebase+alist[len(alist)-2]
        return namebase
    
    binfolder=dirname(input_file)
    
    #outputfolder:
    tifffolder = output_folder+'/'+onlyname(input_file)+'_tiff files'
    #check if tifffolder exists aready
    do_it=False
    if isdir(tifffolder)==True:
        result = messagebox.askquestion('Output folder exits already!', 'Do you want to proceed?')
        if result == 'yes':
            do_it=True
    else:
        do_it=True
        mkdir(tifffolder)
    
    if do_it==True:
        
        #get conversion factor
        (conv_check, conversion_factor)=hconv_choice_binary2X(master,input_file)
        print('Choice of conversion facot:',conv_check, conversion_factor)
    
        if conv_check == True:

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
                
                #write the images of the sequence to bnr file
                for k in range(0,nImages):
                    input_file_path=binfolder+'/'+str(k).rjust(5, '0')+'_phase.bin'
                    (phase_map,in_file_header)=binkoala.read_mat_bin(input_file_path)
                    
                    if conversion_factor != 1.0:
                        phase_map=phase_map*conversion_factor
                    
                    #write to tiff file #k
                    output_file_path=tifffolder+'/'+str(k).rjust(5, '0')+'_phase.tif'
                    imsave(output_file_path, phase_map, photometric='minisblack', compression=5, append=True, bitspersample=32, planarconfig=1, subfiletype=3)
                    
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