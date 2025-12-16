DHM file manager
Autor: Gernot Scheerer, team UMI, CNP-CHUV Lausanne
gernot.scheerer@hotmail.de
 
Version 05 - update 16.12.2025

This program is used to post-process images recorded during one experience with a LynceeTec DHM.

This program does:
a) Open "bin" and "bnr" image files written by LynceeTec Koala or LynceeTec Possum, as well as TIFF files;
   Shows the header information for "bin" and "bnr" files.

b) Convert files between different formats
   - Supported input file formats:
     - "bin" - a series of binary file, where every file is a single image from a LynceeTec DHM recording.
     - "bnr" - a binary file containing a sequence of images from a LynceeTec DHM recording.
     - "tiff stack" - a TIFF file containing a sequence of images.
     - "single-image tiff files" - a series of TIFF files, where every file is a single image.
   - Supported output file formats:
     - "bin"
     - "bnr"
     - "tiff stack"
     - "single-image tiff files"
     
c) Modify the header of all bin files of a choosen folder. Click button "Bin-file header mod" to access this function.

d) Modify the header of a bnr file. Click button "Bnr-file header mod" to access this function. 
