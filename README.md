# Welcome to the Multiplanar (MP) YOLOv5 Based Bone Identification Method
Welcome to the GitHub page for our multiplanar bone detection method. This GitHub page makes use of the [YOLOv5](https://github.com/ultralytics/yolov5) framework, which we used to train a bone detection and identification method to localize 64 different bones (and costal cartilage) in CT data. Below we will explain what this method can do, and how to get started. If you decide to make use of this method, please cite our paper [link]()
## What can it do for you? 
This method was designed to identify the locations of bone abnormalities such as bone lesions, tumors, or fractures. By providing a segmentation mask in which all the voxels of these abnormalities are annotated, in combination with the corresponding CT scan, we can automatically give the bone in which the abnormalities are located. The bones that can be detected with this method are the following:

- skull
- spine $^1$
- clavicula $^2$
- scapula $^2$
- humeri $^2$
- ribs $^1$ $^1$
- sternum
- sacrum
- hip 
- femur$^2$
- costal cartilage
$^1$: Makes a distinction between bone levels
$^2$: Makes a distinction between left and right

## What do you need? 

## How to get started? 

This GitHub provides the code to run a multiplaner (MP) YOLOv5-based bone detection model. The intended goal behind this code is to identify the bones in which bone abnormalities are located, in a computationally preserving manner. An alternative to this method is using a segmentation method such as the [nnUnet](https://github.com/MIC-DKFZ/nnUNet). In our paper [link]() we have shown that our method is a competitive alternative to nnUnet and since our method is 2D based, it requires less computational resources.

We trained a model on the axial, sagittal, and coronal planes using 3 YOLOv5l models. These were trained on the bone labels of a selection of the [Total Segmentator Dataset](https://github.com/wasserth/TotalSegmentator) CT scans. 

With this code, a bone label can be automatically derived when providing a CT scan in combination with a segmentation mask that indicates the voxels of the bone abnormality. 

![Example_Results](https://github.com/user-attachments/assets/c0578303-38dd-4dc0-be04-b09b631acba3)


