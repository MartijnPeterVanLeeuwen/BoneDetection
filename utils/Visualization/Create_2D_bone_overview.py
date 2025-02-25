import os
import sys
import scipy
from skimage.measure import label, regionprops

Current_directory = os.getcwd()
Main_folder = "/".join(Current_directory.split("/")[0:-2])  # Linux
sys.path.append(Main_folder)
from utils.PreProcessing.Loading_and_saving_data import Data_processing
from utils.Packages_file import *
from utils.PostProcessing.Return_label_functions import Return_label_dict

Functions=Data_processing()


def Create_2D_bone_overview(Affected_bones,Neighbouring_bones,Path_to_bone_labels,Path_to_all_bones,storage_dir,Exclude_Costal_Cartlidge=True,
                             Visualize_neighbouring_bones=True,Path_to_transformation_dict=None,Mute_text=False,Reduce_label=False):


    if Path_to_transformation_dict!=None:
        with open(Path_to_transformation_dict, 'r') as file:
            Label_transformation_dict = json.load(file)
        file.close()

    Label_dict=Return_label_dict(Path_to_all_bones)
    Reversed_label_dict= {v: k for k, v in Label_dict.items()}

    Label,Header=Functions.Loading_Nifti_data(Path_to_bone_labels,"Bone_atlas.nii",Mute=True)
    Swapped_lab=np.rot90(np.swapaxes(Label[0],0,1),1,axes=(1,2))

    if Exclude_Costal_Cartlidge==True:
        Swapped_lab[np.where(Swapped_lab==3)]=0
    else:
        Swapped_lab[np.where(Swapped_lab==3)]=0.05

    bone_masks=np.zeros((Swapped_lab.shape))
    empty_vol=np.zeros(Swapped_lab.shape)
    Neighbouring_bone_map=np.zeros(Swapped_lab.shape)

    centroid_affected_bones=[]

    for i in range(len(Affected_bones)):
        Approved=False
        coordinates=np.array(np.where(Swapped_lab==Affected_bones[i]))
        attempt=0
        while Approved==False:
            max_depth=np.argmax(coordinates[0,:])

            Coordinate_intensity_neighbour=Swapped_lab[coordinates[0][max_depth]-3:coordinates[0][max_depth]+5,
                                            coordinates[1][max_depth]-3:coordinates[1][max_depth]+5,
                                           coordinates[2][max_depth]-3:coordinates[2][max_depth]+5]

            unique_labels=np.unique(Coordinate_intensity_neighbour)
            unique_labels=[i for i in unique_labels if i!=0]
            Counts=[list(Coordinate_intensity_neighbour.flatten()).count(i) for i in unique_labels]
            Max_label=unique_labels[np.argmax(Counts)]

            if Max_label==Affected_bones[i] and Counts[np.argmax(Counts)]>20:
                Approved==True
                break
            else:
                coordinates=np.delete(coordinates, (max_depth), axis=1)
                attempt+=1
            if attempt>100:
                print('failed to find correct label')
                break

        Selected_coordinates=[coordinates[0][max_depth],coordinates[1][max_depth],coordinates[-1][max_depth]]
        Selected_coordinates.append(Affected_bones[i])
        centroid_affected_bones.append(Selected_coordinates)
        empty_vol[coordinates[0,:],coordinates[1,:],coordinates[2,:]]+=0.33

    #sorted_labels = [val for _, val in sorted(zip(centroid_affected_bones, All_labels),reverse=True)]

    sorted_centroids = sorted(centroid_affected_bones, key=lambda x: x[1])

    init=0
    min_distance=10
    Done=[]
    Side=[]
    previous_side=0
    for i in range(len(sorted_centroids)):

        if sorted_centroids[i][3] not in Done:
            bone_label=sorted_centroids[i][3]

            slice_distance=sorted_centroids[i][1]-init

            if slice_distance<min_distance and previous_side==0:

                sorted_centroids[i][1]+=min_distance-slice_distance
                Side.append(1)
                previous_side=1
            else:
                Side.append(0)
                previous_side=0


            b0=bone_label

            init=sorted_centroids[i][1]
            Done.append(sorted_centroids[i][3])
        else:
            Side.append(-1)
    Only_neigbouring=np.zeros(empty_vol.shape)
    Only_neigbouring[np.where(empty_vol==0)]=1

    for i in range(len(Neighbouring_bones)):
        coordinates=np.where(Swapped_lab==Neighbouring_bones[i])
        Neighbouring_bone_map[coordinates]+=0.33

    Neighbouring_bone_map=Neighbouring_bone_map*Only_neigbouring

    Swapped_label_copy=copy.copy(Swapped_lab)

    fig,ax=plt.subplots(1,4,figsize=(14.8,5),dpi=400)

    plt.subplots_adjust(top=None, wspace=None, hspace=0.1)
    for iii in range(2):
        Flip=False
        for ii in range(2):
            Flip=False

            if ii==1 and iii==1:
                iii=0
            elif ii==1 and iii==0:
                iii=1

            if (iii==1 and ii==0) or (iii==1 and ii==1):
                Flip=True

            if ii ==1:

                if iii==1:
                    min_scalar=0.85
                    max_scalar=-0.5
                else:
                    min_scalar=-0.5
                    max_scalar=0.85

                Degrading_map=np.ones(np.rot90(bone_masks,1,axes=(0,2)).shape)
                degrading_scalar=np.linspace(min_scalar,max_scalar,np.rot90(bone_masks,1,axes=(0,2)).shape[0])

                for i in range(Degrading_map.shape[0]):
                    Degrading_map[i,:,:]=Degrading_map[i,:,:]*degrading_scalar[i]

                Bone_volume=np.rot90(empty_vol,1,axes=(0,2))
                Neighbouring_bone_volume=np.rot90(Neighbouring_bone_map,1,axes=(0,2))
                Swapped_lab_plot=np.rot90(Swapped_label_copy,1,axes=(0,2))

            else:
                if iii==0:
                    min_scalar=0.25
                    max_scalar=0.9
                else:
                    min_scalar=0.75
                    max_scalar=-0.5

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

            selection_bone_mask=selection_bone_mask*1.75

            margin=50

            start_point_left=-90
            start_point_right=complete_bone_mask.shape[1]+20
            Unique_label_detections=np.unique(Affected_bones)
            Processed_labels=[]
            fontsize=5

            for j in range(len(Affected_bones)):
                No_counts=0

                k=sorted_centroids[j]

                if k[3] not in Processed_labels:

                    side=Side[j]
                    Processed_labels.append(k[3])
                    bone_label=Reversed_label_dict[k[3]]

                    if Path_to_transformation_dict!=None:
                        bone_label=Label_transformation_dict[bone_label]

                    No_counts=Affected_bones.count(k[3])

                    if Reduce_label:
                        if 'rib' in str(bone_label):
                            bone_label='Rib'
                        if 'vertebra' in str(bone_label):
                            bone_label='Vertebra'

                    if No_counts>1:
                        bone_label=bone_label+' (%sx)'%No_counts

                    if ii==0:
                        make_label=True
                        if iii==0:
                            index=0

                            if side==0:
                                start=k[2]
                                end=start_point_left
                                side_text=start_point_left

                            else:
                                start=start_point_right
                                end=k[2]
                                side_text=start_point_right

                            if 'left' in bone_label:
                                make_label=False
                        else:
                            index=2
                            start=complete_bone_mask.shape[1]-k[2]

                            if side==0:
                                start=complete_bone_mask.shape[1]-k[2]
                                end=start_point_left
                                side_text=start_point_left
                            else:
                                start=start_point_right
                                end=complete_bone_mask.shape[1]-k[2]
                                side_text=start_point_right

                            if 'right' in bone_label:
                                make_label=False

                        letters=len(bone_label)
                        current_sp=start_point_left-letters-margin

                        if make_label and Mute_text==False:
                            ax[index].hlines(k[1], xmin=end, xmax=start,linestyles='dotted')
                            ax[index].text(side_text,k[1],bone_label,fontsize=fontsize,color='black')

                    else:

                        make_label=True
                        if iii==1:
                            index=3

                            if side==0:
                                start=complete_bone_mask.shape[1]-k[0]
                                end=start_point_left
                                side_text=start_point_left
                            else:
                                start=start_point_right
                                end=complete_bone_mask.shape[1]-k[0]
                                side_text=start_point_right

