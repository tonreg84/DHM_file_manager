"""
DHM file manager
 Autor: tonreg, team UMI, CNP-CHUV Lausanne
 
 Version 01 - 28.03.2024

 This program is used to post-process data recorded during one experience with a LynceeTec DHM.

 This program does:
 a) open image files written by LynceeTec Koala, LynceeTec Possum, or FIJI and shows the header information.

 b) convert files between "LynceeTec" formats
    - Supported input file formats:
      - "bin" - a series of binary file, where every file is a single image of a recording.
      - "bnr" - a binary file containing a sequence of images of a recording.
      - "tif" or "tiff" - is a sequence of images in TIFF format of a recording.
      - single "tif" files - a series of file in TIFF format, where every file is a single image of a recording.
    - Supported output file formats:
      - "bin"
      - "bnr"
      - "tif" or "tiff" sequence
      - single "tif" files - a series of file in TIFF format, where every file is a single image of a recording.

 c) modify the header of all bin files of a choosen folder. Click button "Bin-file header mod" to access this function.
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

import numpy
from skimage.transform import resize

import matplotlib.image

from modify_header import modify_header

#some control variables:
infilewithness=None
showheaderwithness=None
outform=None

#info window
with open('info.txt') as f:
    infotext=f.read()
f.close()
#infotext='DHM file manager - version 01 - 15.03.2024\n Autor: Gernot Scheerer, team UMI, CNP-CHUV Lausanne\n gernot.scheerer@hotmail.de\n\n This program is used to post-process data recorded during one experience with a LynceeTec DHM.\n\nThis program does:\n\na) Open images and sequences written by LynceeTec Koala, LynceeTec Possum, or FIJI.\n\nb) convert files between "LynceeTec" formats\n- Supported input file formats:\n-- "bin" - a series of binary file, where every file is a single image of a recording.\n-- "bnr" - a binary file containing a sequence of images of a recording.\n-- "tif" or "tiff" - is a sequence of images in TIFF format of a recording.\n-- single "tif" files - a series of file in TIFF format, where every file is a single image of a recording.\n- Supported output file formats:\n-- "bin"\n-- "bnr"\n-- "tif" or "tiff" sequence\n-- single "tif" files - a series of file in TIFF format, where every file is a single image of a recording.\n\nc) modify the header of all bin files of a choosen folder. Click button \"Bin-file header mod\" to access this function.'

# First the window layout in 3 columns
files_and_parameter = [
    [
        simgui.Text("Input file:"),
        simgui.In(size=(50, 1), enable_events=True, key="infilepath"),
        simgui.FileBrowse(),
    ],
    [
        simgui.Text("Timestamp file:"),
        simgui.In(size=(50, 1), enable_events=True, key="timefilepath"),
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
        simgui.Checkbox("tiff", enable_events=True, key='outformtif'),
        simgui.Checkbox("single tiffs", enable_events=True, key='outformtifS'),
    ],
    [
         simgui.Text("Output file:"),
         simgui.In(size=(50, 1), enable_events=True, key="outfilepath"),
         simgui.FileBrowse(),
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
        simgui.Text("                                                                                 "),
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
        binfolder=simgui.popup_get_folder('Please select a folder with bin files:',  title="Chose bin folder.")
        if binfolder!=None:
            if binfolder=='':
                simgui.popup_auto_close('Error: No folder selected.')
            elif os.path.isdir(binfolder)==False:
                simgui.popup_auto_close('Error: This folder doesn\'t exist.')
            else: 
                modify_header(binfolder)
    #modify header of bin files - END
    
#if tik one box, then set all others to false
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
            #change outfile format if we tick another output format box
            window['convinf'].update(value='File conversion info: slecting input\nIf output format = bin, the output files will be created in a new folder \"outputfilename_Bin_files\"')
            if values['outfilepath'] != "":
                out_file_name, out_file_extension = os.path.splitext(values['outfilepath'])
                if out_file_extension != outform:
                    out_file_path=out_file_name+outform
                    window['outfilepath'].update(value=out_file_path)
        else: outform=None
    if event == 'outformbnr':
        if window['outformbnr'].get() == True:
            window['outformbin'].update(value=False)
            window['outformtif'].update(value=False)
            window['outformtifS'].update(value=False)
            outform='.bnr'
            #change outfile format if we tick another output format box
            if values['outfilepath'] != "":
                out_file_name, out_file_extension = os.path.splitext(values['outfilepath'])
                if out_file_extension != outform:
                    out_file_path=out_file_name+outform
                    window['outfilepath'].update(value=out_file_path)
        else: outform=None
    if event == 'outformtif':
        if window['outformtif'].get() == True:
            window['outformbnr'].update(value=False)
            window['outformbin'].update(value=False)
            window['outformtifS'].update(value=False)
            outform='.tif'
            #change outfile format if we tick another output format box
            if values['outfilepath'] != "":
                out_file_name, out_file_extension = os.path.splitext(values['outfilepath'])
                if out_file_extension != outform:
                    out_file_path=out_file_name+outform
                    window['outfilepath'].update(value=out_file_path)
        else: outform=None
    if event == 'outformtifS':
        if window['outformtifS'].get() == True:
            window['outformbnr'].update(value=False)
            window['outformbin'].update(value=False)
            window['outformtif'].update(value=False)
            outform='.single_tiffs'
            #change outfile format if we tick another output format box
        else: outform=None
                
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
    
    #write output file path into 'outfilepath' if input file and output format are choosen
    if values['infilepath'] != "" and values['outfilepath'] == "" and infilewithness != values['infilepath']:
        in_file_name, in_file_extension = os.path.splitext(values['infilepath'])
        
        if window['outformbin'].get() == True or window['outformbnr'].get() == True or window['outformtif'].get() == True or window['outformtifS'].get() == True:
            out_file_path=in_file_name+outform
            print('New output file name: ', out_file_path)
            window['outfilepath'].update(value=out_file_path)
            infilewithness = values['infilepath']
            
    #start main program = file conversion
    if event == 'startfileconv':
        print('\nStart file conversion\n -> Check input and output parameters:\n')
        
        #check if all files and parameter are choosen correctly
        #first check if input file is selected
        if values['infilepath'] == "": 
            print(' Error: No input file selected')
            new_in_file=simgui.popup_get_file('Please select an input file:',  title="Error: No input file selected.")
            window['infilepath'].update(value=new_in_file)
            print (" Input file selected: ", values['infilepath'])
        else:
            print (" Input file selected: ", values['infilepath'])
            #now we check the input file extension
            file_name, in_file_extension = os.path.splitext(values['infilepath'])
            if in_file_extension != ".bin" and in_file_extension !=".bnr" and in_file_extension !=".tif":
                print("  Error: Wrong input file format")
                new_in_file=simgui.popup_get_file('Please select another input file:',  title="Error: Wrong input file format.")
                window['infilepath'].update(value=new_in_file)
                print('  New input file selected: ', new_in_file)
            else:
                print("  Correct input file format: ", in_file_extension)
                
                #if in_file is tiff, check if its a file of a series of "single tiffs"
                if in_file_extension == '.tif':
                    
                    tiffcheck=simgui.popup_yes_no('You have chosen a tiff file as input.\n\nIs it a tiff-sequence or a file from a\nseries of "single tiffs?\n\n  Sequence  Singles', title='TiffS?')

                    if tiffcheck!=None:
                        if tiffcheck=='No':
                            in_file_extension='.single_tiffs'
                
                #now check if timestamp file is choosen
                if values['timefilepath'] == "": 
                    print('   Error: No timestamp file selected')
                    new_in_file=simgui.popup_get_file('Please select a timestamp file:',  title="Error: No timestamp file selected.")
                    window['timefilepath'].update(value=new_in_file)
                    print("   Timestamp file selected: ", new_in_file)
                else:
                    print("   Timestamp file selected: ", values['timefilepath'])
                    #now check if wavelength is selected
                    if window['682'].get() == False and window['666'].get() == False:
                        simgui.popup_auto_close('Error: No wavelength selected.')
                    else:
                        #nowcheck  if output format selected
                        if window['outformbin'].get() == False and window['outformbnr'].get() == False and window['outformtif'].get() == False and window['outformtifS'].get() == False:
                            simgui.popup_auto_close('Error: No output file format selected.')
                        else:
                            #now check if output file is selected
                            if values['outfilepath'] == "": 
                                print('    Error: No output file selected')
                                new_out_file=simgui.popup_get_file('Please select an output file:',  title="Error: No output file selected.")
                                window['outfilepath'].update(value=new_out_file)
                                print ("    Output file selected: ", new_out_file)
                            else:
                                print ("    Output file selected: ", values['outfilepath'])
                                #get output format and check if output and input format are different                                
                                if window['outformbin'].get() == True:
                                    outform='.bin'
                                elif window['outformbnr'].get() == True:
                                    outform='.bnr'
                                elif window['outformtif'].get() == True:
                                    outform='.tif'
                                elif window['outformtifS'].get() == True:
                                    outform='.single_tiffs'
                                if in_file_extension == outform:
                                    print('     Error: Same input and output format')
                                    simgui.popup_auto_close('Error: Identic input and output format. Please chose another output format!')
                                else:
                                    if in_file_extension=='.bin' and outform=='.bnr':
                                        print('bin to bnr')
                                        window['convinf'].update(value='File conversion info: \nconversion bin to bnr\n\t - IN PROGRESS -')
                                        #funtion bin to bnr:
                                        bin2bnr(values['infilepath'],values['timefilepath'],wavelength,values['outfilepath'])
                                        window['convinf'].update(value='File conversion info: \nconversion bin to bnr\n\t - DONE -')
                                    
                                    elif in_file_extension=='.bin' and outform=='.tif':
                                        print('bin to tif')
                                        window['convinf'].update(value='File conversion info: \nconversion bin to tif\n\t - IN PROGRESS -')
                                        #funtion bin to tif:
                                        bin2tif(values['infilepath'],values['timefilepath'],wavelength,values['outfilepath'])
                                        window['convinf'].update(value='File conversion info: \nconversion bin to tif\n\t - DONE -')
                                    
                                    elif in_file_extension=='.bnr' and outform=='.tif':
                                        print('bnr to tif')
                                        window['convinf'].update(value='File conversion info: \nconversion bnr to tif\n\t - IN PROGRESS -')
                                        #funtion bnr to tif
                                        bnr2tif(values['infilepath'],values['timefilepath'],wavelength,values['outfilepath'])
                                        window['convinf'].update(value='File conversion info: \nconversion bnr to tif\n\t - DONE -')
                                    
                                    elif in_file_extension=='.bnr' and outform=='.bin':
                                        print('bnr to bin')
                                        window['convinf'].update(value='File conversion info: \nconversion bnr to bin\n\t - IN PROGRESS -')
                                        #funtion bnr to bin
                                        bnr2bin(values['infilepath'],values['timefilepath'],wavelength,values['outfilepath'])
                                        window['convinf'].update(value='File conversion info: \nconversion bnr to bin\n\t - DONE -')
                                   
                                    elif in_file_extension=='.tif' and outform=='.bin':
                                        print('tif to bin')
                                        window['convinf'].update(value='File conversion info: \nconversion tif to bin\n\t - IN PROGRESS -')
                                        #funtion tif to bin
                                        tif2bin(values['infilepath'],values['timefilepath'],wavelength,values['outfilepath'])
                                        window['convinf'].update(value='File conversion info: \nconversion tif to bin\n\t - DONE -')
                                    
                                    elif in_file_extension=='.tif' and outform=='.bnr':
                                        print('tif to bnr')
                                        window['convinf'].update(value='File conversion info: \nconversion tif to bnr\n\t - IN PROGRESS -')
                                        #funtion tif to bnr
                                        tif2bnr(values['infilepath'],values['timefilepath'],wavelength,values['outfilepath'])
                                        window['convinf'].update(value='File conversion info: \nconversion tif to bnr\n\t - DONE -')
                                        
                                    elif in_file_extension=='.tif' and outform=='.single_tiffs':
                                        print('tif to single tiffs')
                                        window['convinf'].update(value='File conversion info: \nconversion tif to single tiffs\n\t - IN PROGRESS -')
                                        #funtion tif to single tiffs
                                        tif2tiffS(values['infilepath'],values['timefilepath'],wavelength,values['outfilepath'])
                                        window['convinf'].update(value='File conversion info: \nconversion tif to single tiffs\n\t - DONE -')
                                        
                                    elif in_file_extension=='.bin' and outform=='.single_tiffs':
                                        print('bin to single tiffs')
                                        window['convinf'].update(value='File conversion info: \nconversion bin files to single tiffs\n\t - IN PROGRESS -')
                                        #funtion bin to single tiffs
                                        bin2tiffS(values['infilepath'],values['timefilepath'],wavelength,values['outfilepath'])
                                        window['convinf'].update(value='File conversion info: \nconversion bin files to single tiffs\n\t - DONE -')
                                
                                    elif in_file_extension=='.bnr' and outform=='.single_tiffs':
                                        print('bnr to single tiffs')
                                        window['convinf'].update(value='File conversion info: \nconversion bnr file to single tiffs\n\t - IN PROGRESS -')
                                        #funtion bnr to single tiffs
                                        bnr2tiffS(values['infilepath'],values['timefilepath'],wavelength,values['outfilepath'])
                                        window['convinf'].update(value='File conversion info: \nconversion bnr file to single tiffs\n\t - DONE -')
                                        
                                    elif in_file_extension=='.single_tiffs' and outform=='.tif':
                                        print('single tiffs to tiff')
                                        window['convinf'].update(value='File conversion info: \nconversion single tiffs to tiff\n\t - IN PROGRESS -')
                                        #funtion single tiffs to tiff
                                        tiffS2tiff(values['infilepath'],values['timefilepath'],wavelength,values['outfilepath'])
                                        window['convinf'].update(value='File conversion info: \nconversion single tiffs to tiff\n\t - DONE -')
                             
                                    elif in_file_extension=='.single_tiffs' and outform=='.bin':
                                        print('single tiffs to  bin')
                                        window['convinf'].update(value='File conversion info: \nconversion single tiffs to bin\n\t - IN PROGRESS -')
                                        #funtion single tiffs to tiff
                                        tiffS2bin(values['infilepath'],values['timefilepath'],wavelength,values['outfilepath'])
                                        window['convinf'].update(value='File conversion info: \nconversion single tiffs to bin\n\t - DONE -')

                                    elif in_file_extension=='.single_tiffs' and outform=='.bnr':
                                        print('single tiffs to  bnr')
                                        window['convinf'].update(value='File conversion info: \nconversion single tiffs to bnr\n\t - IN PROGRESS -')
                                        #funtion single tiffs to tiff
                                        tiffS2bnr(values['infilepath'],values['timefilepath'],wavelength,values['outfilepath'])
                                        window['convinf'].update(value='File conversion info: \nconversion single tiffs to bnr\n\t - DONE -')






window.close()
