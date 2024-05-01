"""
DHM file manager
Autor: tonreg, team UMI, CNP-CHUV Lausanne
 
Version 03 - 01.05.2024

This program is used to post-process data recorded during one experience with a LynceeTec DHM.

This program does:
a) open "bin" and "bnr" image files written by LynceeTec Koala or LynceeTec Possum, aw well as TIFF files, and shows the header information for "bin" and "bnr" files.

b) convert files between "LynceeTec" formats
   - Supported input file formats:
     - "bin" - a series of binary file, where every file is a single image of a DHM recording.
     - "bnr" - a binary file containing a sequence of images of a DHM recording.
     - "tiff stack" - a TIFF file containing a sequence of images of a DHM recording.
     - "single-image tiff files" - a series of TIFF files, where every file is a single image of a DHM recording.
   - Supported output file formats:
     - "bin"
     - "bnr"
     - "tiff stack"
     - "single-image tiff files"
     
c) modify the header of all bin files of a choosen folder. Click button "Bin-file header mod" to access this function.

d) modify the header of a bnr file. Click button "Bnr-file header mod" to access this function. 
"""

import os
import PySimpleGUI as simgui
import os.path
import binkoala
import tifffile

from bin2bnr import bin2bnr
from bin2tif import bin2tif
from bnr2tif import bnr2tif
from bnr2bin import bnr2bin
from tif2bin import tif2bin
from tif2bnr import tif2bnr
from tif2single_tiffs import tif2tiffS
from bin2single_tiffs import bin2tiffS
from bnr2single_tiffs import bnr2tiffS
from single_tiffs2tiff import tiffS2tiff
from single_tiffs2bin import tiffS2bin
from single_tiffs2bnr import tiffS2bnr
from tiffs_or_tiffS import tiffs_or_tiffS

import numpy
from skimage.transform import resize

import matplotlib.image

from modify_header import modify_bin_header
from modify_header import modify_bnr_header

#some control variables:
infilewithness=None
showheaderwithness=None
outform=None
out_file_name=''
out_file_folder=''
out_file_path=''

#info window
with open('info.txt') as f:
    infotext=f.read()
f.close()

# First the window layout in 3 columns
files_and_parameter = [
    [
        simgui.Text("Input file:"),
        simgui.In(size=(50, 1), enable_events=True, key="infilepath"),
        simgui.FileBrowse(),
    ],
    [
        simgui.Text("Timestamp file:"),
        simgui.In(size=(50, 1), enable_events=True, key='timefilepath'),
        simgui.FileBrowse(),
    ],
    [
        simgui.Text("Laser wavelength in nm:"),
        simgui.Checkbox("682.5", enable_events=True, key='682'),
        simgui.Checkbox("666", enable_events=True, key='666'),
    ],
    [
        simgui.Text("Output format:"),
        simgui.Checkbox("bin", enable_events=True, key='outformbin'),
        simgui.Checkbox("bnr", enable_events=True, key='outformbnr'),
        simgui.Checkbox("tiff stack", enable_events=True, key='outformtif'),
        simgui.Checkbox("single-image tiff files", enable_events=True, key='outformtifS'),
    ],
    [
         simgui.Text("Output file folder:"),
         simgui.In(size=(30, 1), enable_events=True, key="outfilefolder"),
         simgui.FolderBrowse(),simgui.Button(button_text='Same as input file',enable_events=True, key="outfolderbutton"),
    ],
    [
         simgui.Text("Output file name:"),
         simgui.In(size=(30, 1), enable_events=True, key="outfilename"),
    ],
    [
        simgui.Button("Start file conversion!", enable_events=True, key='startfileconv'),
        simgui.Multiline(default_text='File conversion info: slecting input', enable_events=True, size=(50, 3), key='convinf'),
    ],
    [
         simgui.Text("   "),
    ],
    [
        simgui.Button(button_text='Bin-file header mod',enable_events=True, key="bin_head_mod"),
        simgui.Button(button_text='Bnr-file header mod',enable_events=True, key="bnr_head_mod"),
        simgui.Text("                                                     "),
        simgui.Button(button_text='Info',enable_events=True, key="infobutton"),
    ],
]
#header display column
header_column = [
    [
     simgui.Text("Input file info:")],
    [simgui.Multiline(default_text='No input file selected.', enable_events=True, size=(35, 15), key='headerdisplay')
    ],
]
# image display column
display_column = [
    [simgui.Text("Input file image:")],
    [simgui.Image(key="display")],
]

