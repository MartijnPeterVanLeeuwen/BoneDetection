import os
import sys
import pandas as pd

def Report_prediction_results(class_structure,path_to_results="C:\\Users\\mleeuwen\\Demo"):

    Path_to_summary=os.path.join(path_to_results,'%s\\Summary.xlsx'%(class_structure.Experiment_name))

    result_dataframe=pd.read_excel(Path_to_summary)

    list_of_coordinates_lesion_GUI=class_structure.Annotation_coords_match

    list_of_annotations=class_structure.annotations_raw

    for i in range(result_dataframe.shape[0]):

       label=result_dataframe.iloc[i,4]
       x_coord=result_dataframe.iloc[i,1]
       y_coord=result_dataframe.iloc[i,2]
       z_coord=result_dataframe.iloc[i,3]

       for z in range(len(list_of_coordinates_lesion_GUI)):

            coord=list_of_coordinates_lesion_GUI[z]
            difference_x=abs(coord[2]-x_coord)
            difference_y=abs(coord[1]-y_coord)
            difference_z=abs(coord[0]-z_coord)

            if difference_x<2 and difference_y<2 and difference_z<2:

                 index = z  #
                 item_id = class_structure.annotation_ids[index]
                 old_values = class_structure.tree.item(item_id, "values")

                 # Create new tuple with updated ground truth (column 1)
                 new_values = (old_values[0], old_values[1], label)
                 class_structure.tree.item(item_id, values=new_values)


    return None
