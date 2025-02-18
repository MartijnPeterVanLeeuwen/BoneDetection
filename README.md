# Welcome to the Multiplanar (MP) YOLOv5 Based Bone Identification Method
Welcome to the GitHub page for our multiplanar bone detection method. This GitHub page makes use of the [YOLOv5](https://github.com/ultralytics/yolov5) framework, which we used to train a bone detection and identification method to localize 64 different bones (and costal cartilage) in CT data. Below we will explain what this method can do, and how to get started. If you decide to make use of this method, please cite our paper [link]()

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

The code is structured so that there is a specific file [paths.json](https://github.com/MartijnPeterVanLeeuwen/BoneDetection/blob/main/paths.json) in which you need to specify the location of a folder that contains the CT scans (*"Path_to_input_CT"*), the folder that contains the segmentation mask (*"Path_to_abnormalities"*) and the directory where you want to results to be outputted to (*"Path_to_storage"*). For the code, both the CT scan and the Abnormality file must have the same name and must be composed in this format: *{PROJECT_ID}_{IMGNR}.nii*, where you use a project ID, followed by an image number. Different file name structures are not supported. An example if shown below. 

```sh
Path_to_input_CT/
├── test_1.nii

Path_to_abnormalities/
├── test_1.nii

Path_to_storage/
├── Experiment 
├── Experiment_1
```

## How to get started? 

This GitHub provides the code to run a multiplaner (MP) YOLOv5-based bone detection model. The intended goal behind this code is to identify the bones in which bone abnormalities are located, in a computationally preserving manner. An alternative to this method is using a segmentation method such as the [nnUnet](https://github.com/MIC-DKFZ/nnUNet). In our paper [link]() we have shown that our method is a competitive alternative to nnUnet and since our method is 2D based, it requires less computational resources.

We trained a model on the axial, sagittal, and coronal planes using 3 YOLOv5l models. These were trained on the bone labels of a selection of the [Total Segmentator Dataset](https://github.com/wasserth/TotalSegmentator) CT scans. 

With this code, a bone label can be automatically derived when providing a CT scan in combination with a segmentation mask that indicates the voxels of the bone abnormality. 

![Example_Results](https://github.com/user-attachments/assets/c0578303-38dd-4dc0-be04-b09b631acba3)


