def tiffs_or_tiffS(master):
    import tkinter as tk
    go_on=False
    tiff_type=None

    def check(w):
        #if tik one box, set the other to false
        if w=='stack':
            if vstack.get() == True:
                vsingle.set(False)
        if w=='single':
            if vsingle.get() == True:
                vstack.set(False)

    def confirm():    
        nonlocal a
        if vstack.get():
            a=1
            window.destroy()
        elif vsingle.get():
            a=2
            window.destroy()
        
    def cancel():
        window.destroy()
    
    a=None
    
    window = tk.Toplevel(master)
    window.geometry("210x130")
    window.title('-_-')

    label = tk.Label(window, text= 'You have chosen a tiff file as input.')
    label.pack()
    vstack=tk.BooleanVar()
    vsingle=tk.BooleanVar()
    stackbutton = tk.Checkbutton(window, text='It is a tiff stack file.', variable=vstack, command=lambda: check('stack'))
    stackbutton.pack()
    stackbutton = tk.Checkbutton(window, text='These are single-image tiff files.', variable=vsingle, width=25, height=1, command=lambda: check('single'))
    stackbutton.pack()
    stackbutton = tk.Button(window, text='Confirm', width=6, height=1, command=confirm)
    stackbutton.pack()
    stackbutton = tk.Button(window, text='Cancel', width=5, height=1, command=cancel)
    stackbutton.pack(pady=5)

    window.protocol("WM_DELETE_WINDOW", lambda: None)  # Disable closing the window using the close button
    window.geometry("+{}+{}".format(master.winfo_rootx() + 50, master.winfo_rooty() + 50))
    window.grab_set()
    master.wait_window(window)

    if a==1:
        go_on=True
        tiff_type='.tif'
    elif a==2:
        go_on=True
        tiff_type='.singletif'
    
    return(go_on,tiff_type)