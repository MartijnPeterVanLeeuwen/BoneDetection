import copy
import numpy as np
def Apply_windowing(Volume,L,W,Mute=False):

    Windowed_volume=copy.copy(Volume)

    min_value=L-(0.5*W)
    max_value=L+(0.5*W)

    Windowed_volume[np.where(Volume<min_value)]=min_value
    Windowed_volume[np.where(Volume>max_value)]=max_value

    if Mute==False:
        print("--- Start Normalising Data---")

    Windowed_volume=(Windowed_volume - min_value)/(max_value-min_value)

    if Mute==False:
        print("---Data Normalised---")


    return Windowed_volume
