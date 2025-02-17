import os
import sys
import scipy
from skimage.measure import label, regionprops

Current_directory = os.getcwd()
Main_folder = "/".join(Current_directory.split("/")[0:-2])  # Linux
sys.path.append(Main_folder)
from utils.PreProcessing.Loading_and_saving_data import Data_processing
from utils.Packages_file import *
Functions=Data_processing()


def Create_2D_bone_overview(Affected_bones,Neighbouring_bones,Path_to_bone_labels,file,storage_dir,Exclude_Costal_Cartlidge=True,
                             Visualize_neighbouring_bones=True):

    Label,Header=Functions.Loading_Nifti_data(Path_to_bone_labels,file,Mute=True)
    Swapped_lab=np.rot90(np.swapaxes(Label[0],0,1),1,axes=(1,2))

    if Exclude_Costal_Cartlidge==True:
        Swapped_lab[np.where(Swapped_lab==3)]=0

    bone_masks=np.zeros((Swapped_lab.shape))

    empty_vol=np.zeros(Swapped_lab.shape)
    Neighbouring_bone_map=np.zeros(Swapped_lab.shape)

    for i in range(len(Affected_bones)):
        empty_vol[np.where(Swapped_lab==Affected_bones[i])]+=0.33

    Only_neigbouring=np.zeros(empty_vol.shape)
    Only_neigbouring[np.where(empty_vol==0)]=1

    for i in range(len(Neighbouring_bones)):
        Neighbouring_bone_map[np.where(Swapped_lab==Neighbouring_bones[i])]+=0.33
    Neighbouring_bone_map=Neighbouring_bone_map*Only_neigbouring

    Swapped_label_copy=copy.copy(Swapped_lab)
    Flip=False

    fig,ax=plt.subplots(2,2,figsize=(5,9),dpi=300)

    for iii in range(2):

        if iii>0:
            Flip=True

        for ii in range(2):

            if ii ==1:

                if iii==1:
                    min_scalar=0.48
                    max_scalar=1
                else:
                    min_scalar=1
                    max_scalar=0.48

                Degrading_map=np.ones(np.rot90(bone_masks,1,axes=(0,2)).shape)
                degrading_scalar=np.linspace(min_scalar,max_scalar,np.rot90(bone_masks,1,axes=(0,2)).shape[0])

                for i in range(Degrading_map.shape[0]):
                    Degrading_map[i,:,:]=Degrading_map[i,:,:]*degrading_scalar[i]

                Bone_volume=np.rot90(empty_vol,1,axes=(0,2))
                Neighbouring_bone_volume=np.rot90(Neighbouring_bone_map,1,axes=(0,2))
                Swapped_lab_plot=np.rot90(Swapped_label_copy,1,axes=(0,2))

            else:
                if iii==0:
                    min_scalar=0.65
                    max_scalar=1
                else:
                    min_scalar=1
                    max_scalar=0

                Degrading_map=np.ones(bone_masks.shape)
                degrading_scalar=np.linspace(min_scalar,max_scalar,bone_masks.shape[0])

                for i in range(Degrading_map.shape[0]):
                    Degrading_map[i,:,:]=Degrading_map[i,:,:]*degrading_scalar[i]

                Bone_volume=copy.copy(empty_vol)
                Neighbouring_bone_volume=copy.copy(Neighbouring_bone_map)

                Swapped_lab_plot=Swapped_label_copy

            multiplied_bone_mask=Bone_volume*Degrading_map
            multiplied_neighbouring_bone_mask=Neighbouring_bone_volume*Degrading_map
            selection_bone_mask=np.max(multiplied_bone_mask,axis=0)
            selection_neighbouring_mask=np.max(multiplied_neighbouring_bone_mask,axis=0)

            Swapped_lab_plot=np.array(Swapped_lab_plot)>0
            Complete_bone_masks=Swapped_lab_plot*Degrading_map
            complete_bone_mask=np.max(Complete_bone_masks,axis=0)

            Complete_overview=np.zeros((complete_bone_mask.shape[0],complete_bone_mask.shape[1],3))

            if Visualize_neighbouring_bones==False:
                selection_neighbouring_mask=0

            Complete_overview[:,:,0]=complete_bone_mask
            Complete_overview[:,:,1]=complete_bone_mask-selection_bone_mask-0.4*selection_neighbouring_mask
            Complete_overview[:,:,2]=complete_bone_mask-selection_bone_mask-selection_neighbouring_mask
            Complete_overview=np.clip(Complete_overview,0,255)

            if Flip:
                Complete_overview=np.flip(Complete_overview,axis=1)

            ax[iii,ii].imshow(Complete_overview,vmin=0,vmax=1)

            ax[iii,ii].axis('off')

    storage_file=os.path.join(storage_dir,'Affected_Bones.png')
    plt.tight_layout()
    plt.savefig(storage_file,bbox_inches="tight")

    return None
