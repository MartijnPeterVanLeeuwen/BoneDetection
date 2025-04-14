import os
import sys
import random
from matplotlib import image
import nibabel as nib


Current_directory = os.getcwd()
Main_folder = "/".join(Current_directory.split("/")[0:-2])  # Linux
sys.path.append(Main_folder)

from utils.PreProcessing.Loading_and_saving_data import Data_processing
from utils.Packages_file import *
from Packages_file import *

Functions=Data_processing()
from code_paper.preprocess_TotalSegmentator_scans import Return_label_dict

from SETUPDIR import Set_up_dir
from Create_yaml_file import Create_yaml_file
from Swap_axis import Swap_axis
from Rescale_dimension_scan import Rescale_scan
from Determine_test_split import Determine_data_splittage
from Apply_windowing import Apply_windowing
from Reshape_scan_size import Reshape_scan_size
from Split_patients import Split_patients
from Move_data import Move_patients
from Swap_axis import Swap_axis
from Create_txt_label import Create_txt_label

class PreProcess():

    def __init__(self,Path_to_storage,Path_to_CT_scans,Path_to_Labels,seed=123,Label_values=[1],Resize=False,
                 Patient_nr_index=1,axis="Axial",Manual_patients=None,L=0,W=0):
        self.Path_to_input_Annotation=Path_to_Labels
        self.Path_to_input_CT=Path_to_CT_scans
        self.Validation_fraction=0.1
        self.Test_fraction=0.1
        self.Min_lesion_size=5
        self.Max_hounsfield=2000
        self.Path_to_storage=Path_to_storage
        random.seed(seed)
        self.Path_dictionary=Set_up_dir(Path_to_storage)
        self.Resize=Resize#(768,768)
        self.Label_values=Label_values
        self.Patient_nr_index=Patient_nr_index
        self.min_nr_pixels=5
        self.axis=axis
        self.Manual_patients=Manual_patients
        self.W=W
        self.L=L

    def Extract_positive_patches(self,Train_image_dir,Train_label_dir):

        def load_data (Path_to_CT, Path_to_annoation):

            orginal_data  = nib.load(Path_to_CT).get_fdata()
            label_data  = nib.load(Path_to_annoation).get_fdata()
            Header_data_im=nib.load(Path_to_CT).header
            Header_data_lab=nib.load(Path_to_annoation).header
            pixel_dim=Header_data_im["pixdim"]

            Manual_max=self.L+0.5*W
            Manual_min=self.L-0.5*W

            if self.axis=="Coronal":
                axis=1
            elif self.axis=="Sagital":
                #orginal_data=np.rot90(orginal_data,2,(1,2))
                #label_data=np.rot90(label_data,2,(1,2))
                axis=0

            if self.axis == "Sagital" or self.axis == "Coronal":

                Pixel_dim_im=np.round(Header_data_im["pixdim"],2)
                Pixel_dim_lab=np.round(Header_data_lab["pixdim"],2)

                if (Pixel_dim_im[1:4]==[Pixel_dim_im[1],Pixel_dim_im[1],Pixel_dim_im[1]]).all() and (Pixel_dim_lab[1:4]==[Pixel_dim_lab[1],Pixel_dim_lab[1],Pixel_dim_lab[1]]).all():
                    Rescaled_scan=orginal_data
                    Rescaled_label=label_data
                    rescaled_header=Header_data_im
                else:
                    raise Exception("The dimensions of the scan where not equal, stop preprocessing and implement rescaling")

                Rescaled_scan, Rescaled_label,x = Swap_axis(Rescaled_scan, Rescaled_label, axis=axis,Manual_max=Manual_max,Manual_min=Manual_min)
                orginal_data = Apply_windowing(Rescaled_scan,self.L,self.W, Mute=True)
                label_data=np.round(Rescaled_label)

            else:
                Rescaled_scan, Rescaled_label,x = Swap_axis(orginal_data, label_data, axis=0,Swap=False,Manual_max=Manual_max,Manual_min=Manual_min)
                orginal_data = Apply_windowing(Rescaled_scan,self.L,self.W, Mute=True)
                label_data=np.round(Rescaled_label)


            return orginal_data,label_data

        def regionprops_and_crop (image_data, label_data, Patient_ID ):

            image_data=Reshape_scan_size(image_data,max_size_xy=448,max_size_z=672,Cross_section=self.axis)
            label_data=Reshape_scan_size(label_data,max_size_xy=448,max_size_z=672,Cross_section=self.axis)

            mask=np.zeros(label_data.shape)
            mask[np.where(label_data>0)]=1

            RP_label = label(mask>0)
            regions = regionprops(RP_label)

            All_slices=[]

            for props in regions:
                Slices=list(np.unique(props.coords[:,-1]))
                All_slices+=Slices

            All_slices=np.unique(All_slices)

            for slice_nr in All_slices:
                Approved_lesion_size=False

                for Label_value in Label_values:
                    class_mask=label_data[:,:,slice_nr]==Label_value
                    region_slice=regionprops(label(class_mask))

                    for ii in region_slice:
                        Bounding_box=ii.bbox
                        max_width=Bounding_box[2]-Bounding_box[0]
                        max_height=Bounding_box[3]-Bounding_box[1]
                        if max_width>= self.min_nr_pixels or max_height >=self.min_nr_pixels:
                            Approved_lesion_size=True

                    if Approved_lesion_size:
                        z0_or=int(slice_nr)
                        slice_label = np.array(class_mask>0).astype(int)
                        slice_im = image_data [:,:,z0_or]
                        CCP_region_patch=regionprops(label(slice_label))
                        Approved_size=False
                        Copy_slice_label=copy.copy(slice_label)

                        for lesion in CCP_region_patch:
                            bbox=lesion.bbox
                            lesion_sizes=[bbox[2]-bbox[0],bbox[3]-bbox[1]]

                            if lesion_sizes[0]>=self.min_nr_pixels or lesion_sizes[1]>=self.min_nr_pixels:
                                Approved_size=True
                            else:
                                Copy_slice_label[bbox[0]:bbox[2],bbox[1]:bbox[3]]=0

                        CCP_region_patch=regionprops(label(Copy_slice_label))

                        if Approved_size==True:
                            if f"{Patient_ID}_{z0_or}.png" :
                                image.imsave(os.path.join(Train_image_dir,f"{Patient_ID}_{z0_or}.png"), slice_im, cmap ='gray',vmin=0,vmax=1)
                                Create_txt_label(CCP_region_patch,slice_label.shape ,Train_label_dir, f"{Patient_ID}_{z0_or}.txt",label_value=(Label_value-1))
                                self.Positive_patch_index+=1


        def final_run(label_path, orginal_path):

            Labels=sorted(os.listdir(label_path))
            Patients=sorted(os.listdir(orginal_path))

            if self.Manual_patients!=None:
               Labels=sorted(self.Manual_patients)
               Patients=sorted(self.Manual_patients)

            for i in tqdm(range(len(Labels))):

                Patient_ID="_".join(Patients[i].split(".")[:self.Patient_nr_index])
                print(Patient_ID)
                image_data, label_data = load_data (os.path.join(orginal_path,Patients[i]), os.path.join(label_path,Labels[i]))
                regionprops_and_crop (image_data, label_data, Patient_ID)
            return

        self.Positive_patch_index=0
        final_run(self.Path_to_input_Annotation, self.Path_to_input_CT)


    def Split_lesions(self,Patient_nr_index=0,error_margin=100,Auto_no_patients_based_on_fractions=False,
                     Manual_split=False ):
        if Manual_split:
            Training_patients, Validation_patients, Test_patients=Determine_data_splittage(Manual_split)
        else:
            Training_patients,Validation_patients,Test_patients=Split_patients(self.Path_dictionary,Patient_nr_index=Patient_nr_index,error_margin=error_margin,Auto_no_patients_based_on_fractions=Auto_no_patients_based_on_fractions)
        print(Training_patients)
        Move_patients(self.Path_dictionary, Training_patients, Validation_patients, Test_patients)

        return Training_patients,Validation_patients,Test_patients

