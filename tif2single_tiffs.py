def tif2tiffS(input_file,timestampsfile,wavelength,output_folder,master):
# function for the program DHM file manager v04
    
#this function converts a tiff sequence into single tiff files

#input_file: filepath of the tiff sequence
#timestampsfile: int32 array from 3rd column of Koala timestamps file#timestampsfile: filepath of the corresponding Koala timestamps file, from there we will take the int32 array from 3rd column#output_file -> the tiff files will be saved in the folder "output_file_tiff files"
#wavelength of the DHM laser, float32
#output_folder -> the tiff files will be saved in the folder output_folder+'_tiff files'

    from os.path import isdir, basename
    from os import mkdir
    from tifffile import imsave
    from tifffile import imread
    from numpy import single, array
    
    from tkinter import messagebox, ttk, Toplevel, DoubleVar
    import threading
    from hconv_choice import hconv_choice_tif2tif
    
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
        
    #get conversion factor
    (conv_check, conversion_factor, n_1, n_2, pz)=hconv_choice_tif2tif(master,wavelength)
    print('Choice of conversion factor:', conv_check, conversion_factor)
    
    if conv_check == True:
    
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
                
                #write the bin files
                for k in range(nImages):
                
                    #get image k from tiff stack                                     
                    if conversion_factor != 1.0:
                        phase_map = imread(input_file, key=k)*conversion_factor
                    else:
                        phase_map = imread(input_file, key=k)
                    
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