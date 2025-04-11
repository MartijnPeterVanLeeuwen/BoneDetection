#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 09:51:14 2023

@author: mleeuwen
"""
import os 
import random
from tqdm import tqdm
def Split_patients(Path_dictionary,Val_fraction=0.1,Test_fraction=0.1, Auto_no_patients_based_on_fractions=False,
                   No_val_patients=10, No_test_patients=10, error_margin=10,Patient_nr_index=0):

    
    Train_directory_images=Path_dictionary["Im_tr_dir"]
    Val_directory_images=Path_dictionary["Im_val_dir"]
    Test_directory_images=Path_dictionary["Im_test_dir"]
    
    Train_directory_labels=Path_dictionary["Lab_tr_dir"]
    Val_directory_labels=Path_dictionary["Lab_val_dir"]
    Test_directory_labels=Path_dictionary["Lab_test_dir"]
    

    All_training_images=os.listdir(Train_directory_images)
    All_training_labels=os.listdir(Train_directory_labels)
    
    Patients_dict=dict()
    Total_nr_lesions=0
    for i in tqdm(range(len(All_training_labels))):
        #Patient="_".join(All_training_labels[i].split("_")[:Patient_nr_index])
        Patient="_".join(All_training_labels[i].split("_")[:Patient_nr_index])

        with open(os.path.join(Path_dictionary["Lab_tr_dir"],All_training_labels[i]),"r") as f:
                  lines=f.readlines()
        
        if Patient not in list(Patients_dict.keys()):
            Patients_dict[Patient]=len(lines)
        else:
            Patients_dict[Patient]+=len(lines)
        Total_nr_lesions+=len(lines)

    Nr_val_lesions=round(Total_nr_lesions*Val_fraction)
    Nr_test_lesions=round(Total_nr_lesions*Test_fraction)
    
    Patient_nrs=list(Patients_dict.keys())
        
    if Auto_no_patients_based_on_fractions:
        No_test_patients=int(Test_fraction*len(Patient_nrs))
        No_val_patients=int(Val_fraction*len(Patient_nrs))

    Val_patients=[]
    attempt=0
    nr_attempts=100
    Val_lesions=[]
    
    
    while ((Nr_val_lesions-error_margin)<=sum(Val_lesions)<=(Nr_val_lesions+error_margin))==False:
        print("start looking")
        #print((Nr_val_lesions-error_margin),sum(Val_lesions),(Nr_val_lesions+error_margin))
        random_val_patients=random.sample(Patient_nrs,No_val_patients)
        Val_lesions=[Patients_dict[i] for i in random_val_patients]
        attempt+=1
        
        Validation_patients=random_val_patients
    
        if attempt>nr_attempts:
            print("stopped in validation cycle")
            return None
    
    Remaining_patients=[i for i in Patient_nrs if i not in Validation_patients]
    
    attempt=0
    nr_attempts=100
    Test_lesions=[]
    
    while ((Nr_test_lesions-error_margin)<=sum(Test_lesions)<=(Nr_test_lesions+error_margin))==False:
        print("start looking")
        
        random_test_patients=random.sample(Remaining_patients,No_test_patients)
        Test_lesions=[Patients_dict[i] for i in random_test_patients]
        attempt+=1
        
        Test_patients=random_test_patients
    
        if attempt>nr_attempts:
            print("stopped in  test cycle")
            return None
    
    Remaining_training_patients=[i for i in Remaining_patients if i not in Test_patients]
    
    print(sum(Val_lesions),sum(Test_lesions),Total_nr_lesions)

    
    return Remaining_training_patients,Validation_patients,Test_patients
