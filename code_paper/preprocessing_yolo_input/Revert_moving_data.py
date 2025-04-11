#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 09:46:35 2023

@author: mleeuwen
"""
import os 

def Revert_moving_Data(Directory_dictionary):
    
    Train_dir_im=Directory_dictionary["Im_tr_dir"]
    Train_dir_lab=Directory_dictionary["Lab_tr_dir"]
    
    Path_to_validation_im=Directory_dictionary["Im_val_dir"]
    Path_to_test_im=Directory_dictionary["Im_test_dir"]

    Path_to_validation_lab=Directory_dictionary["Lab_val_dir"]
    Path_to_test_lab=Directory_dictionary["Lab_test_dir"]
    
    Validation_images=os.listdir(Path_to_validation_im)
    Validataion_labels=os.listdir(Path_to_validation_lab)
    
    Test_images=os.listdir(Path_to_test_im)
    Test_labels=os.listdir(Path_to_test_lab)
    
    print("Start moving validation data")
    print(len(Validation_images))
    for i in Validation_images:
        old_dir=os.path.join(Path_to_validation_im,i)
        new_dir=os.path.join(Train_dir_im,i)
        os.rename(old_dir, new_dir)
        
    for i in Validataion_labels:
        old_dir=os.path.join(Path_to_validation_lab,i)
        new_dir=os.path.join(Train_dir_lab,i)
        os.rename(old_dir, new_dir)
        
        
    print("Start moving test data")
    print(len(Test_images))
    for i in Test_images:
        old_dir=os.path.join(Path_to_test_im,i)
        new_dir=os.path.join(Train_dir_im,i)
        os.rename(old_dir, new_dir)
        
    for i in Test_labels:
        old_dir=os.path.join(Path_to_test_lab,i)
        new_dir=os.path.join(Train_dir_lab,i)
        os.rename(old_dir, new_dir)

    print("Training data has %s images and %s labels"%(len(os.listdir(Train_dir_im)),len(os.listdir(Train_dir_lab))))  

    return None


