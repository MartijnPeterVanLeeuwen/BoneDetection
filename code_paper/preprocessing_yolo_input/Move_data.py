#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 11:30:32 2023

@author: mleeuwen
"""
import os 


def Move_patients(Path_directory,Training_patients,Validation_patients,Test_patients,):

    All_im_files=os.listdir(Path_directory["Im_tr_dir"])    
    All_lab_files=os.listdir(Path_directory["Lab_tr_dir"])    

    Val_file_names_im=[]
    for i in Validation_patients:
        Val_file_names_im+=[ii for ii in All_im_files if i in ii]
    
    Test_file_names_im=[]   
    for i in Test_patients:
        Test_file_names_im+=[ii for ii in All_im_files if i in ii]
     
    Val_file_names_lab=[]
    for i in Validation_patients:
        Val_file_names_lab+=[ii for ii in All_lab_files if i in ii]
    
    Test_file_names_lab=[]   
    for i in Test_patients:
        Test_file_names_lab+=[ii for ii in All_lab_files if i in ii]
     
    print(len(Val_file_names_im),len(Test_file_names_im),len(Val_file_names_lab),len(Test_file_names_lab))
    
    for i in range(len(Val_file_names_im)):
        old_path_image=os.path.join(Path_directory["Im_tr_dir"],Val_file_names_im[i])
        new_path_image=os.path.join(Path_directory["Im_val_dir"],Val_file_names_im[i])
        old_path_label=os.path.join(Path_directory["Lab_tr_dir"],Val_file_names_lab[i])
        new_path_label=os.path.join(Path_directory["Lab_val_dir"],Val_file_names_lab[i])
        os.rename(old_path_image, new_path_image)
        os.rename(old_path_label, new_path_label)
    
    for i in range(len(Test_file_names_im)):
        old_path_image=os.path.join(Path_directory["Im_tr_dir"],Test_file_names_im[i])
        new_path_image=os.path.join(Path_directory["Im_test_dir"],Test_file_names_im[i])
        old_path_label=os.path.join(Path_directory["Lab_tr_dir"],Test_file_names_lab[i])
        new_path_label=os.path.join(Path_directory["Lab_test_dir"],Test_file_names_lab[i])
        os.rename(old_path_image, new_path_image)
        os.rename(old_path_label, new_path_label)


    
    
    
    return None