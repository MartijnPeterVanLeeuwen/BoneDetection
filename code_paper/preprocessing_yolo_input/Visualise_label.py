from PIL import Image

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from numpy import asarray
import random
def Create_plot(Path_to_image,Path_to_label,Save_dir):

    im_frame = Image.open(Path_to_image)
    np_frame = asarray(im_frame)
    f = open(Path_to_label, "r")
    label_file=f.readlines()
    plt.figure()
    plt.imshow(np_frame)
    Color_dict={}

    for i in label_file:

        line=i.split(" ")

        centroid_x=np.array(line[1]).astype(float)*np_frame.shape[0]
        centroid_y=np.array(line[2]).astype(float)*np_frame.shape[1]
        width=np.array(line[3]).astype(float)*np_frame.shape[0]
        height=np.array(line[4][:-2]).astype(float)*np_frame.shape[1]
        print(centroid_x,centroid_y,width,height,height)
        class_nr= int(np.array(line[0]).astype(float))

        if class_nr not in list(Color_dict.keys()):
            color = 0
            Search_color=True
            while Search_color:
                if color not in list(Color_dict.values()):
                    color = ["#"+''.join([random.choice('0123456789ABCDEF') for i in range(6)])][0]
                    Color_dict[int(class_nr)] = color
                    Search_color=False
        else:
            color=  Color_dict[int(class_nr)]
        print(color)

        plt.plot(centroid_x,centroid_y,c=color)

        plt.plot([centroid_x-(0.5*width),centroid_x+0.5*width],[centroid_y+(0.5*height),centroid_y+(0.5*height)],c=color)
        plt.plot([centroid_x-(0.5*width),centroid_x+0.5*width],[centroid_y-(0.5*height),centroid_y-(0.5*height)],c=color)
        plt.plot([centroid_x-(0.5*width),centroid_x-0.5*width],[centroid_y-(0.5*height),centroid_y+(0.5*height)],c=color)
        plt.plot([centroid_x+(0.5*width),centroid_x+0.5*width],[centroid_y-(0.5*height),centroid_y+(0.5*height)],c=color)


    plt.savefig(os.path.join(Save_dir,"test.png"))
    return None

model="Coronal_BSv2"
Save_dir="/home/mleeuwen/Deep learning Models/Total_bone_detector/datasets/"
Path_to_scans="/home/mleeuwen/Deep learning Models/Total_bone_detector/datasets/%s/train/images"%model

images=os.listdir(Path_to_scans)
print(len(images))
print(images)
image="Scan_0252_100"
Path_to_image="/home/mleeuwen/Deep learning Models/Total_bone_detector/datasets/%s/train/images/%s.png"%(model,image)
Path_to_label="/home/mleeuwen/Deep learning Models/Total_bone_detector/datasets/%s/train/labels/%s.txt"%(model,image)

Create_plot(Path_to_image,Path_to_label,Save_dir)
