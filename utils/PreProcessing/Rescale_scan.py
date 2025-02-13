import numpy as np
import scipy

def Rescale_scan(Image,pixdim_array,rescale_to=1.5,Mute=True,order=False):

    if Mute==False:
        print("----Start rescaling----")

    x_dim=pixdim_array[1]
    y_dim=pixdim_array[2]
    z_dim=pixdim_array[3]

    Scale=[x_dim/rescale_to,y_dim/rescale_to,z_dim/rescale_to]

    if order==0:
        Rescaled_scan=scipy.ndimage.zoom(Image,Scale,order=0)
    else:
        Rescaled_scan=scipy.ndimage.zoom(Image,Scale)

    if Mute==False:
        print("----Done rescaling----")

    return Rescaled_scan
