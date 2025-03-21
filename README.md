DHM file manager
Autor: tonreg, team UMI, CNP-CHUV Lausanne
 
Version 05 - 14.03.2025

This program is used to post-process data recorded during one experience with a LynceeTec DHM.

This program does:
a) open "bin" and "bnr" image files written by LynceeTec Koala or LynceeTec Possum, as well as TIFF files, and shows the header information for "bin" and "bnr" files.

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
