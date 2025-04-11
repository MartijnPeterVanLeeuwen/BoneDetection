#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 14:40:20 2023

@author: mleeuwen
"""

import numpy as np
from skimage.measure import regionprops, label
import os 


def Create_txt_label(Region,Original_dim,Storage_folder,file_name,label_value=0):
    
    mode="w"
    if os.path.isfile(os.path.join(Storage_folder,file_name))==True:
        mode="a"

    
    with open(os.path.join(Storage_folder,file_name),mode) as f:

        for lesion in Region:
            scaled_center_y=(lesion.bbox[0]+0.5*(lesion.bbox[2]-lesion.bbox[0]))/Original_dim[1]
            scaled_center_x=(lesion.bbox[1]+0.5*(lesion.bbox[3]-lesion.bbox[1]))/Original_dim[0]

            scaled_width=(lesion.bbox[3]-lesion.bbox[1])/Original_dim[1]
            scaled_height=(lesion.bbox[2]-lesion.bbox[0])/Original_dim[0]
            
            
            f.write("%s %s %s %s %s\n"%(label_value,scaled_center_x,scaled_center_y,scaled_width,scaled_height))
    
    f.close()
    
    return None
