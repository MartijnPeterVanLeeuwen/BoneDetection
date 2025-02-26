import argparse

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
current_wd= os.getcwd()

parser = argparse.ArgumentParser(description="Execute Inference")

parser.add_argument("--Scan_name", type=str, help="Name of the scan in the CT and Label folder that should be processed")
parser.add_argument("--Label_name", type=str, help="Name of the file that contains the bone abnormality data",default=None)
parser.add_argument("--Experiment_name", type=str, help="The name that should be assigned to the experiment",default="Experiment")
parser.add_argument("--Device", help="The selected GPU on which will be used during inference, or type 'cpu'",default='cpu')
parser.add_argument("--Slices", type=int, help="The number of slices per plane on which you want to run inference",default=3)
parser.add_argument("--Rotate_input", type=int, help="Rotate the the input 90 degrees, the variable should indicate the number of times the input data should be rotated",default=0)
parser.add_argument("--Flip_input", type=int, help="Flip the input axes",default=False)
parser.add_argument("--IoU", type=float, help="IoU argument passed into YOLOs inference method",default=0.75)
parser.add_argument("--Minimal_TH", type=float, help="All predictions below this bounding box will be removed",default=0.75)
parser.add_argument("--Dont_save_prediction_images", help="Indicate if the png predictions made by YOLOv5 should be stored",action='store_true')
parser.add_argument("--No_inference", help="Indicate if want to run the inference, or if you want to change the post-processing of the model output",action='store_true')
parser.add_argument("--Mute", help="Indicate if want to mute printing of statements during execution of the script",action='store_true')
parser.add_argument("--Remove_2D_bone_overview", help="Indicate if you dont want to include a 2D bone overview ",action='store_true')
parser.add_argument("--Finalize_inference", help="Indicate if you want to remove all the files that can be used to change the prediction labels ",action='store_true')
parser.add_argument("--Switch_left_right", help="Depending on the orientation, left and right can be switched ",action='store_true')
parser.add_argument("--Mute_text_in_plot", help="Mute the plotting of the labels in the plots if it gets too cluttered ",action='store_true')
parser.add_argument("--Reduce_labels",help="Don't assign a level to the ribs or vertebrae, creating",action='store_true')


# Parse arguments
args = parser.parse_args()

