#Multiplanar (MP) YOLOv5 based bone identification method
This GitHub provides the code to run a multiplaner (MP) YOLOv5-based bone detection model. The intended goal behind this code is to identify the bones in which bone abnormalities are located, in a computationally preserving manner. An alternative to this method is using a segmentation method such as the [nnUnet](https://github.com/MIC-DKFZ/nnUNet). In our paper [link]() we have shown that this method, and since this method is 2D based, it is possibly less computationally expensive. 

We trained a model on the axial, sagittal, and coronal planes using 3 YOLOv5l models. These were trained on the bone labels of a selection of the [Total Segmentator Dataset](https://github.com/wasserth/TotalSegmentator) CT scans. 

With this code, a bone label can be automatically derived when providing a CT scan in combination with a segmentation mask that indicates the voxels of the bone abnormality. 

Documentation on this GitHub's code can be found via this [link](https://github.com/MartijnPeterVanLeeuwen/BoneDetection/blob/main/documentation)

![Example_Results](https://github.com/user-attachments/assets/c0578303-38dd-4dc0-be04-b09b631acba3)


