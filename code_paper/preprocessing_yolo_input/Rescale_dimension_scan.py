import os
import sys
import scipy

Current_directory = os.getcwd()
Main_folder = "/".join(Current_directory.split("/")[0:-2])  # Linux
sys.path.append(Main_folder)
from CODE_Unet.General_Functions_Preprocessing.Loading_and_saving_data import Data_processing
from Packages_file import *
Functions=Data_processing()

def Rescale_scan(Data,Header,Save_dir=None,Filename=None,label=False):

    Dimensions=Header["pixdim"]
    X_dim=Dimensions[1]
    Y_dim=Dimensions[2]
    Z_dim=Dimensions[3]
    if label:
        Data=Data.astype(int)
        Rescaled_scan = scipy.ndimage.zoom(Data, (X_dim, Y_dim, Z_dim),mode='nearest',order=0)
    else:
        Rescaled_scan=scipy.ndimage.zoom(Data,(X_dim,Y_dim,Z_dim))

    Altered_header=None
    if Save_dir!=None:
        Altered_header=copy.copy(Header)
        Header["pixdim"][1]=1
        Header["pixdim"][2]=1
        Header["pixdim"][3]=1

        Functions.Save_image_data_as_nifti(Save_dir,Filename,Rescaled_scan,Altered_header)

    return Rescaled_scan,Altered_header
