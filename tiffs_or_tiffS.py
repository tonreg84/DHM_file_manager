def tiffs_or_tiffS(in_file_extension):
    
#in_file_extension: string
    
    from PySimpleGUI import Text
    from PySimpleGUI import Button
    from PySimpleGUI import Window
    from PySimpleGUI import WIN_CLOSED
    
    tiff_go_on=True
    if in_file_extension == '.tif':
    
        Alayout = [
            [Text('You have chosen a tiff file as input.\n\nIs it a TIFF stack containing a sequence or \na series of single-image TIFF files?'),],
            [Button(button_text='TIFF stack',enable_events=True, key='tiffstack'),
             Button(button_text='single-image files',enable_events=True, key='tiffsingle'),
             Button(button_text='Cancel',enable_events=True, key='cancel-button'),
             ],
            ]
        
        tiff_win = Window('tiff or tiffS?', Alayout, size=(275, 125))
        
        #open the popup window
        tiff_win_check=True
        tiff_go_on=False
        while tiff_win_check == True:
            event, values = tiff_win.read()
            
            if event == WIN_CLOSED:
                tiff_win_check=False
                
            if event == 'cancel-button':
                tiff_win_check=False
                
            if event == 'tiffstack':
                tiff_win_check=False
                tiff_go_on=True
            
            if event == 'tiffsingle':
                tiff_win_check=False
                tiff_go_on=True
                in_file_extension='.single_tiffs'
        tiff_win.close()
    
    return(tiff_go_on,in_file_extension)