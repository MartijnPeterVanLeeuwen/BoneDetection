This GitHub provides the code to run a multiplaner (MP) YOLOv5-based bone detection model. This code is designed to identify the bones in which bone abnormalities are located.

We trained a model on the axial, sagittal, and coronal planes using 3 YOLOv5l models. These were trained on the bone labels of a selection of the [Total Segmentator Dataset](https://github.com/wasserth/TotalSegmentator) CT scans. 

With this code, a bone label can be automatically derived when providing a CT scan in combination with a segmentation mask that indicates the voxels of the bone abnormality. 

![Example_Results](https://github.com/user-attachments/assets/c0578303-38dd-4dc0-be04-b09b631acba3)
