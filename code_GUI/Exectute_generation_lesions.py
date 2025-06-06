
import sys
import os
cwd="\\".join(os.getcwd().split('\\')[:-1])
sys.path.append(cwd)
import numpy as np
from code_paper.preprocess_TotalSegmentator_scans.generate_synthetic_lesion.Create_synthetic_lesions import Create_sphere_coords



def Create_sphere(class_attribute,list_of_coordinates_code,list_of_coordinates_gui):

        Annotation_file_gui=np.zeros(class_attribute.ct_data.shape)
        Annotation_file_script=np.zeros(class_attribute.ct_data.shape)

        for i in range(len(list_of_coordinates_code)):
             coordinate=list_of_coordinates_code[i]
             raw_coordiante_list=list_of_coordinates_gui[i]
             Annotation_file_gui=Create_sphere_coords(Annotation_file_gui,coordinate[0],coordinate[1],coordinate[2], np.ceil(10/1.5).astype(int), resolution=20)
             Annotation_file_script=Create_sphere_coords(Annotation_file_script,raw_coordiante_list[0],raw_coordiante_list[2],raw_coordiante_list[1], np.ceil(10/1.5).astype(int), resolution=20)

        return Annotation_file_gui,Annotation_file_script