if __name__ == "__main__":

    if args.Mute==False:
       print("======================== Start Executing Inference Script ======================== ")

    #Load the file that contains the paths to the input data and the storage directory.
    with open(os.path.join(current_wd,'paths.json'), 'r') as file:
        paths = json.load(file)

    if os.path.isdir(paths['Path_to_storage'])==False:
        os.mkdir(paths['Path_to_storage'])

    #Define the directory in which the results should be stored
    patient_folder=os.path.join(paths["Path_to_storage"],args.Experiment_name)

    # If no explicit "Label_name" is provided, it is set equal to the "Scan_name".
    if args.Label_name==None:
        args.Label_name=args.Scan_name

    # If you do not want to run inference, no new directory is created, and an existing patient_folder is used.
    if args.No_inference==False:
        patient_folder=Check_storage_dir(patient_folder)

        if args.Mute==False:
           print("======================== Storage folder created  ======================== ")

    Patient_ID=args.Scan_name.split('.nii')[0]

    path_to_utils=os.path.join(current_wd,'utils')

    path_to_bone_types=os.path.join(path_to_utils,'Desired_labels.txt')

    path_to_segmentations=paths['Path_to_abnormalities']

    #Create an a file in which information about the included abnormalities is stored
    Path_to_lesion_label_overview=Create_Abnormality_overview(args.Scan_name,path_to_bone_types,path_to_segmentations,patient_folder,
                                rotation=args.Rotate_input, flip=args.Flip_input)

    #Transform the annotation file so that each abnormality has a unique integer value. The centroids are also scaled so that they fit with a scaling of [1.5,1.5,1.5]
    Annotation=Obtain_x_y_z_lesion(paths['Path_to_abnormalities'], Path_to_lesion_label_overview, args.Scan_name, patient_folder,
                                rotation=args.Rotate_input, flip=args.Flip_input)

    #The next section is run when the "args.No_inference" is not called.
    if args.No_inference==False:

        if args.Mute==False:
           print("======================== Start Inference  ======================== ")
           start_time=time.time()

        Path_to_weights=os.path.join(current_wd,'weights')
        Path_to_yolo_folder=os.path.join(path_to_utils,'Model')

        #The next function performs the multiplane bone detection.
        Predict_multi_model_function(paths["Path_to_input_CT"],Annotation, args.Scan_name,Path_to_yolo_folder,
                            Patient_ID, patient_folder, Path_to_weights=Path_to_weights,Total_number_of_slices=args.Slices, GPU=args.Device,
                            L=400, W=1800,IOU_threshold=args.IoU, Dont_save_prediction_images=args.Dont_save_prediction_images,
                            rotation=args.Rotate_input, flip=args.Flip_input)

        #This function creates the individual folders in which the bone detection results are stored.
        Create_lesion_folders(patient_folder)

        #From the outputted label files from the YOLOv5 model, a dataframe is created for each plane
        Create_prediction_dataframe(path_to_bone_types, patient_folder,Select_smallest=False,
                                Select_minimal_distance=True,Min_threshold=args.Minimal_TH)
        if args.Mute==False:
           end_time=time.time()
           duration=end_time-start_time
           duration=np.round(duration/60,2)
           print("======================== Ended Inference in %s minutes  ======================== "%duration)

    # If you want to switch the orientation of 'left' and 'right', the argument "args.Switch_left_right" does so.
    if args.Switch_left_right==False:
        Path_to_label_translation_dict=os.path.join(current_wd,'utils','Bone_labels_pov_patient.json')
        Switch_orientation=True
    else:
        Path_to_label_translation_dict=os.path.join(current_wd,'utils','Bone_labels_pov_outside.json')
        Switch_orientation=False

    #This file contains the neighbouring bones of each of the bones. The file contains an "Acceptable" and "Unacceptable" key. The "Acceptable" is the neighbour bone, and the "Unacceptable" is the same bone only on the onter side (left/right)
    Path_to_neighbouring_files=os.path.join(current_wd,'utils','Neighbour_file.json')

    #Combine the multiple predictions into 1 single label for each abnormality
    Affected_bones,Neighbouring_bones,Summary_dict=Obtain_single_label(path_to_bone_types, patient_folder,Path_to_neighbouring_files,
                                                            Path_to_transformation_dict=Path_to_label_translation_dict,TH=args.Minimal_TH)

    if args.Remove_2D_bone_overview==False:
        #Create a 2D image showing which bones are affected by the bone abnormalities.
        Create_2D_bone_overview(Affected_bones,Neighbouring_bones,current_wd,path_to_bone_types,patient_folder,
                                Path_to_transformation_dict=Path_to_label_translation_dict,Mute_text=args.Mute_text_in_plot,Reduce_label=args.Reduce_labels)

    path_to_bone_switch_label=os.path.join(current_wd,'utils','Bone_label_switch.json')

    Path_to_transformed_lesion_label_overview=os.path.join(patient_folder,'Annotation_info',"Transformed_Lesion_centroids.xlsx")

    #Summarize the findings into a single dataframe and store this in the "patient_folder"
    Summary_df=Create_summary_results(Summary_dict,patient_folder,Path_to_transformed_lesion_label_overview,path_to_bone_switch_label,path_to_bone_types,Switch_orientation=Switch_orientation,Reduce_label=args.Reduce_labels)

    #Transform the annotation file so that each seperate bone abnormality has an 'int' value that indicates in what bone that annotation is located in.
    Create_nii_output(paths['Path_to_abnormalities'],args.Label_name,patient_folder,Summary_df,Rotate=args.Rotate_input, Flip=args.Flip_input)

    #If no further finetuning is required, you can remove all the irrelant files.
    Cleanup_folder(patient_folder,Remove_segmentation_folders=args.Finalize_inference)

    if args.Mute==False:
       print(Summary_df)

       print("======================== Succesfully Concluded Inference Script  ======================== ")
