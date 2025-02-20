import os
import sys
import nibabel as nib

Current_directory = os.getcwd()
Main_folder = "/".join(Current_directory.split("/")[0:-3])  # Linux
sys.path.append(Main_folder)

from utils.Packages_file import *
from utils.PreProcessing.Loading_and_saving_data import Data_processing

Functions=Data_processing()

def Obtain_x_y_z_lesion(Path_to_Label, Path_to_lesion_label_overview, File_name,Patient_folder,rotation=False,flip=False):

    with open(Path_to_lesion_label_overview, 'r') as file:
        Label_dictionary_overview = json.load(file)

    Lesion_overview=Label_dictionary_overview

    Annotation,Header=Functions.Loading_Nifti_data(Path_to_Label,File_name,Mute=True)

    if flip!= False:
        Annotation=[np.flip(Annotation[0],flip)]
    if rotation!=False:
        Annotation=[np.rot90(Annotation[0],rotation)]

    Scale_x=Header[0]["pixdim"][1]/1.5
    Scale_y=Header[0]["pixdim"][2]/1.5
    Scale_z=Header[0]["pixdim"][3]/1.5

    Regions=regionprops(label(Annotation[0]>0))

    Centroids_x=[]
    Centroids_y=[]
    Centroids_z=[]

    Scaled_centroids_x=[]
    Scaled_centroids_y=[]
    Scaled_centroids_z=[]
    Label_values=[]
    Lesion_ID=[]

    for j in range(len(Regions)):

        Centroid=Regions[j].centroid
        Found=False

        for i in range(len((Lesion_overview.keys()))):
            sub_dict=Lesion_overview[list(Lesion_overview.keys())[i]]

            if sub_dict["centroid_x"]==np.round(Centroid[0]).astype(float) and  sub_dict["centroid_y"]==np.round(Centroid[1]).astype(float) and  sub_dict["centroid_z"]==np.round(Centroid[2]).astype(float):
                label_value=sub_dict["label_values"]
                Found=True

        if Found:
            Lesion_ID.append(j+1)

            Label_values.append(label_value)

            Centroids_x.append(Centroid[0])
            Centroids_y.append(Centroid[1])
            Centroids_z.append(Centroid[-1])

            Scaled_centroids_x.append(np.round(Centroid[0]*Scale_x).astype(int))
            Scaled_centroids_y.append(np.round(Centroid[1]*Scale_y).astype(int))
            Scaled_centroids_z.append(np.round(Centroid[-1]*Scale_z).astype(int))

    Dataframe={"Lesion_ID":Lesion_ID,
                            "Centroid_x":Centroids_x,
                            "Centroid_y":Centroids_y,
                            "Centroid_z":Centroids_z,
                            "Scaled_centroid_x":Scaled_centroids_x,
                            "Scaled_centroid_y":Scaled_centroids_y,
                            "Scaled_centroid_z":Scaled_centroids_z,
                            "Label":Label_values}

    Dataframe=pd.DataFrame(Dataframe)

    Storage_folder=os.path.join(Patient_folder,'Annotation_info')
    Dataframe.to_excel(os.path.join(Storage_folder,"Transformed_Lesion_centroids.xlsx"))

    return None