Start_preprocessing=True
Split_data=True

axis="Coronal"
Experiment_name="%s_BSv2_v5"%axis
Path_to_yolo_folder="/home/mleeuwen/Deep learning Models/Total_bone_detector/yolov5"
Path_to_input_images="/home/mleeuwen/DATA/TSv3_Selection/Images"
Path_to_input_labels="/home/mleeuwen/DATA/TSv3_Selection/Labels"
Path_to_storage_directory="/home/mleeuwen/Deep learning Models/Total_bone_detector/datasets/%s"%Experiment_name
Path_to_label_txt="/home/mleeuwen/DATA/Totalsegmentator_dataset_v201/Desired_labels.txt"
Path_to_reference_dataset="/home/mleeuwen/Deep learning Models/Total_bone_detector/datasets/Axial_BSv2_v4"

Label_dict=Return_label_dict(Path_to_label_txt)
Label_values=list(Label_dict.values())
Create_yaml_file(Path_to_yolo_folder,Label_dict=Label_dict,name_experiment=Experiment_name)
Patient_nr_index=1

L=400
W=1800

Class=PreProcess(Path_to_storage_directory,Path_to_input_images,Path_to_input_labels,
                 Label_values=Label_values,Resize=False,Patient_nr_index=Patient_nr_index,axis=axis,Manual_patients=None,L=L,W=W)


if Start_preprocessing:
    Class.Extract_positive_patches(Class.Path_dictionary["Im_tr_dir"],Class.Path_dictionary["Lab_tr_dir"])

Patient_nr_index=2
Auto_no_patients_based_on_fractions=True
error_margin=100

if Split_data:

    Patients=Class.Split_lesions(Patient_nr_index,error_margin=error_margin,
                            Auto_no_patients_based_on_fractions=Auto_no_patients_based_on_fractions,
                                Manual_split=Path_to_reference_dataset)

#     Patients=Class.Split_lesions(Patient_nr_index,error_margin=error_margin,
#                              Auto_no_patients_based_on_fractions=Auto_no_patients_based_on_fractions)
#

#
