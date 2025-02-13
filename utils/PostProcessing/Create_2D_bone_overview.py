import os
import sys
import scipy

from utils.PreProcessing.Loading_and_saving_data import Data_processing

Current_directory = os.getcwd()
Main_folder = "/".join(Current_directory.split("/")[0:-2])  # Linux
sys.path.append(Main_folder)

from utils.Packages_file import *

Functions=Data_processing()


def Create_2D_bone_overview(Affected_bones,Path_to_bone_labels,file,storage_dir):

    Label,Header=Functions.Loading_Nifti_data(Path_to_bone_labels,file,Mute=True)
    Swapped_lab=np.rot90(np.swapaxes(Label[0],0,1),1,axes=(1,2))
    Swapped_lab[np.where(Swapped_lab==3)]=0

    bone_masks=np.zeros((Swapped_lab.shape))
    Degrading_map=np.ones(bone_masks.shape)
    degrading_scalar=np.linspace(0,1,bone_masks.shape[0])

    for i in range(Degrading_map.shape[0]):
        Degrading_map[i,:,:]=Degrading_map[i,:,:]*degrading_scalar[i]

    empty_vol=np.zeros(Swapped_lab.shape)
    for i in range(len(Affected_bones)):
        empty_vol[np.where(Swapped_lab==Affected_bones[i])]=1

    multiplied_bone_mask=empty_vol*Degrading_map
    selection_bone_mask=np.max(multiplied_bone_mask,axis=0)

    Swapped_lab=np.array(Swapped_lab)>0
    Complete_bone_masks=Swapped_lab*Degrading_map
    complete_bone_mask=np.max(Complete_bone_masks,axis=0)

    Complete_overview=np.zeros((complete_bone_mask.shape[0],complete_bone_mask.shape[1],3))

    Complete_overview[:,:,0]=complete_bone_mask
    Complete_overview[:,:,1]=complete_bone_mask-selection_bone_mask
    Complete_overview[:,:,2]=complete_bone_mask-selection_bone_mask


    fig,ax=plt.subplots(1,2)
    ax[0].imshow(complete_bone_mask,'grey',vmin=0,vmax=1)
    ax[1].imshow(Complete_overview,vmin=0,vmax=1)

    ax[0].axis('off')
    ax[1].axis('off')

    storage_file=os.path.join(storage_dir,'Overview_Bone_lesions.png')
    plt.tight_layout()
    plt.savefig(storage_file,bbox_inches="tight")

    return None

#Path_to_bone_labels="/home/mleeuwen/DATA/TSv3_Selection/Labels"
#file="Scan_0616.nii"
#storage_dir='/home/mleeuwen/Plot_folder'
#Create_overview_plot([1,2,3],Path_to_bone_labels,file,storage_dir)
