from utils.Packages_file import *
from utils.PostProcessing.Return_label_functions import Return_label_dict
from utils.PreProcessing.Loading_and_saving_data import Data_processing
Functions=Data_processing()

def Create_nii_output(Path_to_label,File_name,Patient_folder,Summary_df,Rotate,Flip):

    Label,Header=Functions.Loading_Nifti_data(Path_to_label,File_name,Mute=True)
    centroids=[]
    labels=[]

    for i in range(Summary_df.shape[0]):
        centroid=np.array([Summary_df.iloc[i,1],Summary_df.iloc[i,2],Summary_df.iloc[i,3]]).astype(int)
        centroids.append(centroid)
        bone_label=Summary_df.iloc[i,6]
        labels.append(bone_label)

    if Flip:
        Label=[np.flip(Label[0],flip)]
    if Rotate:
        Label=[np.rot90(Label[0],Rotate)]

    region=regionprops(label(Label[0]))

    Labeled_annotations=np.zeros(Label[0].shape)

    for i in range(len(region)):
        empty_volume=np.zeros(Labeled_annotations.shape)
        coordinates=region[i].coords
        empty_volume[coordinates[:,0],coordinates[:,1],coordinates[:,2]]=1
        for j in range(len(centroids)):
            intensity=empty_volume[centroids[j][0],centroids[j][1],centroids[j][2]]
            if intensity==1:
                break

        new_intensity= labels[j]
        empty_volume=empty_volume*new_intensity
        Labeled_annotations+=empty_volume

    if Rotate:
        Labeled_annotations=np.rot90(Labeled_annotations,Rotate)

    if Flip:
        Labeled_annotations=np.flip(Labeled_annotations,flip)

    Functions.Save_image_data_as_nifti(Patient_folder,'Labeld_annotation_file.nii',Labeled_annotations.astype(int),Header=Header[0],Mute=True)

    return None