#                            start=complete_bone_mask.shape[1]-k[0]
                            if 'right' in bone_label:
                                make_label=False
                        else:
                            index=1
                            start=k[0]
                            if side==0:
                                start=k[0]
                                end=start_point_left
                                side_text=start_point_left
                            else:
                                start=k[0]
                                end=start_point_right
                                side_text=start_point_right


                            if 'left' in bone_label:
                                make_label=False

                        letters=len(bone_label)
                        current_sp=start_point_left-letters-margin

                        if make_label and Mute_text==False:
                            ax[index].hlines(k[1], xmin=end, xmax=start,linestyles='dotted')
                            ax[index].text(side_text,k[1],bone_label,fontsize=fontsize,color='black')


                Complete_overview[:,:,0]=complete_bone_mask
                Complete_overview[:,:,1]=complete_bone_mask-selection_bone_mask-0.4*selection_neighbouring_mask
                Complete_overview[:,:,2]=complete_bone_mask-selection_bone_mask-selection_neighbouring_mask
                Complete_overview=np.clip(Complete_overview,0,255)

                if Flip:
                    Complete_overview=np.flip(Complete_overview,axis=1)

                ax[index].imshow(Complete_overview)
                ax[index].axis('off')

    storage_file=os.path.join(storage_dir,'Affected_Bones.png')
    plt.tight_layout()
    plt.savefig(storage_file,bbox_inches="tight")

    return None
