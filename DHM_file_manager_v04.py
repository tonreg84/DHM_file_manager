"""
DHM file manager
Autor: tonreg, team UMI, CNP-CHUV Lausanne
 
Version 04 - 27.05.2024

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

import os.path
import binkoala
from tifffile import imread
import numpy

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

from modify_header import modify_bin_header
from modify_header import modify_bnr_header

#initialize some variables and controls
convinf=''
outform=None
wavelength=None
in_file_path=''
timestamps_file=''
out_folder=''
out_file_name=''
out_file_path=''
infilewithness=None

#TKinter prep
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

#some functions called by the buttons
def exitprog(root):
    root.destroy()
    
#info window
with open('info.txt') as f:
    infotext=f.read()
f.close()
def show_info():
    with open('info.txt') as f:
        infotext=f.read()
    f.close()
    tk.messagebox.showinfo("Info", infotext)

def display_array_as_image(float_array):
    # Normalize the float array to range [0, 1]
    normalized_array = (float_array - float_array.min()) / (float_array.max() - float_array.min())
    # Create a viridis colormap
    cmap = plt.get_cmap('viridis')
    # Apply the colormap to the normalized array
    cmap_array = cmap(normalized_array)
    # Convert the matplotlib array to a PIL image
    image = Image.fromarray((cmap_array[:, :, :3] * 255).astype(numpy.uint8))
    image = image.resize((300, 300))
    # Convert PIL image to Tkinter-compatible format
    photo = ImageTk.PhotoImage(image)
    # Update the image label
    image_label.config(image=photo)
    image_label.image = photo  # Keep a reference to the image to prevent it from being garbage collected

def get_in_file():
    global out_file_name
    global in_file_path
    out_file_name=out_name_entry.get()
    #from display_file_info import display_file_info
    in_file_path = filedialog.askopenfilename(parent=root, title="Select a DHM image or sequence file")
    print('Input file selected:',in_file_path)
    #display_file_info(in_file_path)
    #display input file info and image
    if in_file_path != "" and in_file_path !=None:
        in_file_name, in_file_extension = os.path.splitext(in_file_path)
        if in_file_extension == ".bin":
                    
            #get header info:
            (in_file_image,in_file_header)=binkoala.read_mat_bin(in_file_path)
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
        
            in_file_info='File name: '+os.path.basename(in_file_path)+'\n\n'+'Header version: '+hv+'\n'+'Endianess: '+end+'\n'+'Header size: '+end+'\n'+'Width: '+w+'\n'+'Heigth: '+w+'\n'+'Pixel size [m]: '+pz+'\n'+'Height coversion factor [m]: '+hconv+'\n'+'Unit code: '+uc+' (1=rad, 2=m, 0=no unit)'+'\n\nMin: '+phasemin+'\nMax: '+phasemax+'\nMean: '+phaseavg+'\n'    
            headerdisplay.delete(1.0, tk.END)
            headerdisplay.insert(1.0,in_file_info)
            print('In-File-Info:\n'+in_file_info)
            
            #display image
            display_array_as_image(in_file_image)

        if in_file_extension == ".bnr":
            
            #get header info:
            fileID = open(in_file_path, 'rb')
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
            
            in_file_info='File name: '+os.path.basename(in_file_path)+'\n\n'+'Sequence length: '+str(nImages)+'\n'+'Width: '+str(w)+'\n'+'Heigth: '+str(h)+'\n'+'Pixel size [m]: '+pz+'\n'+'Wavelength [nm]: '+waveshow+'\n'+'Refraction index 1: '+n_1+'\n'+'Refraction index 2: '+n_2+'\n\nMin: '+phasemin+'\nMax: '+phasemax+'\nMean: '+phaseavg+'\n'
            headerdisplay.delete(1.0, tk.END)
            headerdisplay.insert(1.0,in_file_info)
            print('In-File-Info:\n',in_file_info)
            
            #display image
            display_array_as_image(phase_map)
            
        if in_file_extension == ".tif":
            phase_map = imread(in_file_path, key=0)
            w = str(len(phase_map[0,:]))
            h = str(len(phase_map[:,0]))
            phasemin=str(phase_map.min())
            phasemax=str(phase_map.max())
            phaseavg=str(numpy.mean(phase_map))
            in_file_info='File name: '+os.path.basename(in_file_path)+'\n\n'+'Width: '+str(w)+'\n'+'Heigth: '+str(h)+'\n\nAttention: When converting from tiff to another format, the pixel values might needed to be devided by hconv!\n\nMin: '+phasemin+'\nMax: '+phasemax+'\nMean: '+phaseavg
            headerdisplay.delete(1.0, tk.END)
            headerdisplay.insert(1.0,in_file_info)
            print('In-File-Info:\n',in_file_info)
            
            #display image
            display_array_as_image(phase_map)
            
        #suggest output filename 
        if out_file_name == '':
            if outform == '.bnr' or outform == '.tif':
                alist=os.path.basename(in_file_path).split('.')
                if len(alist) == 1:
                    out_file_name=os.path.basename(in_file_path)+outform
                else:
                    namebase=''
                    for k in range(len(alist)-2):
                        namebase=namebase+alist[k]+'.'
                    namebase=namebase+alist[len(alist)-2]    
                    out_file_name=namebase+outform
                out_name_entry.delete(0,tk.END)
                out_name_entry.insert(0,out_file_name)
def get_timestamps_file():
    global timestamps_file
    timestamps_file = filedialog.askopenfilename(parent=root, title="Select a timestamps file")
    print('Timestamps file selected:',timestamps_file)
def check_w(w):
    global wavelength
    #if tik one w box, set the other to false, set wavelength variable
    if w=='682':
        if v682.get() == True:
            v666.set(False)
            wavelength=682.5
        else: wavelength=None
    if w=='666':
        if v666.get() == True:
            v682.set(False)
            wavelength=666
        else: wavelength=None
def check_format(formstring):
    global out_file_name
    global outform
    out_file_name=out_name_entry.get()
    #if tik one format box, set all others to false, suggest output file name, set outform variable
    #change outfile format if we tick another output format box
    if formstring=='bin':
        if vbin.get()==True:
            vbnr.set(False)
            vtifstack.set(False)
            vsingletif.set(False)
            outform='.bin'
            out_name_entry.config(state= "normal")
            out_file_name='00000_phase.bin'
            out_name_entry.delete(0,tk.END)
            out_name_entry.insert(0,out_file_name)
            out_name_entry.config(state= "disabled")
            convinf='File conversion info: selecting input\nOutput format = single-image bin files\nA new folder will be created to save the bin files.'
            convinf_text.config(text=convinf)
        else:
            outform=None
            out_name_entry.config(state= "normal")
            
    if formstring=='bnr':
        if vbnr.get()==True:
            vbin.set(False)
            vtifstack.set(False)
            vsingletif.set(False)
            outform='.bnr'
            
            out_name_entry.config(state= "normal")
            convinf='File conversion info: selecting input\nOutput format = bnr (bin stack).'
            convinf_text.config(text=convinf)
            #change outfile format
            if out_file_name != '':
                alist=out_file_name.split('.')
                if len(alist) == 1:
                    out_file_name=out_file_name+outform
                else:
                    namebase=''
                    for k in range(len(alist)-2):
                        namebase=namebase+alist[k]+'.'
                    namebase=namebase+alist[len(alist)-2]
                    out_file_name=namebase+outform
                out_name_entry.delete(0,tk.END)
                out_name_entry.insert(0,out_file_name)
            else:
                #suggest output filename 
                if in_file_path != '':
                    alist=os.path.basename(in_file_path).split('.')
                    if len(alist) == 1:
                        out_file_name=out_file_name+outform
                    else:
                        namebase=''
                        for k in range(len(alist)-2):
                            namebase=namebase+alist[k]+'.'
                        namebase=namebase+alist[len(alist)-2]    
                        out_file_name=namebase+outform
                    out_name_entry.delete(0,tk.END)
                    out_name_entry.insert(0,out_file_name)
                
        else:
            outform=None
                
    if formstring=='tifstack':
        if vtifstack.get()==True:
            vbin.set(False)
            vbnr.set(False)
            vsingletif.set(False)
            outform='.tif'
            
            out_name_entry.config(state= "normal")
            convinf='File conversion info: selecting input\nOutput format = tiff stack.'
            convinf_text.config(text=convinf)
            #change outfile format
            if out_file_name != '':
                alist=out_file_name.split('.')
                
                if len(alist) == 1:
                    out_file_name=out_file_name+outform
                else:
                    namebase=''
                    for k in range(len(alist)-2):
                        namebase=namebase+alist[k]+'.'
                    namebase=namebase+alist[len(alist)-2]
                    out_file_name=namebase+outform
                out_name_entry.delete(0,tk.END)
                out_name_entry.insert(0,out_file_name)
            else:
                #suggest output filename 
                if in_file_path != '':
                    alist=os.path.basename(in_file_path).split('.')
                    if len(alist) == 1:
                        out_file_name=out_file_name+outform
                    else:
                        namebase=''
                        for k in range(len(alist)-2):
                            namebase=namebase+alist[k]+'.'
                        namebase=namebase+alist[len(alist)-2]    
                        out_file_name=namebase+outform
                    out_name_entry.delete(0,tk.END)
                    out_name_entry.insert(0,out_file_name)
        else:
            outform=None
    if formstring=='singletif':
        if vsingletif.get()==True:
            vbnr.set(False)
            vtifstack.set(False)
            vbin.set(False)
            outform='.singletif'
            out_name_entry.config(state= "normal")
            out_file_name='00000_phase.tif'
            out_name_entry.delete(0,tk.END)
            out_name_entry.insert(0,out_file_name)
            out_name_entry.config(state= "disabled")
            convinf='File conversion info: selecting input\nOutput format = single-image tiff files\nA new folder will be created to save the tiff files.'
            convinf_text.config(text=convinf)
        else:
            outform=None
            out_name_entry.config(state= "normal")
def save_out_folder():
    global out_folder
    out_folder=tk.filedialog.askdirectory(parent=root, title="Select the output folder")
    if out_folder != '' and out_folder != None:
        out_folder_entry.delete(0,tk.END)
        out_folder_entry.insert(0,out_folder)
def set_folder():
    global out_folder
    if in_file_path != ''and in_file_path != None:
        out_folder = os.path.dirname(in_file_path)
        out_folder_entry.delete(0,tk.END)
        out_folder_entry.insert(0,out_folder)
def start_file_conversion():
    global in_file_path
    global timestamps_file
    #start main program = file conversion
    #check if all files and parameter are choosen correctly
    print('\nStart file conversion\n -> Check input and output parameters:\n')
    #first check if input file is selected
    if in_file_path == "":
        print('Error: No input file selected')
        #in_file_path = filedialog.askopenfilename(parent=root, title="Error: No input file selected. Please select a DHM image or sequence file.")
        get_in_file()
        print (" Input file selected: ", in_file_path)
    else:
        #now we check the input file extension
        file_name, in_file_extension = os.path.splitext(in_file_path)
        if in_file_extension != ".bin" and in_file_extension !=".bnr" and in_file_extension !=".tif":
            print("Error: Wrong input file format")
            in_file_path = filedialog.askopenfilename(parent=root, title="Error: Wrong input file format. Please select a \".bin\", \".bnr\", or \".tif\" file.")
        else:
            print("Correct input file format: ", in_file_extension)
            #if input file is tiff, ask user if its a tiff stack file or a series of single-image tiff files
            tiff_go_on = False
            if in_file_extension == '.tif':
                from tiffs_or_tiffS import tiffs_or_tiffS
                (go_on,tiff_type)=tiffs_or_tiffS(root)
                print(go_on,tiff_type)
                if go_on == True:
                    tiff_go_on = True
                    in_file_extension=tiff_type
            else: tiff_go_on = True
            if tiff_go_on == True:
                #now check if timestamps file is choosen
                if timestamps_file == '':
                    print('Error: No timestamps file selected')
                    get_timestamps_file()
                else:
                    print("Timestamp file selected:", timestamps_file)
                    #now check if wavelength is selected
                    if v682.get() == False and v666.get() == False:
                        tk.messagebox.showinfo('Error', 'No wavelength selected.')
                    else:
                        #nowcheck if output format selected
                        if vbin.get() == False and vbnr.get() == False and vtifstack.get() == False and vsingletif.get() == False:
                            tk.messagebox.showinfo('Error', 'No output file format selected.')
                        else:
                            #now check output file path
                            if out_folder_entry.get() == '':
                                print('Error: No output folder selected')
                                tk.messagebox.showinfo('Error', 'No output folder selected.')
                            else:
                                if os.path.isdir(out_folder_entry.get()) == False:
                                    tk.messagebox.showinfo('Error', 'The selected output folder does not exist.')
                                else:
                                    if out_name_entry.get() == '':
                                        print('Error: No output file name selected')
                                        tk.messagebox.showinfo('Error', 'Please enter a file name.')
                                    else:
                                        out_file_path=out_folder_entry.get()+'/'+out_name_entry.get()
                                        #now checkt if in- and output formats are different
                                        if in_file_extension == outform:
                                            print('Error: Same input and output format')
                                            tk.messagebox.showinfo('Error', 'Identic input and output format!')
                                        else:
                                            #now checkt if output file exists already (for bnr and tiff sequence file)
                                            checkit=False
                                            if outform == '.bnr' or outform == '.tif':
                                                if os.path.isfile(out_file_path)==True:
                                                    print('/!\\ Output file exits already!')
                                                    result = tk.messagebox.askquestion('Output file exits already!', 'Do you want to overwrite?')
                                                    if result == 'yes':
                                                        checkit=True
                                                    else:
                                                        checkit=False
                                                else:
                                                    checkit=True
                                            else:
                                                checkit=True
    
                                            if checkit == True:
                                                print('All input and output parameters verified. Start conversion.')
                                            
                                                if in_file_extension=='.bin' and outform=='.bnr':
                                                    print('bin to bnr')
                                                    convinf_text.config(text='File conversion info: \nconversion of bin to bnr\n\t - IN PROGRESS -')
                                                    #funtion bin to bnr:
                                                    bin2bnr(in_file_path,timestamps_file,wavelength,out_file_path,root)
                                                    convinf_text.config(text='File conversion info: \nconversion of bin to bnr\n\t - DONE -')
                                                
                                                elif in_file_extension=='.bin' and outform=='.tif':
                                                    print('bin to tif')
                                                    convinf_text.config(text='File conversion info: \nconversion of bin to TIFF stack\n\t - IN PROGRESS -')
                                                    #funtion bin to tif:
                                                    bin2tif(in_file_path,timestamps_file,wavelength,out_file_path,root)
                                                    convinf_text.config(text='File conversion info: \nconversion of bin to TIFF stack\n\t - DONE -')
                                                
                                                elif in_file_extension=='.bnr' and outform=='.tif':
                                                    print('bnr to tif')
                                                    convinf_text.config(text='File conversion info: \nconversion of bnr to TIFF stack\n\t - IN PROGRESS -')
                                                    #funtion bnr to tif
                                                    bnr2tif(in_file_path,timestamps_file,wavelength,out_file_path,root)
                                                    convinf_text.config(text='File conversion info: \nconversion of bnr to TIFF stack\n\t - DONE -')
                                                
                                                elif in_file_extension=='.bnr' and outform=='.bin':
                                                    print('bnr to bin')
                                                    convinf_text.config(text='File conversion info: \nconversion of bnr to bin\n\t - IN PROGRESS -')
                                                    #funtion bnr to bin
                                                    bnr2bin(in_file_path,timestamps_file,wavelength,out_folder_entry.get(),root)
                                                    convinf_text.config(text='File conversion info: \nconversion of bnr to bin\n\t - DONE -')
                                               
                                                elif in_file_extension=='.tif' and outform=='.bin':
                                                    print('tif to bin')
                                                    convinf_text.config(text='File conversion info: \nconversion of TIFF stack to bin\n\t - IN PROGRESS -')
                                                    #funtion tif to bin
                                                    tif2bin(in_file_path,timestamps_file,wavelength,out_folder_entry.get(),root)
                                                    convinf_text.config(text='File conversion info: \nconversion of TIFF stack to bin\n\t - DONE -')
                                                
                                                elif in_file_extension=='.tif' and outform=='.bnr':
                                                    print('tif to bnr')
                                                    convinf_text.config(text='File conversion info: \nconversion of TIFF stack to bnr\n\t - IN PROGRESS -')
                                                    #funtion tif to bnr
                                                    tif2bnr(in_file_path,timestamps_file,wavelength,out_file_path,root)
                                                    convinf_text.config(text='File conversion info: \nconversion of TIFF stack to bnr\n\t - DONE -')
                                                    
                                                elif in_file_extension=='.tif' and outform=='.singletif':
                                                    print('tif to single tiffs')
                                                    convinf_text.config(text='File conversion info: \nconversion of TIFF stack to single-image TIFF files\n\t - IN PROGRESS -')
                                                    #funtion tif to single tiffs
                                                    tif2tiffS(in_file_path,timestamps_file,wavelength,out_folder_entry.get(),root)
                                                    convinf_text.config(text='File conversion info: \nconversion of TIFF stack to single-image TIFF files\n\t - DONE -')
                                                    
                                                elif in_file_extension=='.bin' and outform=='.singletif':
                                                    print('bin to single tiffs')
                                                    convinf_text.config(text='File conversion info: \nconversion of bin files to single-image TIFF files\n\t - IN PROGRESS -')
                                                    #funtion bin to single tiffs
                                                    bin2tiffS(in_file_path,timestamps_file,wavelength,out_folder_entry.get(),root)
                                                    convinf_text.config(text='File conversion info: \nconversion of bin files to single-image TIFF files\n\t - DONE -')
                                            
                                                elif in_file_extension=='.bnr' and outform=='.singletif':
                                                    print('bnr to single tiffs')
                                                    convinf_text.config(text='File conversion info: \nconversion of bnr file to ssingle-image TIFF files\n\t - IN PROGRESS -')
                                                    #funtion bnr to single tiffs
                                                    bnr2tiffS(in_file_path,timestamps_file,wavelength,out_folder_entry.get(),root)
                                                    convinf_text.config(text='File conversion info: \nconversion of bnr file to single-image TIFF files\n\t - DONE -')
                                                    
                                                elif in_file_extension=='.singletif' and outform=='.tif':
                                                    print('single tiffs to tiff')
                                                    convinf_text.config(text='File conversion info: \nconversion of single-image TIFF files to TIFF stack\n\t - IN PROGRESS -')
                                                    #funtion single tiffs to tiff
                                                    tiffS2tiff(in_file_path,timestamps_file,wavelength,out_file_path,root)
                                                    convinf_text.config(text='File conversion info: \nconversion of single-image TIFF files to TIFF stack\n\t - DONE -')
                                         
                                                elif in_file_extension=='.singletif' and outform=='.bin':
                                                    print('single tiffs to  bin')
                                                    convinf_text.config(text='File conversion info: \nconversion of single-image TIFF files to bin\n\t - IN PROGRESS -')
                                                    #funtion single tiffs to tiff
                                                    tiffS2bin(in_file_path,timestamps_file,wavelength,out_folder_entry.get(),root)
                                                    convinf_text.config(text='File conversion info: \nconversion of single-image TIFF files to bin\n\t - DONE -')
            
                                                elif in_file_extension=='.singletif' and outform=='.bnr':
                                                    print('single tiffs to  bnr')
                                                    convinf_text.config(text='File conversion info: \nconversion of single-image TIFF files to bnr\n\t - IN PROGRESS -')
                                                    #funtion single tiffs to tiff
                                                    tiffS2bnr(in_file_path,timestamps_file,wavelength,out_file_path,root)
                                                    convinf_text.config(text='File conversion info: \nconversion of single-image TIFF files to bnr\n\t - DONE -')

##############################################################################
###
###   Main window layout
###
##############################################################################

#create main window
root = tk.Tk()
root.title("DHM file manager")

info_button = tk.Button(root, text="Information", width=10, height=1, command=lambda: show_info())

#####################################################################
 # Frame to chose input files, output location and some parameters
FP_frame = tk.LabelFrame(root, text="Files and parameters")

load_file_button = tk.Button(FP_frame, text="Load DHM image or sequence", width=25, height=1, command=lambda: get_in_file())

load_timestamps_button = tk.Button(FP_frame, text="Load timestamps file", width=25, height=1, command=lambda: get_timestamps_file())

w_label = tk.Label(FP_frame, text= "Laser wavelength in nm:")
v682=tk.BooleanVar()
checkbutton_682= tk.Checkbutton(FP_frame, text="682.5", variable=v682, command=lambda: check_w('682'))
v666=tk.BooleanVar()
checkbutton_666 = tk.Checkbutton(FP_frame, text="666", variable=v666, command=lambda: check_w('666'))

format_label = tk.Label(FP_frame, text= "Output format:")
vbin=tk.BooleanVar()
vbnr=tk.BooleanVar()
vtifstack=tk.BooleanVar()
vsingletif=tk.BooleanVar()
bin_checkbutton = tk.Checkbutton(FP_frame, text="bin", variable=vbin, command=lambda: check_format('bin'))
bnr_checkbutton = tk.Checkbutton(FP_frame, text="bnr", variable=vbnr, command=lambda: check_format('bnr'))
tifstack_checkbutton = tk.Checkbutton(FP_frame, text="tiff stack", variable=vtifstack, command=lambda: check_format('tifstack'))
singletif_checkbutton = tk.Checkbutton(FP_frame, text="single-image tiff files", variable=vsingletif, command=lambda: check_format('singletif'))

out_name_label = tk.Label(FP_frame, text= "Output file name:")
out_name_entry = tk.Entry(FP_frame)
out_folder_label = tk.Label(FP_frame, text= "Output file folder:")
out_folder_entry = tk.Entry(FP_frame)
select_folder_button = tk.Button(FP_frame, text="Browse", width=8, height=1, command=lambda: save_out_folder())
set_folder_button = tk.Button(FP_frame, text="Same as input file", width=16, height=1, command=lambda: set_folder())

load_file_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")
load_timestamps_button.grid(row=1, column=0, padx=5, pady=5, sticky="w")

w_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
checkbutton_682.grid(row=2, column=1, padx=5, pady=5, sticky="w")
checkbutton_666.grid(row=2, column=2, padx=5, pady=5, sticky="w")

format_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
bin_checkbutton.grid(row=3, column=1, padx=5, pady=5, sticky="w")
bnr_checkbutton.grid(row=3, column=2, padx=5, pady=5, sticky="w")
tifstack_checkbutton.grid(row=3, column=3, padx=5, pady=5, sticky="w")
singletif_checkbutton.grid(row=3, column=4, padx=5, pady=5, sticky="w")

out_folder_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
out_folder_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")
select_folder_button.grid(row=4, column=2, padx=5, pady=5, sticky="w")
set_folder_button.grid(row=4, column=3, padx=5, pady=5, sticky="w")

out_name_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")
out_name_entry.grid(row=5, column=1, padx=5, pady=5, sticky="w")

##############################
# Conversion frame
conv_frame = tk.LabelFrame(root)
start_button = tk.Button(conv_frame, text="Start file conversion!", width=17, height=1, command=lambda: start_file_conversion())
# display state of file conversion
convinf_text=tk.Label(conv_frame, height = 3, width = 50, background='white')
convinf_text.config(text="File conversion info: slecting input")

start_button.grid(row=0, column=0, padx=5, pady=5, sticky="n,w")
convinf_text.grid(row=0, column=1, padx=5, pady=5, sticky="n,w")

#############################
#buttons to start header modification procedure
bin_head_mod = tk.Button(root, text="Modify the header of a bin-sequence", width=30, height=1, command=lambda: modify_bin_header(root))
bnr_head_mod = tk.Button(root, text="Modify the header of a bnr-sequence", width=30, height=1, command=lambda: modify_bnr_header(root))

##############################
# header display frame
header_frame = tk.LabelFrame(root, text="Input file info:")
headerdisplay=tk.Text(header_frame, height = 16, width = 30)
headerdisplay.pack(side="left", padx=5, pady=5)
headerdisplay.insert(tk.END, "No input file selected.")

##############################
#####
##### image display frame
#####
##############################
display_frame = tk.LabelFrame(root, text="Input file image:")
# Create a label for displaying the image
default_image = Image.new("RGB", (300, 300), "grey")  # Create a white square image
default_photo = ImageTk.PhotoImage(default_image)
image_label = tk.Label(display_frame, image=default_photo)
image_label.grid(row=0, column=0, padx=5, pady=5, sticky="n,w")

##############################
#window layout
info_button.grid(row=0, column=0, padx=5, pady=5, sticky='n,w')
FP_frame.grid(row=1, column=0, padx=5, pady=5, sticky='n,w')
conv_frame.grid(row=2, column=0, padx=5, pady=5, sticky='n,w')
bin_head_mod.grid(row=3, column=0, padx=5, pady=5, sticky='n,w')
bnr_head_mod.grid(row=3, column=1, padx=5, pady=5, sticky='n,w')
header_frame.grid(row=1, column=1, padx=5, pady=5, sticky='n,w')
display_frame.grid(row=1, column=2, padx=5, pady=5, sticky='n,w')

#Exit button
exit_button = tk.Button(root, text="EXIT", width=10, height=1, command=lambda: exitprog(root))
exit_button.grid(row=3, column=2, padx=5, pady=5, sticky='n,e')
###########################################

root.mainloop()

###########################################