# ----- Full layout -----
layout = [
    [
        simgui.Column(files_and_parameter),
        simgui.VSeperator(),
        simgui.Column(header_column),
        simgui.VSeperator(),
        simgui.Column(display_column),
    ]
]

window = simgui.Window("DHM file manager", layout)

# Main programme
while True:
    event, values = window.read()
    if event == simgui.WIN_CLOSED:
        break
    
    if event == 'infobutton':
        simgui.popup_scrolled(infotext, title="Info", font=("Arial Bold", 9), size=(100,20))
    
    #modify header of bin files - START
    if event == 'bin_head_mod':
        binfolder=simgui.popup_get_folder('Please select a folder with bin files:',  title="Chose bin folder")
        if binfolder!=None:
            if binfolder=='':
                simgui.popup_auto_close('Error: No folder selected.')
            elif os.path.isdir(binfolder)==False:
                simgui.popup_auto_close('Error: This folder doesn\'t exist.')
            else: 
                modify_bin_header(binfolder)
    #modify header of bin files - END
    
    #modify header of bnr files - START
    if event == 'bnr_head_mod':
        bnrfile=simgui.popup_get_file('Please select a bnr file:',  title="Chose bnr file")
        print(bnrfile)
        if bnrfile!=None:
            if bnrfile=='':
                simgui.popup_auto_close('Error: No file selected.')
            elif os.path.isfile(bnrfile)==False:
                simgui.popup_auto_close('Error: This file doesn\'t exist.')
            else: 
                modify_bnr_header(bnrfile)
    #modify header of bnr files - END
    
    #if tik one box, then set all others to false, suggest output file name,
    #change outfile format if we tick another output format box
    if event == '682':
        if window['682'].get() == True:
            window['666'].update(value=False)
            wavelength=682.5
        else: wavelength=None
    if event == '666':
        if window['666'].get() == True:
            window['682'].update(value=False)
            wavelength=665.8
        else: wavelength=None
    if event == 'outformbin':
        if window['outformbin'].get() == True:
            window['outformbnr'].update(value=False)
            window['outformtif'].update(value=False)
            window['outformtifS'].update(value=False)
            outform='.bin'

            window['outfilename'].update(disabled=True)
            
            out_file_name='0000X_phase.bin'
            window['outfilename'].update(value=out_file_name)
            
            window['convinf'].update(value='File conversion info: selecting input\nOutput format = single-image bin files, The programme will add \"_Bin files\" to the choosen output folder.')

        else:
            outform=None
            window['outfilename'].update(disabled=False)
    if event == 'outformbnr':
        if window['outformbnr'].get() == True:
            window['outformbin'].update(value=False)
            window['outformtif'].update(value=False)
            window['outformtifS'].update(value=False)
            outform='.bnr'
            
            window['outfilename'].update(disabled=False)
            window['convinf'].update(value='File conversion info: selecting input\nOutput format = bnr (bin stack).')
            
            #change outfile format if we tick another output format box
            if values['outfilename'] != '':
                out_file_name=values['outfilename']
                alist=out_file_name.split('.')
                
                if len(alist) == 1:
                    out_file_name=out_file_name+outform
                else:
                    namebase=''
                    for k in range(len(alist)-2):
                        namebase=namebase+alist[k]+'.'
                    namebase=namebase+alist[len(alist)-2]
                    out_file_name=namebase+outform
                    
                window['outfilename'].update(value=out_file_name)
                
        else: outform=None
    if event == 'outformtif':
        if window['outformtif'].get() == True:
            window['outformbnr'].update(value=False)
            window['outformbin'].update(value=False)
            window['outformtifS'].update(value=False)
            outform='.tif'
            
            window['outfilename'].update(disabled=False)
            window['convinf'].update(value='File conversion info: selecting input\nOutput format = tiff stack.')
            
            #change outfile format if we tick another output format box
            if values['outfilename'] != '':
                out_file_name=values['outfilename']
                alist=out_file_name.split('.')
                
                if len(alist) == 1:
                    out_file_name=out_file_name+outform
                else:
                    namebase=''
                    for k in range(len(alist)-2):
                        namebase=namebase+alist[k]+'.'
                    namebase=namebase+alist[len(alist)-2]
                    out_file_name=namebase+outform
                    
                window['outfilename'].update(value=out_file_name)
                
        else: outform=None
    if event == 'outformtifS':
        if window['outformtifS'].get() == True:
            window['outformbnr'].update(value=False)
            window['outformbin'].update(value=False)
            window['outformtif'].update(value=False)
            outform='.single_tiffs'
            
            window['outfilename'].update(disabled=True)
            
            out_file_name='0000X_phase.tif'
            window['outfilename'].update(value=out_file_name)
            
            window['convinf'].update(value='File conversion info: selecting input\nOutput format = single-image tiff files, The programme will add \"_tiff files\" to the choosen output folder.')

        else:
            outform=None
            window['outfilename'].update(disabled=False)
    
    #display input file info and image
    if values['infilepath'] != "" and showheaderwithness != values['infilepath']:
        showheaderwithness = values['infilepath']
        in_file_name, in_file_extension = os.path.splitext(values['infilepath'])
        if in_file_extension == ".bin":
                    
            #get header info:
            (in_file_image,in_file_header)=binkoala.read_mat_bin(values['infilepath'])
            hv=str(in_file_header['version'][0])
            end=str(in_file_header['endian'][0])
            hz=str(in_file_header['head_size'][0])
            w=str(in_file_header['width'][0])
            h=str(in_file_header['height'][0])
            pz=str(in_file_header['px_size'][0])
            hconv=str(in_file_header['hconv'][0])
            uc=str(in_file_header['unit_code'][0])
            
            phasemin=str(in_file_image.min())
            phasemax=str(in_file_image.max())
            phaseavg=str(numpy.mean(in_file_image))
        
            in_file_info='File name: '+os.path.basename(values['infilepath'])+'\n\n'+'Header version: '+hv+'\n'+'Endianess: '+end+'\n'+'Header size: '+end+'\n'+'Width: '+w+'\n'+'Heigth: '+w+'\n'+'Pixel size [m]: '+pz+'\n'+'Height coversion factor [m]: '+hconv+'\n'+'Unit code: '+uc+' (1=rad, 2=m, 0=no unit)'+'\n\nMin: '+phasemin+'\nMax: '+phasemax+'\nMean: '+phaseavg+'\n'    
            window['headerdisplay'].update(value=in_file_info)
            print('In-File-Info:\n'+in_file_info)
            
            #in_file_image=(in_file_image-min(in_file_image))*100
            
            #show image
            #resize image to 300x300 pixels:
            dim1, dim2 = 300, 300
            in_file_image = resize(in_file_image,(dim1,dim2),order=3)
            
            in_file_image_path=os.path.dirname(values['infilepath'])+'/in_file_image.png'
            print('input file image path: '+in_file_image_path)
            matplotlib.image.imsave(in_file_image_path, in_file_image)
            window['display'].update(in_file_image_path)
            os.remove(in_file_image_path)
            
        if in_file_extension == ".bnr":
            
            #get header info:
            fileID = open(values['infilepath'], 'rb')
            nImages = numpy.fromfile(fileID, dtype="i4", count=1)
            nImages = nImages[0]
            w = numpy.fromfile(fileID, dtype="i4", count=1)
            w=w[0]
            h = numpy.fromfile(fileID, dtype="i4", count=1)
            h=h[0]
            pz = numpy.fromfile(fileID, dtype="f4", count=1)
            pz=str(pz[0])
            wave = numpy.fromfile(fileID, dtype="f4", count=1)
            waveshow=str(wave[0])
            n_1 = numpy.fromfile(fileID, dtype="f4", count=1)
            n_1=str(n_1[0])
            n_2 = numpy.fromfile(fileID, dtype="f4", count=1)
            n_2=str(n_2[0])
            #timestamps = numpy.fromfile(fileID, dtype="i4", count=nImages)
            timestamps = [0] * nImages
            for k in range(0,nImages):
                x=numpy.fromfile(fileID, dtype="i4", count=1)
                timestamps[k] = x[0]
            #get first image from sequence
            phase_map = numpy.zeros((h,w))
            for k in range(h):
                phase_map[k,:] = numpy.fromfile(fileID, dtype="f4", count=w)
            phase_map=numpy.single(phase_map)
            fileID.close
            
            phasemin=str(phase_map.min())
            phasemax=str(phase_map.max())
            phaseavg=str(numpy.mean(phase_map))
            
            in_file_info='File name: '+os.path.basename(values['infilepath'])+'\n\n'+'Sequence length: '+str(nImages)+'\n'+'Width: '+str(w)+'\n'+'Heigth: '+str(h)+'\n'+'Pixel size [m]: '+pz+'\n'+'Wavelength [nm]: '+waveshow+'\n'+'Refraction index 1: '+n_1+'\n'+'Refraction index 2: '+n_2+'\n\nMin: '+phasemin+'\nMax: '+phasemax+'\nMean: '+phaseavg+'\n'
            window['headerdisplay'].update(value=in_file_info)
            print('In-File-Info:\n',in_file_info)
            #show image
            #resize image to 300x300 pixels:
            dim1, dim2 = 300, 300
            in_file_image = resize(phase_map,(dim1,dim2),order=3)
            
            in_file_image_path=os.path.dirname(values['infilepath'])+'/in_file_image.png'
            print('input file image path: '+in_file_image_path)
            matplotlib.image.imsave(in_file_image_path, in_file_image)
            window['display'].update(in_file_image_path)
            os.remove(in_file_image_path)
            
        if in_file_extension == ".tif":
            phase_map = tifffile.imread(values['infilepath'], key=0)
            w = str(len(phase_map[0,:]))
            h = str(len(phase_map[:,0]))
            phasemin=str(phase_map.min())
            phasemax=str(phase_map.max())
            phaseavg=str(numpy.mean(phase_map))
            in_file_info='File name: '+os.path.basename(values['infilepath'])+'\n\n'+'Width: '+str(w)+'\n'+'Heigth: '+str(h)+'\n\nAttention: When converting from tiff to another format, the pixel values might needed to be devided by hconv!\n\nMin: '+phasemin+'\nMax: '+phasemax+'\nMean: '+phaseavg
            window['headerdisplay'].update(value=in_file_info)
            print('In-File-Info:\n',in_file_info)
            #show image
            #resize image to 300x300 pixels:
            dim1, dim2 = 300, 300
            in_file_image = resize(phase_map,(dim1,dim2),order=3)
            in_file_image_path=os.path.dirname(values['infilepath'])+'/in_file_image.png'
            print('input file image path: '+in_file_image_path)
            matplotlib.image.imsave(in_file_image_path, in_file_image)
            window['display'].update(in_file_image_path)
            os.remove(in_file_image_path)
    
    #suggest output file name if input file and output format are choosen
    if values['infilepath'] != "" and infilewithness != values['infilepath']:
        if window['outformbnr'].get() == True or window['outformtif'].get() == True:
            
            infilewithness = values['infilepath']
            
            alist=os.path.basename(values['infilepath']).split('.')
            namebase=''
            for k in range(len(alist)-1):
                namebase=namebase+alist[k]
            out_file_name=namebase+outform
            
            window['outfilename'].update(value=out_file_name) 
            
    if event == "outfolderbutton":
        window['outfilefolder'].update(value=os.path.dirname(values['infilepath']))
       
    #start main program = file conversion
    if event == 'startfileconv':
        print('\nStart file conversion\n -> Check input and output parameters:\n')
        
        #check if all files and parameter are choosen correctly
        
        #first check if input file is selected
        if values['infilepath'] == "": 
            print('Error: No input file selected')
            new_in_file=simgui.popup_get_file('Please select an input file:',  title="Error: No input file selected.")
            window['infilepath'].update(value=new_in_file)
            print (" Input file selected: ", values['infilepath'])
        else:
            
            if os.path.isfile(values['infilepath']) != True:
                print('Error: Input file does not exist.')
                simgui.popup_auto_close('Error: Input file does not exist.')
            else:
                print (" Input file selected: ", values['infilepath'])
            
                #now we check the input file extension
                file_name, in_file_extension = os.path.splitext(values['infilepath'])
                if in_file_extension != ".bin" and in_file_extension !=".bnr" and in_file_extension !=".tif":
                    print("Error: Wrong input file format")
                    new_in_file=simgui.popup_get_file('Please select another input file:',  title="Error: Wrong input file format.")
                    window['infilepath'].update(value=new_in_file)
                    print('New input file selected: ', new_in_file)
                else:
                    print("Correct input file format: ", in_file_extension)
    
                    #if input file is tiff, ask user if its a tiff stack file or a series of single-image tiff files
                    (tiff_go_on,in_file_extension)=tiffs_or_tiffS(in_file_extension)
                    
                    if tiff_go_on == True:
    
                        #now check if timestamp file is choosen
                        if values['timefilepath'] == '':
                            print('Error: No timestamp file selected')
                            new_in_file=simgui.popup_get_file('Please select a timestamp file:',  title="Error: No timestamp file selected.")
                            window['timefilepath'].update(value=new_in_file)
                            print("Timestamp file selected:", new_in_file)
                        else:
                            print("Timestamp file selected:", values['timefilepath'])
                            #now check if wavelength is selected
                            if window['682'].get() == False and window['666'].get() == False:
                                simgui.popup_auto_close('Error: No wavelength selected.')
                            else:
                                #nowcheck if output format selected
                                if window['outformbin'].get() == False and window['outformbnr'].get() == False and window['outformtif'].get() == False and window['outformtifS'].get() == False:
                                    simgui.popup_auto_close('Error: No output file format selected.')
                                else:
                                    
                                    #now check if output file is selected
                                    if values['outfilefolder'] == '' or values['outfilename'] == '':
                                        print('Error: No output file selected')
                                        simgui.popup_auto_close('Error: No output file selected.')
                                    else:
                                        out_file_path=values['outfilefolder']+'/'+values['outfilename']
                                        print ("Output file selected:", out_file_path)

                                        #get output format and check if output and input format are different                                
                                        if window['outformbin'].get() == True:
                                            outform='.bin'
                                        elif window['outformbnr'].get() == True:
                                            outform='.bnr'
                                        elif window['outformtif'].get() == True:
                                            outform='.tif'
                                        elif window['outformtifS'].get() == True:
                                            outform='.single_tiffs'
                                        
                                        #now checkt if in- and output files are different
                                        if values['infilepath'] == out_file_path:
                                            print('Error: Identic input and output files')
                                            simgui.popup_auto_close('Error: Identic input and output files!')
                                        else:
                                            #now checkt if in- and output formats are different
                                            if in_file_extension == outform:
                                                print('Error: Same input and output format')
                                                simgui.popup_auto_close('Error: Identic input and output format!')
                                            else:
                                                #now checkt if output file exists already (for bnr and tiff sequence file)
                                                checkit=False
                                                if outform == '.bnr' or outform == '.tif':
        
                                                    if os.path.isfile(out_file_path)==True:
                                                        print('/!\\ Output file exits already!')
                                                        checkit=simgui.popup_ok_cancel("Output file exits already!\n\n- Press Ok to proceed.\n\n-Press Cancel to stop.\n ",  title="Output file exits already!")
                                                        checkit=False
                                                    else:
                                                        checkit=True
                                                else:
                                                    checkit=True
        
                                                if checkit == True:
                                                
                                                    if in_file_extension=='.bin' and outform=='.bnr':
                                                        print('bin to bnr')
                                                        window['convinf'].update(value='File conversion info: \nconversion of bin to bnr\n\t - IN PROGRESS -')
                                                        #funtion bin to bnr:
                                                        bin2bnr(values['infilepath'],values['timefilepath'],wavelength,out_file_path)
                                                        window['convinf'].update(value='File conversion info: \nconversion of bin to bnr\n\t - DONE -')
                                                    
                                                    elif in_file_extension=='.bin' and outform=='.tif':
                                                        print('bin to tif')
                                                        window['convinf'].update(value='File conversion info: \nconversion of bin to TIFF stack\n\t - IN PROGRESS -')
                                                        #funtion bin to tif:
                                                        bin2tif(values['infilepath'],values['timefilepath'],wavelength,out_file_path)
                                                        window['convinf'].update(value='File conversion info: \nconversion of bin to TIFF stack\n\t - DONE -')
                                                    
                                                    elif in_file_extension=='.bnr' and outform=='.tif':
                                                        print('bnr to tif')
                                                        window['convinf'].update(value='File conversion info: \nconversion of bnr to TIFF stack\n\t - IN PROGRESS -')
                                                        #funtion bnr to tif
                                                        bnr2tif(values['infilepath'],values['timefilepath'],wavelength,out_file_path)
                                                        window['convinf'].update(value='File conversion info: \nconversion of bnr to TIFF stack\n\t - DONE -')
                                                    
                                                    elif in_file_extension=='.bnr' and outform=='.bin':
                                                        print('bnr to bin')
                                                        window['convinf'].update(value='File conversion info: \nconversion of bnr to bin\n\t - IN PROGRESS -')
                                                        #funtion bnr to bin
                                                        bnr2bin(values['infilepath'],values['timefilepath'],wavelength,out_file_path)
                                                        window['convinf'].update(value='File conversion info: \nconversion of bnr to bin\n\t - DONE -')
                                                   
                                                    elif in_file_extension=='.tif' and outform=='.bin':
                                                        print('tif to bin')
                                                        window['convinf'].update(value='File conversion info: \nconversion of TIFF stack to bin\n\t - IN PROGRESS -')
                                                        #funtion tif to bin
                                                        tif2bin(values['infilepath'],values['timefilepath'],wavelength,out_file_path)
                                                        window['convinf'].update(value='File conversion info: \nconversion of TIFF stack to bin\n\t - DONE -')
                                                    
                                                    elif in_file_extension=='.tif' and outform=='.bnr':
                                                        print('tif to bnr')
                                                        window['convinf'].update(value='File conversion info: \nconversion of TIFF stack to bnr\n\t - IN PROGRESS -')
                                                        #funtion tif to bnr
                                                        tif2bnr(values['infilepath'],values['timefilepath'],wavelength,out_file_path)
                                                        window['convinf'].update(value='File conversion info: \nconversion of TIFF stack to bnr\n\t - DONE -')
                                                        
                                                    elif in_file_extension=='.tif' and outform=='.single_tiffs':
                                                        print('tif to single tiffs')
                                                        window['convinf'].update(value='File conversion info: \nconversion of TIFF stack to single-image TIFF files\n\t - IN PROGRESS -')
                                                        #funtion tif to single tiffs
                                                        tif2tiffS(values['infilepath'],values['timefilepath'],wavelength,out_file_path)
                                                        window['convinf'].update(value='File conversion info: \nconversion of TIFF stack to single-image TIFF files\n\t - DONE -')
                                                        
                                                    elif in_file_extension=='.bin' and outform=='.single_tiffs':
                                                        print('bin to single tiffs')
                                                        window['convinf'].update(value='File conversion info: \nconversion of bin files to single-image TIFF files\n\t - IN PROGRESS -')
                                                        #funtion bin to single tiffs
                                                        bin2tiffS(values['infilepath'],values['timefilepath'],wavelength,out_file_path)
                                                        window['convinf'].update(value='File conversion info: \nconversion of bin files to single-image TIFF files\n\t - DONE -')
                                                
                                                    elif in_file_extension=='.bnr' and outform=='.single_tiffs':
                                                        print('bnr to single tiffs')
                                                        window['convinf'].update(value='File conversion info: \nconversion of bnr file to ssingle-image TIFF files\n\t - IN PROGRESS -')
                                                        #funtion bnr to single tiffs
                                                        bnr2tiffS(values['infilepath'],values['timefilepath'],wavelength,out_file_path)
                                                        window['convinf'].update(value='File conversion info: \nconversion of bnr file to single-image TIFF files\n\t - DONE -')
                                                        
                                                    elif in_file_extension=='.single_tiffs' and outform=='.tif':
                                                        print('single tiffs to tiff')
                                                        window['convinf'].update(value='File conversion info: \nconversion of single-image TIFF files to TIFF stack\n\t - IN PROGRESS -')
                                                        #funtion single tiffs to tiff
                                                        tiffS2tiff(values['infilepath'],values['timefilepath'],wavelength,out_file_path)
                                                        window['convinf'].update(value='File conversion info: \nconversion of single-image TIFF files to TIFF stack\n\t - DONE -')
                                             
                                                    elif in_file_extension=='.single_tiffs' and outform=='.bin':
                                                        print('single tiffs to  bin')
                                                        window['convinf'].update(value='File conversion info: \nconversion of single-image TIFF files to bin\n\t - IN PROGRESS -')
                                                        #funtion single tiffs to tiff
                                                        tiffS2bin(values['infilepath'],values['timefilepath'],wavelength,out_file_path)
                                                        window['convinf'].update(value='File conversion info: \nconversion of single-image TIFF files to bin\n\t - DONE -')
                
                                                    elif in_file_extension=='.single_tiffs' and outform=='.bnr':
                                                        print('single tiffs to  bnr')
                                                        window['convinf'].update(value='File conversion info: \nconversion of single-image TIFF files to bnr\n\t - IN PROGRESS -')
                                                        #funtion single tiffs to tiff
                                                        tiffS2bnr(values['infilepath'],values['timefilepath'],wavelength,out_file_path)
                                                        window['convinf'].update(value='File conversion info: \nconversion of single-image TIFF files to bnr\n\t - DONE -')
                                                                    
window.close()
