
# Welcome to the Multiplanar (MP) YOLOv5 Based Bone Identification Method
Welcome to the GitHub page for our multiplanar bone detection method. This GitHub page makes use of the [YOLOv5](https://github.com/ultralytics/yolov5) framework, which we used to train a bone detection and identification method to localize 64 different bones (and costal cartilage) in the axial, coronal and sagittal planes of Computed Tomography (CT) scans. These models were trained on scans and bone labels that originated from a selection of the [Total Segmentator](https://github.com/wasserth/TotalSegmentator) dataset CT scans. Below we will explain what this method can do, and how to get started. If you decide to make use of this method, please cite our paper [link]() 

## What can this GitHub be used for? 
This method was designed to identify the locations of bone abnormalities such as bone lesions, tumors, or fractures. By providing a segmentation mask in which all the voxels of these abnormalities are annotated, in combination with the corresponding CT scan, we can automatically give the bone in which the abnormalities are located. The bones that can be detected with this method are the following:

- Skull
- Spine $^1$
- Clavicula $^2$
- Scapula $^2$
- Humeri $^2$
- Ribs $^1$ $^2$
- Sternum
- Sacrum
- Hip 
- Femur $^2$ 
- Costal cartilage
  
$^1$: Makes a distinction between bone levels,
$^2$: Makes a distinction between left and right

For the ribs and the vertebrae, the method also provides the exact bone level in which the abnormality is located. However, the method is less precise when predicting an exact level, but is much better when estimating a range of 3 bone levels (predicted level + neighboring bone levels). We therefore also provide the option to return a range of bone labels for these methods.

## What do you need to run it? 
Not much is the answer! To execute this code, you do not need expensive hardware, as you can run it on your laptop. However, the process is of course sped up whenever you run it with a GPU. In terms of data, you will need a CT scan in combination with a segmentation mask (of the same size) in which the voxels of the bone abnormality are annotated. 

You will need to specify certain directories in [paths.json](https://github.com/MartijnPeterVanLeeuwen/BoneDetection/blob/main/paths.json) containing the location of a folder that contains the CT scans (*"Path_to_input_CT"*), the folder that contains the segmentation mask (*"Path_to_abnormalities"*) and the directory where you want to results to be outputted to (*"Path_to_storage"*). Both the CT scan and the bone abnormality file must have the same name and must be stored in the following format:
```sh
{PROJECT_ID}_{IMGNR}.nii
```
An example of how such a directory structure looks like is shown below. Note that other formatting types are not recognized and can therefore lead to errors. 

```sh
../Path_to_input_CT/
├── test_1.nii

../Path_to_abnormalities/
├── test_1.nii

../Path_to_storage/
├── Experiment 
├── Experiment_1
├── ...
```

An example of a CT scan and manually created bone abnormality annotations are included in [example_data.zip](https://github.com/MartijnPeterVanLeeuwen/BoneDetection/blob/main/example_data.zip) This is an example scan that was downloaded from the [TotalSegmenator dataset](https://zenodo.org/records/10047292)

Your data must have the same orientation as the data in the example data for the code to properly run. For instance, when running this data on the [RibFrac](https://ribfrac.grand-challenge.org/) you will need to rotate the input data 180 degrees before running the code as the orientation of these scans does not align with the orientation that we use in our code. 


## How to get started? 
To get started with this code, run the following code
```sh
git clone https://github.com/MartijnPeterVanLeeuwen/BoneDetection.git
```
After cloning the git repository, create a new virtual environment in which you can install the required packages. Upon activating this environment and navigating to the git directory, run the following command. 
```
pip install -r /Requirements.txt

```
This will install all the required packages. Note that you do not have to separately download the YOLOv5 directory, we have included it in Github in this [folder](https://github.com/MartijnPeterVanLeeuwen/BoneDetection/tree/main/utils/Model). This code was directly downloaded from the original [YOLOv5](https://github.com/ultralytics/yolov5) GitHub page.

When the git repository has been cloned, the paths file has been updated, and the input files have been stored correctly, the code can be executed. This can be done by running the following command in the command prompt:
```
python Predict.py --Scan_name test_1.nii --Experiment_name Experiment --Device cpu --Slices 5
```
This will start executing the code for scan *"test_1.nii"* and create a folder *"Experiment"* in the *"Path_to_storage"* directory in which all the results will be stored. A description of the other arguments that this function can use are described below: 

- ``` --Scan_name ```-> The name of the scan and the annotation file on which the code will be applied ``` (no Default)``` 
- ``` --Experiment_name ```-> The name of the folder in which all the results will be stored (```Default= Experiment```)
- ``` --Device ```-> CUDA device, i.e., '0' or '0,1,2,3' or 'cpu' (```Default= cpu```)
- ``` --Slices ```-> Number of slices per plane on which you want to run the models (```Default= 3```)
- ``` --Rotate_input ```-> Indicate the number of times the input should be rotated 90 degrees (```Default= 0```)
- ``` --Flip_input ```*->Indicate if you want to flip the input data around the 0 axis (Action argument, ```Default=False```)
- ``` --IoU ```-> The maximum IoU used during inference given to the YOLOv5 model (```Default=0.75```)
- ``` --Minimal_TH ```-> The minimal threshold for the bounding box predictions. Predictions below this threshold are removed (```Default=0.75```)
- ``` --Use_existing_folder ```*->Indicate if you want to run the code in an existing folder, or if you want to create a new folder. (Action argument, ```Default=False```)
- ``` --Dont_save_prediction_images ```*->Indicate if you want to remove the prediction PNG images to reduce the memory usage (Action argument, ```Default=False```)
- ``` --No_inference ```*-> Indicate if you do not want to run inference (Action argument, ```Default=False```)
- ``` --Mute ```*-> Indicate if you want to mute the printing of statements during inference (Action argument, ```Default=False```)
- ``` --Remove_2D_bone_overview ```*-> Indicate if you do not want to create the "Affected_Bones.PNG" image  (Action argument, ```Default=False```)

** = To put these arguments in effect, simply add them as arguments to the input data
