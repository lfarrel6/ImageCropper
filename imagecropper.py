# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from PIL import Image
import sys
import os
import getopt

def main():
    cmd_args = sys.argv[1:]
    folder = False
    target = ""
    dimensions = (1,3)
    try:
        opts, args = getopt.getopt(cmd_args, "hf:d:", ["help","folder=","dimensions="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt , arg in opts:
        if opt in ("-h","--help"):
            usage()
            sys.exit(2)
        elif opt in ("-f","--folder"):
            folder = True
            target = arg
        elif opt in ("-d","--dimensions"):
            [height,width] = arg.replace("(","").replace(")","").split(",")
            dimensions=(int(height),int(width))
    if folder == False:
        target = "".join(args)
        print("file: ",target)
        splitImage(target,dimensions)
    else:
        print("folder: ",target)
        folderHandler(target,dimensions)        

def usage():
    print("********USAGE NOTES********")
    print("-f or --folder <directory>: specify the folder of files to process")
    print("-d or --dimenstions <(rows,columns)>: specify the grid of squares to create (default is (1,3))")

def splitImage(file,dim):
    print("Will split", file)
    splitF = file.split("\\")
    fileNameWType = splitF[len(splitF)-1]
    [fileName,_type] = fileNameWType.split(".")
    im = Image.open(file)
    (width,height)=im.size
    (nRows,nCols)=dim
    boxWidth=width/nCols
    boxHeight=height/nRows
    """
    Initial implementation takes 3 boxes across
    """
    nRowsComplete = 0
    while nRowsComplete < nRows:
        nColsComplete = 0
        x1 = 0
        y1 = 0+(nRowsComplete*boxHeight)
        x2 = boxWidth
        y2 = boxHeight+(nRowsComplete*boxHeight)
        while nColsComplete < nCols:
            nColsComplete+=1
            newCrop = im.crop((x1,y1,x2,y2))
            newCrop.save(fileName+"Crop"+str(nRowsComplete)+""+str(nColsComplete)+"."+_type)
            x1+=boxWidth
            x2+=boxWidth
        nRowsComplete+=1
    print(fileName,"cropped")
    

def folderHandler(folder,dim):
    print("Will split all images in",folder)
    os.chdir(folder)
    files = os.listdir()
    for file in files:
        split_name = file.split(".")
        file_type = split_name[len(split_name)-1]
        if isImage(file_type):
            splitImage(file,dim)
    print("All images found in",folder,"have been cropped")
    
def isImage(file_type):
    file_type=file_type.lower()
    if (file_type == "jpg") | (file_type == "png") | (file_type == "gif" ):
        return True
    return False
    
if __name__ == "__main__":
    main()
