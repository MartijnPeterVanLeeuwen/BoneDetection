import os   

def Set_up_dir(Path_to_data_folder):
        """
        This function creates folders that are used to store the training test and validation data
    
        Parameters
        ----------
        Path_to_data_folder : string
            Path to the folder where you want to store the preprocessing results..
    
        Returns
        -------
        Dictionary_paths : dict
            Dictionary with all of the paths that are used during pre-processing or training.
    
        """
        
        Main_Data_folder=Path_to_data_folder
        Data_folder=Main_Data_folder
    
    
        if os.path.isdir(Main_Data_folder)==False:
            os.mkdir(Main_Data_folder)
           
        if os.path.isdir(Data_folder)==False:
            os.mkdir(Data_folder)
            
        Training_dir=os.path.join(Data_folder,"train")
        if os.path.isdir(Training_dir)==False:
            os.mkdir(Training_dir)
        Image_train_dir=os.path.join(Training_dir,"images")
        if os.path.isdir( Image_train_dir)==False:
            os.makedirs( Image_train_dir)
        Label_train_dir=os.path.join(Training_dir,"labels")
        
        if os.path.isdir( Label_train_dir)==False:
            os.makedirs( Label_train_dir)
        
        Testing_dir=os.path.join(Data_folder,"test")
        if os.path.isdir(Testing_dir)==False:
            os.mkdir(Testing_dir)
            
        Image_test_dir=os.path.join(Testing_dir,"images")
        if os.path.isdir( Image_test_dir)==False:
            os.makedirs( Image_test_dir)
            
        Label_test_dir=os.path.join(Testing_dir,"labels")
        if os.path.isdir( Label_test_dir)==False:
            os.makedirs( Label_test_dir)
    
        Validation_dir=os.path.join(Data_folder,"val")
        if os.path.isdir(Validation_dir)==False:
            os.mkdir(Validation_dir)
            
        Image_val_dir=os.path.join(Validation_dir,"images")
        if os.path.isdir( Image_val_dir)==False:
            os.makedirs( Image_val_dir)
        
        Label_val_dir=os.path.join(Validation_dir,"labels")
        if os.path.isdir( Label_val_dir)==False:
            os.makedirs( Label_val_dir)
            
        #%%
        Dictionary_paths=dict()
        
        Dictionary_paths["Im_tr_dir"]=Image_train_dir
        Dictionary_paths["Lab_tr_dir"]=Label_train_dir
        Dictionary_paths["Im_val_dir"]=Image_val_dir
        Dictionary_paths["Lab_val_dir"]=Label_val_dir
        Dictionary_paths["Im_test_dir"]=Image_test_dir
        Dictionary_paths["Lab_test_dir"]=Label_test_dir
        Dictionary_paths["Train_dir"]=Training_dir
        Dictionary_paths["Val_dir"]=Validation_dir
        Dictionary_paths["Test_dir"]=Testing_dir
        
        Dictionary_paths["Dataloader_train_path_im"]=os.path.join(Training_dir,"images")
        Dictionary_paths["Dataloader_train_path_lab"]=os.path.join(Training_dir,"labels")

        Dictionary_paths["Dataloader_val_path_im"]=os.path.join(Validation_dir,"images")
        Dictionary_paths["Dataloader_val_path_lab"]=os.path.join(Validation_dir,"labels")
        #%%


        return Dictionary_paths