# Welcome to the Multiplanar (MP) YOLOv5 Bone Identification Method
Welcome to the GitHub page for our multiplanar bone detection method. This GitHub page makes use of the [YOLOv5](https://github.com/ultralytics/yolov5) framework, which we used to train a bone detection and identification method to localize 64 different bones (and costal cartilage) in the axial, coronal and sagittal planes of Computed Tomography (CT) scans. These models were trained on scans and bone labels that originated from a selection of the [Total Segmentator](https://github.com/wasserth/TotalSegmentator) dataset CT scans. 

On this page, we will explain what this method is capable of doing and provide instructions on how you can get started. One of the outputs that this method produces is shown below, which is a plot that indicates different regions that are affected by the provided bone abnormalities.

 If you decide to make use of this method, please cite our paper [link]() (Waiting for publication of proceedings EMBC2025)

![Affected_Bones](https://github.com/user-attachments/assets/d931d1bb-9668-4da4-8730-1b7b68ec0f9e)
![Affected_Bones](https://github.com/user-attachments/assets/c0436b66-c9d5-4e7b-990b-056f6fc0c3de)

## What can this GitHub be used for? 
This method was designed to identify the locations of bone abnormalities such as bone lesions, tumors, or fractures. By providing a segmentation mask in which all the voxels of these abnormalities are annotated, in combination with the corresponding CT scan, we can automatically give the bone in which the abnormalities are located. The bones that can be detected with this method is shown below:

<details>
<summary> Included Bones </summary>

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

The method also provides the exact bone level in which the abnormality is located for the ribs and vertebrae. However, it is less precise when predicting an exact level but much better when estimating a range of 3 bone levels (predicted level + neighboring bone levels). We, therefore, also provide the option to return a range of bone labels for these methods.
</details>

## What do you need to run it? 
To execute this code, you do not need expensive hardware, as you can easily run it on a CPU, although the process is sped up whenever you run it with a GPU. In terms of data, you will need a CT scan in combination with a segmentation mask (of the same size) in which the voxels of a bone abnormality are annotated.  



You will need to specify certain directories in [paths.json](https://github.com/MartijnPeterVanLeeuwen/BoneDetection/blob/main/paths.json) containing the location of a folder that contains the CT scans (```Path_to_input_CT```), the folder that contains the segmentation mask (```Path_to_abnormalities```) and the directory where you want to results to be outputted to (```Path_to_storage```). Both the CT scan and the bone abnormality file must have the same name and must be stored in the following format:
```sh
{PROJECT_ID}_{IMGNR}.nii
```
Below is an example of such a directory structure. Note that other formatting types are not recognized and can, therefore, lead to errors. 

```sh
../Path_to_input_CT/
└── test_1.nii

../Path_to_abnormalities/
└── test_1.nii

../Path_to_storage/
├── Experiment 
├── Experiment_1
├── ...
```

An example of a CT scan and manually created bone abnormality annotations is included in [example_data.zip](https://github.com/MartijnPeterVanLeeuwen/BoneDetection/blob/main/example_data.zip). This is an example scan that was downloaded from the [TotalSegmenator dataset](https://zenodo.org/records/10047292). 

**IMPORTANT**: The code was developed to process images that have a field of view in the x and y direction of 1.5x448=672mm and in the z direction of 1.5x672=1.008mm. When using larger scans as an input, this code will return an error message. Make sure that the sizes of the scans that are inputted do not exceed these field of view values! 

Your data must have the same orientation as the data in the example data for the code to run properly. For instance, when running this data on the [RibFrac](https://ribfrac.grand-challenge.org/), you will need to rotate the input data 180 degrees before running the code, as the orientation of these scans does not align with the orientation that we use in our code. 

## How to run the code on your data
Below you can find instructions on how to install and run the code from this GitHub on your device.

<details open>

<summary>Clone repository and install required packages </summary>

## How to get started? 
To get started with this code, run the following code
```sh
git clone https://github.com/MartijnPeterVanLeeuwen/BoneDetection.git
```
After cloning the git repository, create a new virtual environment in which you can install the required packages. The code was developed with ```python``` version ```3.9```. Using a different version might lead to conflicts between packages, so make sure that the virtual environment runs on this Python version. Upon activating this environment and navigating to the git directory, run the following command to install all the required packages. 
```
pip install -r /Requirements.txt
```

**IMPORTANT**: After installing the packages, you need to clone the [YOLOv5](https://github.com/ultralytics/yolov5) directory into this [folder](https://github.com/MartijnPeterVanLeeuwen/BoneDetection/tree/main/utils/Model). Without this step, the code will not run!

</details>


<details open>

<summary> Run Prediction </summary>

### Run Prediction 
When the git repository has been cloned, the paths file has been updated, and the input files have been stored correctly, the code can be executed. This can be done by running the following command in the command prompt:
```
python Predict.py --Scan_name test_1.nii --Experiment_name Experiment --Device cpu --Slices 5
```
This will start executing the code for scan *"test_1.nii"* and create a folder *"Experiment"* in the *"Path_to_storage"* directory in which all the results will be stored. A description of the other arguments that this function can use is described below: 

<details>

<summary> All Input Arguments </summary>

- ``` --Scan_name ``` :  The name of the scan and the annotation file on which the code will be applied ``` (no Default)```
- ```--Label_name```: The name of the annotation file that contains the labeled bone abnormalities. If this argument is not explicitly called, the label file name is assumed to equal the scan file name (```Default= None```).
- ``` --Experiment_name ``` :  The name of the folder in which all the results will be stored (```Default= Experiment```)
- ``` --Device ``` :  CUDA device, i.e., '0' or '0,1,2,3' or 'cpu' (```Default= cpu```)
- ``` --Slices ``` :  Number of slices per plane on which you want to run the models (```Default= 3```)
- ``` --Rotate_input ``` :  Indicate the number of times the input should be rotated 90 degrees (```Default= 0```)
- ``` --Flip_input ``` : Indicate the axis of the input data that you would like to flip (```Default=False```)
- ``` --IoU ``` :  The maximum IoU used during inference given to the YOLOv5 model (```Default=0.75```)
- ``` --Minimal_TH ``` :  The minimal threshold for the bounding box predictions. Predictions below this threshold are removed (```Default=0.75```)
- ``` --Dont_save_prediction_images ```** : Indicate if you want to remove the prediction PNG images to reduce the memory usage (Action argument, ```Default=False```)
- ``` --No_inference ```** :  Indicate if you do not want to run inference (Action argument, ```Default=False```)
- ``` --Mute ```** :  Indicate if you want to mute the printing of statements during inference (Action argument, ```Default=False```)
- ``` --Remove_2D_bone_overview ```** :  Indicate if you do not want to create the "Affected_Bones.PNG" image  (Action argument, ```Default=False```)
- ```--Finalize_inference"```**: If you do not want to tweak any parameters, these parameters will remove all files that are not needed anymore. (Action argument, ```Default=False```)
- ``` --Switch_left_right```** : Indicate if you want to switch the orientation of left and right. (Action argument, ```Default=False```)
- ```--Mute_text_in_plot```** : Can be used to remove all plotting in the ```Affected_Bones.PNG``` (Action argument, ```Default=False```)
- ```--Reduce_labels```**: Removes the level of the vertebrae and rib labels in the ```Summary.xlsx``` file and gives all abnormalities in the spine and ribs a value of ```100``` and ```101``` in the  ```Labeld_annotation_file.nii```(Action argument, ```Default=False```)

** = To put these arguments in effect, simply add them as arguments to the input data

Note that if you run this code multiple times, it will create new folders called ```Experiment_x``` with x going up to 10 to prevent overwriting previous results. 
</details>

</details>

<details>

<summary>Change post-processing parameters </summary>

### Change prediction parameters without running inference
If you have already run the bone detection models but would like to change the post-processing parameters, such as ```--IoU ``` of ```--Minimal_TH ```, you can do so by adding the following inputs:
```
python Predict.py --Scan_name test_1.nii --Experiment_name Experiment --No_inference --IoU 0.5 --Minimal_TH 0.5

```
In this example, the results from the folder ```Experiment``` are used, only now an ```--IoU``` of ```0.5``` and ```--Minimal_TH```of ```0.5``` is used. Make sure that you use the correct ```--Experiment_name``` file. This is ofcourse not necessary, but it illustrates that you can rerun the code without needing to rerun all the predictions. 

</details>

## Output
The code creates a folder containing several results. This section will discuss what these outputs mean so that you can extract the information you need from the results. The code creates 3 folders and 3 files as shown below
```
../Path_to_storage/Experiment
├── Annotation_info
├── Lesions
├── Prediction_yolo
├── Affected_Bones.PNG
├── Labeled_annotation_file.nii
├── Summary.xlsx
└── YOLOV5_Output.txt

```
- ```Affected_Bones.PNG ``` : This is a visualization of the location of the bone abnormalities. Two examples of such images are shown at the top of this page. This file is generated by using the [```Bone_atlas.nii```](https://github.com/MartijnPeterVanLeeuwen/BoneDetection/blob/main/Bone_atlas.nii) file, which is a bone mask created by using bone labels from the TotalSegmentator dataset. Note that this is a generic bone mask, so it is not a visualization of the patient scan that was given as input but is merely used to indicate the location of the affected bones. Orange regions in this plot indicate the neighboring bones of the predicted rib or vertebra levels.
-  ```Labeled_annotation_file.nii```: This file contains the original abnormality annotations, only now the voxel values represent the bone in which the abnormality is located.
- ``` Summary.xlsx ``` : This file contains a summary of the findings. It indicates the final label of the bone abnormalities, and provides the integer value used to mark this location in the ```Labelled_annotation_file.nii```.
-  ```YOLOV5_Output.txt ``` : This file stores the output created by YOLOv5

The content of the other folders can be found below.
<details>

<summary>Annotation_info </summary>

### Annotation_info
```
../Annotation_info
├── Segmentation_masks─────────────────────├──Labels_Axial─────── ├── 1_1_-1_test_1_x_y_z.png
├── Lesion_centroids.json                  ├──Labels_Coronal      ├── 1_1_0_test_1_x_y_z.png
└── Transformed_Lesion_centroids.xlsx      └──Labels_Sagital      ├── 1_1_1_test_1_x_y_z.png
                                                                  ├── 2_1_-1_test_1_x_y_z.png
                                                                  ├── ...
```
- ```Lesion_centroids.json ``` : Centroid of each lesion in the annotation file after rotating and flipping.
- ```Transformed_Lesion_centroids.xlsx ``` :  Centroids of the lesions after applying scaling, rotation, and flipping (if necessary).  
- ```Segmentation_masks ``` : This folder contains images of the annotation masks of the bone abnormalities. These are used to determine what bounding box overlaps with the annotated bone abnormality.

The ground truth images are structured in a certain format:   ```1_1_-1_test_1_x_y_z.png``` The first number describes the lesion number, and the second shows the integer value that belongs to the annotation mask. The ```-1``` refers to the relative position of the slice to the centroid of the bone lesion. The  ```x```,  ```y```, and ```z``` values indicate the scaled coordinates of the annotation in the input scan.

</details>

<details>

<summary>Prediction_yolo </summary>

### Prediction_yolo
```
../Prediction_yolo
├── Axial ────── ├── labels────────────────────────├── 1_1_-1_test_1_x_y_z.txt
├── Coronal      ├── 1_1_-1_test_1_x_y_z.png       ├── 1_1_0_test_1_x_y_z.txt
└── Sagital      ├── 1_1_0_test_1_x_y_z.png        ├── 1_1_1_test_1_x_y_z.txt
                 ├── 1_1_1_test_1_x_y_z.png        ├── 2_1_-1_test_1_x_y_z.txt  
                 ├── 2_1_-1_test_1_x_y_z.png       ├── ...  
                 ├── ...
```  
This folder contains the raw YOLOv5 output, including the prediction images and the label files describing the bounding boxes' location and label. These outputs are included for each plane. If you do not want to have the PNG images stored, use the ``` --Dont_save_prediction_images ``` command when running the code.

</details>

<details>

<summary>Lesions </summary>

### Lesions
```
../Lesions
├── Lesion_1_1 ────── ├── Dataframe_Axial.xlsx
├── Lesion_2_1        ├── Dataframe_Coronal.xlsx
├── ...               └── Dataframe_Sagital.xlsx

```
This folder contains a separate folder for each lesion in the annotation file. These folders contain ```.xlsx``` files with the selected bone label for each input image, including the outputted probability by YOLOv5. This is done for all 3 planes.

</details>


