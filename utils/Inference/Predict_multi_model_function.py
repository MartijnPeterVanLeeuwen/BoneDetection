import os
import sys
import nibabel as nib
import matplotlib.pyplot as plt
import shutil
from scipy import ndimage
Current_directory = os.getcwd()
Main_folder = "/".join(Current_directory.split("/")[0:-2])  # Linux

from utils.Packages_file import *
from utils.PreProcessing.Swap_axis import Swap_axis
from utils.PreProcessing.Rescale_scan import Rescale_scan
from utils.PreProcessing.Loading_and_saving_data import Data_processing
from utils.PreProcessing.Apply_windowing import Apply_windowing
from utils.PreProcessing.Check_size_yolo_im import Check_size_yolo_im
from utils.PreProcessing.Place_in_empty_vol import *
from utils.PreProcessing.Move_prediction_files import Move_prediction_files
from matplotlib import image
Functions=Data_processing()

def Predict_multi_model_function(Path_to_CT,Path_to_Lesion_label,Name_scan,Path_to_yolo_folder,Patient_ID,Path_to_main_folder,Path_to_weights,
                                 Total_number_of_slices=3,GPU=0,L=400,W=1800,Min_size_im=548,Max_size_im=757,
                                rotation=False,flip=False,IOU_threshold=0.45,MODELS=["Axial","Sagital","Coronal"],
                                Dont_save_prediction_images=False):

    Path_to_storage=os.path.join(Path_to_yolo_folder,"Temporary_input")

    if os.path.isdir(Path_to_storage)==True:
        shutil.rmtree(Path_to_storage)

    Path_to_yaml=os.path.join(Path_to_yolo_folder,"data/Axial_FINAL.yaml")

    Path_to_lesion_centroids=os.path.join(Path_to_main_folder,"Transformed_Lesion_centroids.xlsx")

    if os.path.isdir(Path_to_storage)==False:
        os.mkdir(Path_to_storage)

    Model_Names=["Axial","Sagital","Coronal"]

    Patient_result_folder=os.path.join(Path_to_storage,Name_scan.split(".")[0])

    if os.path.isdir(Patient_result_folder)==False:
        os.mkdir(Patient_result_folder)

    Lesion_centroid_dataframe=pd.read_excel(Path_to_lesion_centroids)
    Additional_slices=int(np.floor(Total_number_of_slices/2))

    for model_nr in range(len(MODELS)):

        MODEL_NR=MODELS[model_nr]

        Crossection_folder=os.path.join(Patient_result_folder,Model_Names[model_nr])
        Path_to_label_folder = os.path.join(Path_to_main_folder, "Labels_%s"%Model_Names[model_nr])

        if os.path.isdir(Path_to_label_folder) == False:
            os.mkdir(Path_to_label_folder)

        Image, Header = Functions.Loading_Nifti_data(Path_to_CT, Name_scan, Mute=True, Resize=False)
        Label,Header= Functions.Loading_Nifti_data(Path_to_Lesion_label, Name_scan,Mute=True,Resize=False)

        if rotation!=False:
            Image = [np.rot90(Image[0], rotation)]
            Label = [np.rot90(Label[0], rotation)]

        if flip!=False:
            Image = [np.flip(Image[0], flip)]
            Label = [np.flip(Label[0], flip)]

        Header = Header[0]
        pixdim_array = Header["pixdim"]

        Image = [Rescale_scan(Image[0], pixdim_array, rescale_to=1.5, Mute=True)]
        Label = [Rescale_scan(Label[0], pixdim_array, rescale_to=1.5, Mute=True)]

        if os.path.isdir(Crossection_folder)==False:
            Input_size = 448

            os.mkdir(Crossection_folder)

            Manual_max = L + 0.5 * W
            Manual_min = L - 0.5 * W
            axis=0
            Swapstatus=False

            Centroid_column="Scaled_centroid_z"
            diff_x = int((448 - Image[0].shape[0]) / 2)
            diff_y = int((448 - Image[0].shape[1]) / 2)
            diff_z = int((672 - Image[0].shape[-1]) / 2)

            x = np.array(Lesion_centroid_dataframe["Scaled_centroid_x"])+diff_x
            y = np.array(Lesion_centroid_dataframe["Scaled_centroid_y"])+diff_y
            z = np.array(Lesion_centroid_dataframe["Scaled_centroid_z"])+diff_z
            label_lesion = list(Lesion_centroid_dataframe["Label"])
            iD_lesion = list(Lesion_centroid_dataframe["Lesion_ID"])

            Coordinates = list(z)

            if Model_Names[model_nr]=="Coronal":
                Input_size = 672

                axis=1
                Swapstatus=True
                Centroid_column = "Scaled_centroid_y"
                diff_x = int((672 - Image[0].shape[0]) / 2)
                diff_y = int((448 - Image[0].shape[1]) / 2)
                diff_z = int((672 - Image[0].shape[-1]) / 2)

                x = np.array(Lesion_centroid_dataframe["Scaled_centroid_x"])+diff_x
                y = np.array(Lesion_centroid_dataframe["Scaled_centroid_z"])+diff_z
                z = np.array(Lesion_centroid_dataframe["Scaled_centroid_y"])+diff_y
                label_lesion = list(Lesion_centroid_dataframe["Label"])
                iD_lesion=list(Lesion_centroid_dataframe["Lesion_ID"])
                Coordinates=list(z)

            if Model_Names[model_nr]=="Sagital":
                Input_size = 672
                axis=0
                Swapstatus=True
                Centroid_column = "Scaled_centroid_x"
                diff_x = int((448 - Image[0].shape[0]) / 2)
                diff_y = int((672 - Image[0].shape[1]) / 2)
                diff_z = int((672 - Image[0].shape[-1]) / 2)

                x = np.array(Lesion_centroid_dataframe["Scaled_centroid_z"])+diff_z
                y = np.array(Lesion_centroid_dataframe["Scaled_centroid_y"])+diff_y
                z = np.array(Lesion_centroid_dataframe["Scaled_centroid_x"])+diff_x
                label_lesion = list(np.round(Lesion_centroid_dataframe["Label"]))
                iD_lesion=list(Lesion_centroid_dataframe["Lesion_ID"])

                Coordinates=list(z)

            Windowed_data,ignore1,ignore2=Swap_axis(Image[0],Image[0],axis=axis,Swap=Swapstatus,Manual_max=Manual_max,Manual_min=Manual_min)
            Label,ignore1,ignore2=Swap_axis(Label[0],Label[0],axis=axis,Swap=Swapstatus,Manual_max=Manual_max,Manual_min=Manual_min)

            Windowed_data=Apply_windowing(Windowed_data,L=L,W=W,Mute=True)

            Windowed_data=Place_in_empty_vol(Windowed_data, max_size_xy=448, max_size_z=672, Cross_section=Model_Names[model_nr])
            Label=[Place_in_empty_vol(Label, max_size_xy=448, max_size_z=672, Cross_section=Model_Names[model_nr])]
            Normalised_im=[Windowed_data]

            lesion=0
            location_indeces=range(-int(Additional_slices),int(Additional_slices+1))
            coordinate=0

            for i in Coordinates:
                current_location_index = 0

                for ii in range(int(i-Additional_slices),int(i+Additional_slices+1)):

                    if ii < Normalised_im[0].shape[-1] and ii>0:

                        location_index=location_indeces[current_location_index]
                        z=ii
                        Slice=Normalised_im[0][:,:,int(ii)]

                        x_value=x[lesion]
                        y_value=y[lesion]
                        label_lesion[coordinate]=np.round(label_lesion[coordinate]).astype(int)
                        Selectected_label = copy.copy(np.round(Label[0][:, :, ii]))

                        Empty_label_slice=np.zeros(Selectected_label.shape)
                        Empty_label_slice[np.where(Selectected_label==np.round(label_lesion[coordinate]).astype(int))]=1

                        image.imsave(os.path.join(Crossection_folder,"%s_%s_%s_%s_%s_%s_%s.png"%(lesion+1,label_lesion[coordinate],location_index,Patient_ID,int(x_value),int(y_value),z)),Slice,cmap="gray",vmin=0,vmax=1)
                        image.imsave(os.path.join(Path_to_label_folder,"%s_%s_%s_%s_%s_%s_%s.png"%(lesion+1,label_lesion[coordinate],location_index,Patient_ID,int(x_value),int(y_value),z)),Empty_label_slice,cmap="gray",vmin=0,vmax=1)
                    current_location_index+=1
                coordinate+=1
                lesion+=1

        sys.path.append(Path_to_yolo_folder)
        Path_to_model_weights=os.path.join(Path_to_weights,"%s/best.pt"%Model_Names[model_nr])
        os.chdir(Path_to_yolo_folder)
        Path_to_input_patients="Temporary_input/%s/%s/"%(Name_scan.split(".")[0],Model_Names[model_nr])
        Experiment_name="Predictions_%s_%s"%(Name_scan.split(".")[0],Model_Names[model_nr])
        Input_yolo=Input_size

        Inputs_for_subprocess=["python", "detect.py", "--data", str(Path_to_yaml), "--weights", str(Path_to_model_weights), "--iou-thres", str(IOU_threshold),
             "--source", str(Path_to_input_patients),  "--imgsz", str(Input_yolo), "--device", str(GPU), "--save-txt" ,"--line-thickness", "1", "--hide-conf",
              "--name", str(Experiment_name), "--save-conf"]

        if Dont_save_prediction_images==True:
            Inputs_for_subprocess.append('--nosave')

        with open(os.path.join(Path_to_main_folder,"YOLOv5_Output.txt"), "a") as f:

            subprocess.run(Inputs_for_subprocess,stdout=f, stderr=f)

        f.close()

    Path_to_prediction=os.path.join(Path_to_yolo_folder,'runs')
    Path_to_prediction=os.path.join(Path_to_prediction,'detect')
    Path_to_prediction_destination=os.path.join(Path_to_main_folder,"Prediction_yolo")

    if os.path.isdir(Path_to_prediction_destination)==False:
        os.mkdir(Path_to_prediction_destination)

    Move_prediction_files(Path_to_prediction,["Predictions_%s_Axial"%Name_scan.split(".")[0],"Predictions_%s_Sagital"%Name_scan.split(".")[0],"Predictions_%s_Coronal"%Name_scan.split(".")[0]],Path_to_prediction_destination)

    shutil.rmtree(Path_to_storage)
    #shutil.rmtree(Path_to_prediction)


