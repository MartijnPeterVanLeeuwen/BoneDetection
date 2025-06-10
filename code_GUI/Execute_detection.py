import sys
import os
current_wd="\\".join(os.getcwd().split('\\')[:-1])
sys.path.append(current_wd)
import shutil
from utils.Packages_file import *
from utils.Inference.Move_input_to_yolo_folder import Move_input_to_yolo_folder
from utils.Inference.Move_input_back import Move_input_back
from utils.PostProcessing.Create_prediction_dataframe import Create_prediction_dataframe
from utils.PreProcessing.Obtain_x_y_z_lesion import Obtain_x_y_z_lesion
from utils.PostProcessing.Create_lesion_folders import Create_lesion_folders
from utils.PreProcessing.Create_Abnormality_overview import Create_Abnormality_overview
from utils.Inference.Predict_multi_model_function import Predict_multi_model_function
from utils.PostProcessing.Cleanup_folder import Cleanup_folder
from utils.Visualization.Create_2D_bone_overview import Create_2D_bone_overview
from utils.PostProcessing.Obtain_single_label import Obtain_single_label
from utils.PreProcessing.Check_storage_dir import Check_storage_dir
from utils.PostProcessing.Create_summary_results import Create_summary_results
from utils.Visualization.Create_nii_output import Create_nii_output


def Run_Inference(Storage_dir="C:\\Users\\mleeuwen\\Demo",
                    Experiment_name='Demo_1',
                    Scan_name="CT_1.nii",
                    Flip_input=False,
                    Rotate_input=False,
                    Label_name="Synthetic_lesion.nii",
                    Device='cpu',
                    Slices=3,
                    Minimal_TH=0.75,
                    Finalize_inference=False,
                    Switch_left_right=False,
                    No_inference=False,):

    Path_to_CT=Storage_dir
    Path_to_Label=Storage_dir
    path_to_segmentations=Storage_dir
    path_to_segmentations=Storage_dir

    #Define the directory in which the results should be stored
    patient_folder=os.path.join(Storage_dir,Experiment_name)
    if os.path.isdir(patient_folder)==False:
        os.mkdir(patient_folder)
    else:
        shutil.rmtree(patient_folder)
        os.mkdir(patient_folder)

    Patient_ID=Scan_name.split('.nii')[0]

    path_to_utils=os.path.join(current_wd,'utils')

    path_to_bone_types=os.path.join(path_to_utils,'Desired_labels.txt')
    print('start creating bone abnormality overview')
    #Create an a file in which information about the included abnormalities is stored
    Path_to_lesion_label_overview=Create_Abnormality_overview(Label_name,path_to_bone_types,path_to_segmentations,patient_folder,
                                rotation=Rotate_input, flip=Flip_input)

    print('overview created')
    #Transform the annotation file so that each abnormality has a unique integer value. The centroids are also scaled so that they fit with a scaling of [1.5,1.5,1.5]
    Annotation=Obtain_x_y_z_lesion(path_to_segmentations, Path_to_lesion_label_overview, Label_name, patient_folder,
                                rotation=Rotate_input, flip=Flip_input)

    #The next section is run when the "args.No_inference" is not called.
    Path_to_weights=os.path.join(current_wd,'weights')
    Path_to_yolo_folder=os.path.join(path_to_utils,'Model')

    #The next function performs the multiplane bone detection.
    Predict_multi_model_function(Path_to_CT,Annotation, Scan_name,Path_to_yolo_folder,
                        Patient_ID, patient_folder, Path_to_weights=Path_to_weights,Total_number_of_slices=Slices, GPU=Device,
                        L=400, W=1800,IOU_threshold=0.75, Dont_save_prediction_images=False,
                        rotation=Rotate_input, flip=Flip_input)

    #This function creates the individual folders in which the bone detection results are stored.
    Create_lesion_folders(patient_folder)

    #From the outputted label files from the YOLOv5 model, a dataframe is created for each plane
    Create_prediction_dataframe(path_to_bone_types, patient_folder,Select_smallest=False,
                            Select_minimal_distance=True,Min_threshold=Minimal_TH)
    # If you want to switch the orientation of 'left' and 'right', the argument "args.Switch_left_right" does so.
    if Switch_left_right==False:
        Path_to_label_translation_dict=os.path.join(current_wd,'utils','Bone_labels_pov_patient.json')
        Switch_orientation=True
    else:
        Path_to_label_translation_dict=os.path.join(current_wd,'utils','Bone_labels_pov_outside.json')
        Switch_orientation=False

    #This file contains the neighbouring bones of each of the bones. The file contains an "Acceptable" and "Unacceptable" key. The "Acceptable" is the neighbour bone, and the "Unacceptable" is the same bone only on the onter side (left/right)
    Path_to_neighbouring_files=os.path.join(current_wd,'utils','Neighbour_file.json')

    #Combine the multiple predictions into 1 single label for each abnormality
    Affected_bones,Neighbouring_bones,Summary_dict=Obtain_single_label(path_to_bone_types, patient_folder,Path_to_neighbouring_files,
                                                            Path_to_transformation_dict=Path_to_label_translation_dict,TH=Minimal_TH)

    #Create a 2D image showing which bones are affected by the bone abnormalities.
    Create_2D_bone_overview(Affected_bones,Neighbouring_bones,current_wd,path_to_bone_types,patient_folder,
                            Path_to_transformation_dict=Path_to_label_translation_dict,Mute_text=False,Reduce_label=False)

    path_to_bone_switch_label=os.path.join(current_wd,'utils','Bone_label_switch.json')

    Path_to_transformed_lesion_label_overview=os.path.join(patient_folder,'Annotation_info',"Transformed_Lesion_centroids.xlsx")

    #Summarize the findings into a single dataframe and store this in the "patient_folder"
    Summary_df=Create_summary_results(Summary_dict,patient_folder,Path_to_transformed_lesion_label_overview,path_to_bone_switch_label,path_to_bone_types,Switch_orientation=Switch_orientation,Reduce_label=False)

    #Transform the annotation file so that each seperate bone abnormality has an 'int' value that indicates in what bone that annotation is located in.
    Create_nii_output(path_to_segmentations,Label_name,patient_folder,Summary_df,Rotate=Rotate_input, Flip=Flip_input)

    #If no further finetuning is required, you can remove all the irrelant files.
    Cleanup_folder(patient_folder,Remove_segmentation_folders=Finalize_inference)

    print("======================== Succesfully Concluded Inference Script  ======================== ")
