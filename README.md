DHM file manager
 Autor: tonreg, team UMI, CNP-CHUV Lausanne
 
 Version 02 - 22.04.2024

 This program is used to post-process data recorded during one experience with a LynceeTec DHM.

 This program does:
 a) open image files written by LynceeTec Koala, LynceeTec Possum, or FIJI and shows the header information.

 b) convert files between "LynceeTec" formats
    - Supported input file formats:
      - "bin" - a series of binary file, where every file is a single image of a recording.
      - "bnr" - a binary file containing a sequence of images of a recording.
      - "tiff stack" - a TIFF stack containing a sequence of images of a recording.
      - "single-image tiff files" - a series of files in TIFF format, where every file is a single image of a recording.
    - Supported output file formats:
      - "bin"
      - "bnr"
      - "tiff stack"
      - "single tiff files"

 c) modify the header of all bin files of a choosen folder. Click button "Bin-file header mod" to access this function.
