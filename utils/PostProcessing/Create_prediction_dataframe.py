import os
import sys
import nibabel as nib
import cv2

Current_directory = os.getcwd()

Main_folder = "/".join(Current_directory.split("/")[0:-2])  # Linux
sys.path.append(Main_folder)
Supportive_folder = "/".join(Current_directory.split("/")[0:-1])  # Linux
sys.path.append(Supportive_folder)

from utils.PreProcessing.Loading_and_saving_data import Data_processing
from utils.PreProcessing.Swap_axis import Swap_axis
from utils.Packages_file import *
Functions=Data_processing()
from utils.PostProcessing.Retrieve_label import Retrieve_label
from utils.PostProcessing.Create_encoding import Create_encoding

def Create_prediction_dataframe(Path_to_desired_labels,Patient_folder,RibFrac=False,Select_smallest=False,
                                Select_minimal_distance=False,Min_threshold=0,
                                Models=["Axial","Sagital","Coronal"]):

    def Extract_prediction(Path_to_prediction_folder,Path_to_GT,Path_to_desired_labels,Model,
                            Dictionary=None,Thresholded=False,Lesion="0",Identfication_method="Mask",
                            RibFrac=False,Select_smallest=Select_smallest,Select_minimal_distance=Select_minimal_distance,
                            Min_threshold=0):

        Path_to_labels=os.path.join(Path_to_prediction_folder,"labels")

        Image_files=os.listdir(Path_to_labels)
        Image_files=[i for i in Image_files if "." in i]

        if Dictionary==None:
            Dictionary=None
        else:
            Dictionary=Dictionary

        Labels=sorted([i.split("_")[0] for i in Image_files])
        Nr_detected_lesions=0
        All_lesions=[]

        label_dict=dict()
        image_files_for_labels=sorted([i for i in Image_files if i.split("_")[0]==Lesion])
        image_files_for_labels = sorted(image_files_for_labels, key=lambda x: int(x.split('_')[2]))

        for im in image_files_for_labels:

            im_file=im.split(".")[0]+".png"
            Path_to_image=os.path.join(Path_to_prediction_folder,im)
            Path_to_label=os.path.join(Path_to_GT,im_file)

            label_im=cv2.imread(Path_to_label,0)
            
            Predicted_labels,Confidences,TH_confidences=Retrieve_label(Path_to_labels,im,label_im.shape,label_im,Margin=0,
                RibFrac=RibFrac,Select_smallest=Select_smallest,Select_minimal_distance=Select_minimal_distance,Min_threshold=Min_threshold)

            label_dict["Predicted_label_%s"%Model]=Predicted_labels
            label_dict["Prediction_Confidences_%s"%Model]=Confidences
            label_dict["Prediction_Confidences_%s_TH"%Model]=TH_confidences

            if label in Predicted_labels:
                Nr_detected_lesions+=1

            Dictionary=Create_encoding(label_dict,label,Path_to_desired_labels,Model,Dictionary,Thresholded=Thresholded)

        return Dictionary,np.array(All_lesions),

    Yolo_prediction_folder=os.path.join(Patient_folder,"Prediction_yolo")

    Lesions=os.listdir(os.path.join(Yolo_prediction_folder,'Axial','labels'))

    Lesions=np.unique(["_".join(i.split("_")[:2]) for i in Lesions if "txt" in i])

    Lesions=sorted(Lesions)

    for lesion in Lesions:

        for ii in range(len(Models)):

            Path_to_prediction_folder=os.path.join(Yolo_prediction_folder,"%s"%(Models[ii]))
            Path_to_GT=os.path.join(Patient_folder,'Annotation_info','Segmentation_masks',"Labels_%s"%Models[ii])

            if ii==0:
                Dictionary=None
            else:
                Dictionary=Dictionary

            Dictionary,All_labels=Extract_prediction(Path_to_prediction_folder,Path_to_GT,Path_to_desired_labels,Models[ii],
                    Dictionary=None,Lesion=lesion.split("_")[0],RibFrac=RibFrac,Select_smallest=Select_smallest,
                    Select_minimal_distance=Select_minimal_distance,Min_threshold=Min_threshold)

            Dataframe=pd.DataFrame(Dictionary)

            Dataframe.to_excel(os.path.join(Patient_folder,"Lesions","Lesion_%s"%lesion,"Dataframe_%s.xlsx"%Models[ii]))

    return None
