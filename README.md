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
