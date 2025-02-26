import os
import sys
import nibabel as nib
from utils.PreProcessing.Loading_and_saving_data import Data_processing
from utils.PreProcessing.Apply_windowing import *
from utils.PostProcessing.Return_label_functions import Return_label_dict
from utils.Packages_file import *
Functions=Data_processing()

def Create_Abnormality_overview(Label_name,Path_to_desired_labels,Path_to_Segmentations,Path_to_storage,rotation=False,flip=False):

    Path_to_storage=os.path.join(Path_to_storage,'Annotation_info')

    if os.path.isdir(Path_to_storage)==False:
        os.mkdir(Path_to_storage)

    file=os.path.join(Path_to_storage,"Lesion_centroids.json")

    if os.path.isfile(file)==False:


        Label_dict=Return_label_dict(Path_to_desired_labels)
        reversed_dict = {v: k for k, v in Label_dict.items()}
        Dictionary={}
        Patient_dictionary={}

        Image,Header=Functions.Loading_Nifti_data(Path_to_Segmentations,Label_name,Mute=True)

        if flip:
            Image=[np.flip(Image[0],flip)]
        if rotation:
            Image=[np.rot90(Image[0],rotation)]

        Lesions_props=regionprops(label(Image[0]>0))
        lesion_nr=1

        for ii in Lesions_props:
            Lesion_dictionary={}
            Centroid=np.round(ii.centroid).astype(int)
            Intensities=Image[0][ii.coords[:,0],ii.coords[:,1],ii.coords[:,2]]
            label_values=np.unique(Intensities)
            label_values=[i for i in label_values if i!=0]

            if len(label_values)>1:
                Counts=[list(Intensities).count(i) for i in label_values]
                max=np.argmax(Counts)
                label_values=[label_values[max]]

            label_values=label_values[0]
            Lesion_dictionary['centroid_x']=Centroid[0].astype(float)
            Lesion_dictionary['centroid_y']=Centroid[1].astype(float)
            Lesion_dictionary['centroid_z']=Centroid[2].astype(float)
            Lesion_dictionary['label_values']=label_values.astype(float)
            Patient_dictionary[str(lesion_nr)]=Lesion_dictionary
            lesion_nr+=1

        json_file = json.dumps(Patient_dictionary,indent=4)
        f = open(file,"w")
        f.write(json_file)
        f.close()

    return file
