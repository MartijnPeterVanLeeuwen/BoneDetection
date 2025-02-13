import os
import numpy as np
import matplotlib.pyplot as plt
import copy
def Retrieve_label(Path_to_labels,Label_file,Image_size,Label_im,Select_minimal_distance=False,
                            Margin=0,Select_smallest=True,RibFrac=False,Min_threshold=0.5):

    if RibFrac:
        Coordinates_x=Label_file.split("_")[5]
        Coordinates_y=Label_file.split("_")[4]
    else:
        Coordinates_x=Label_file.split("_")[6]
        Coordinates_y=Label_file.split("_")[5]

    Normalised_x_coordinate=int(Coordinates_x)/Image_size[0]
    Normalised_y_coordinate=int(Coordinates_y)/Image_size[1]

    Detected_labels=[]
    Confidence=[]
    Sizes=[]
    Distance_to_centroid=[]
    Masks=[]
    Pixels_in_bbox=[]
    Label_im=Label_im/255
    a=0

    if os.path.isfile(os.path.join(Path_to_labels,Label_file)):

        with open(os.path.join(Path_to_labels,Label_file)) as f:
            Predictions = f.readlines()

        f.close()

        for line in Predictions:

            Detected_mask=np.zeros(Image_size)
            Mask=np.zeros(Image_size)
            Line=line.split(" ")
            Line[-1]=Line[-1][:-1]
            Centroid_x=float(Line[1])
            Centroid_y=float(Line[2])
            Width=float(Line[3])
            Height=float(Line[4])
            Conf=float(Line[5])
            x_min=Centroid_x-0.5*Width
            x_max=Centroid_x+0.5*Width
            y_min=Centroid_y-0.5*Height
            y_max=Centroid_y+0.5*Height

            Mask[int(y_min*Image_size[0]):int(y_max*Image_size[0]),int(x_min*Image_size[1]):int(x_max*Image_size[1])]=1
            Detected_mask[int(y_min*Image_size[0]-Margin):int(y_max*Image_size[0]+Margin),int(x_min*Image_size[1]-Margin):int(x_max*Image_size[1]+Margin)]=1
            Slice_mask=np.array(Label_im>0).astype(int)

            if np.max(Slice_mask+Detected_mask)>1:

                Distance=np.sqrt((Centroid_x-Normalised_x_coordinate)**2+(Centroid_y-Normalised_y_coordinate)**2)
                pixels_in_bbox=len(np.where((Slice_mask+Detected_mask)==2)[0])

                if float(Line[-1])>=Min_threshold:
                    Confidence.append(Line[-1])
                    Detected_labels.append(str(int(Line[0])+1))
                    Distance_to_centroid.append(Distance)
                    Masks.append(Mask)
                    Sizes.append(len(np.nonzero(Mask)[0]))
                    Pixels_in_bbox.append(pixels_in_bbox)

        if Select_minimal_distance and len(Detected_labels)>1:
            Smallest_distance=np.argmin(Distance_to_centroid)
            Confidence=[Confidence[Smallest_distance]]
            Detected_labels=[Detected_labels[Smallest_distance]]

        if Select_smallest and len(Detected_labels)>1:
            smallest_size=np.argmin(Sizes)
            Detected_labels=[Detected_labels[smallest_size]]
            Confidence=[Confidence[smallest_size]]

    TH_confidences=np.ones(len(Confidence))
    return Detected_labels,Confidence,TH_confidences
