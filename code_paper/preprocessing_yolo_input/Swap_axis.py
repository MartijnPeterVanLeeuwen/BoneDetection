import numpy as np

def Swap_axis(Image_volume,Label_volume,axis=0,Swap=True,Manual_max=False,Manual_min=False):
    if Swap:
        Swapped_Image_volume=np.swapaxes(Image_volume,-1,axis)
        Swapped_Label_volume=np.swapaxes(Label_volume,-1,axis)
    else:
        Swapped_Image_volume=Image_volume
        Swapped_Label_volume=Label_volume
    Max_dim=np.max([Swapped_Image_volume.shape[0],Swapped_Image_volume.shape[1]])

    Difference_x= Max_dim-Swapped_Image_volume.shape[0]
    Half_Difference_x=Difference_x//2
    Difference_y=Max_dim-Swapped_Image_volume.shape[1]
    Half_Difference_y=Difference_y//2

    if Manual_max and Manual_min:
        Square_volume_image=np.ones((Max_dim,Max_dim,Swapped_Image_volume.shape[-1]))*Manual_min
        Square_volume_label=np.ones((Max_dim,Max_dim,Swapped_Image_volume.shape[-1]))*Manual_min
    else:
        Square_volume_image=np.zeros((Max_dim,Max_dim,Swapped_Image_volume.shape[-1]))
        Square_volume_label=np.zeros((Max_dim,Max_dim,Swapped_Image_volume.shape[-1]))


    Square_volume_image[Half_Difference_x:(Swapped_Image_volume.shape[0]+Half_Difference_x),
                        Half_Difference_y:(Swapped_Image_volume.shape[1]+Half_Difference_y),
                        :] = Swapped_Image_volume

    Square_volume_label[Half_Difference_x:(Swapped_Image_volume.shape[0]+Half_Difference_x),
                        Half_Difference_y:(Swapped_Image_volume.shape[1]+Half_Difference_y),
                        :] = Swapped_Label_volume

    return Square_volume_image,Square_volume_label,[Difference_x,Difference_y]
