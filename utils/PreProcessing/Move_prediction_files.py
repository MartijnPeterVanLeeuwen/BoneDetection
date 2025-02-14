import os
import sys
import shutil

def Move_prediction_files(Path_to_predictions,Folder_names,Target_directory):

    for i in Folder_names:

        old_path=os.path.join(Path_to_predictions,i)

        new_folder=i.split("_")[-1]

        new_path=os.path.join(Target_directory,i)

        shutil.move(old_path,new_path)

        old_name=new_path

        new_name=os.path.join(new_path,new_folder)
        os.rename(os.path.join(Target_directory,i),os.path.join(Target_directory,new_folder))

    return None
