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
current_wd= os.getcwd()

# Create a parser object
parser = argparse.ArgumentParser(description="Execute Inference")

# Add arguments
parser.add_argument("--Scan_name", type=str, help="Name of the scan in the CT and Label folder that should be processed")
parser.add_argument("--Experiment_name", type=str, help="The name that should be assigned to the experiment",default="Experiment")
parser.add_argument("--Use_existing_folder", help="Indicate if you want to create a new folder or if you want to work in an existing folder",action='store_true')
parser.add_argument("--Device", help="The selected GPU on which will be used during inference, or type 'cpu'",default='cpu')
parser.add_argument("--Flip_input", type=int, help="Flip the input axes",default=False)
parser.add_argument("--Rotate_input", type=int, help="Rotate the the input 90 degrees, the variable should indicate the number of times the input data should be rotated",default=0)
parser.add_argument("--IoU", type=float, help="IoU argument passed into YOLOs inference method",default=0.75)
parser.add_argument("--Minimal_TH", type=float, help="All predictions below this bounding box will be removed",default=0.75)
parser.add_argument("--Slices", type=int, help="The number of slices per plane on which you want to run inference",default=3)
parser.add_argument("--Dont_save_prediction_images", help="Indicate if the png predictions made by YOLOv5 should be stored",action='store_true')
parser.add_argument("--No_inference", help="Indicate if want to run the inference, or if you want to change the post-processing of the model output",action='store_true')
parser.add_argument("--Mute", help="Indicate if want to mute printing of statements during execution of the script",action='store_true')
parser.add_argument("--Remove_2D_bone_overview", help="Indicate if you dont want to include a 2D bone overview ",action='store_true')

# Parse arguments
args = parser.parse_args()

if __name__ == "__main__":

    if args.Mute==False:
       print("======================== Start Executing Inference Script ======================== ")

    with open(os.path.join(current_wd,'paths.json'), 'r') as file:
        paths = json.load(file)

    if os.path.isdir(paths['Path_to_storage'])==False:
        os.mkdir(paths['Path_to_storage'])

    patient_folder=os.path.join(paths["Path_to_storage"],args.Experiment_name)

    if args.Use_existing_folder == False:
        patient_folder=Check_storage_dir(patient_folder)

        if args.Mute==False:
           print("======================== Storage folder created  ======================== ")

    Patient_ID=args.Scan_name.split('.nii')[0]

    path_to_utils=os.path.join(current_wd,'utils')
    path_to_bone_types=os.path.join(path_to_utils,'Desired_labels.txt')

    path_to_segmentations=paths['Path_to_abnormalities']

    Path_to_lesion_label_overview=Create_Abnormality_overview(args.Scan_name,path_to_bone_types,path_to_segmentations,patient_folder,
                                rotation=args.Rotate_input, flip=args.Flip_input)

    Obtain_x_y_z_lesion(paths['Path_to_abnormalities'], Path_to_lesion_label_overview, args.Scan_name, patient_folder,
                                rotation=args.Rotate_input, flip=args.Flip_input)

    if args.No_inference==False:

        if args.Mute==False:
           print("======================== Start Inference  ======================== ")
           start_time=time.time()

        Path_to_weights=os.path.join(current_wd,'weights')
        Path_to_yolo_folder=os.path.join(path_to_utils,'Model')

        Predict_multi_model_function(paths["Path_to_input_CT"],paths['Path_to_abnormalities'] , args.Scan_name,Path_to_yolo_folder,
                            Patient_ID, patient_folder, Path_to_weights=Path_to_weights,Total_number_of_slices=args.Slices, GPU=args.Device,
                            L=400, W=1800,IOU_threshold=args.IoU, Dont_save_prediction_images=args.Dont_save_prediction_images,
                            rotation=args.Rotate_input, flip=args.Flip_input)

        Create_lesion_folders(patient_folder)

        Create_prediction_dataframe(path_to_bone_types, patient_folder,Select_smallest=False,
                                Select_minimal_distance=True,Min_threshold=args.Minimal_TH)
        if args.Mute==False:
           end_time=time.time()
           duration=end_time-start_time
           duration=np.round(duration/60,2)
           print("======================== Ended Inference in %s minutes  ======================== "%duration)



    Affected_bones,Summary_dict=Obtain_single_label(path_to_bone_types, patient_folder,TH=args.Minimal_TH)

    if args.Remove_2D_bone_overview==False:
        Create_2D_bone_overview(Affected_bones,current_wd,"Bone_atlas.nii",patient_folder)

    Create_summary_results(Summary_dict,patient_folder)

    Cleanup_folder(patient_folder)

    if args.Mute==False:
       print("======================== Succesfully Concluded Inference Script  ======================== ")
