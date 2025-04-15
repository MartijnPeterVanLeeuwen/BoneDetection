import os

def Set_up_nnUNET_dir(Path_to_directory,Name_project):

    if os.path.isdir(Path_to_directory)==False:
        os.mkdir(Path_to_directory)

    no_files=len(os.listdir(Path_to_directory))
    if no_files==0:
        no_files=1
    string="0"*(3-len(str(no_files)))+"%s"%no_files
    Name_of_project="Dataset%s_%s"%(string,Name_project)

    Path_to_project=os.path.join(Path_to_directory,Name_of_project)

    if os.path.isdir(Path_to_project)==False:
        os.mkdir(Path_to_project)

    train_im_dir=os.path.join(Path_to_project,"imagesTr")
    train_lab_dir=os.path.join(Path_to_project,"labelsTr")
    test_dir=os.path.join(Path_to_project,"imagesTs")

    if os.path.isdir(train_im_dir)==False:
        os.mkdir(train_im_dir)
        os.mkdir(train_lab_dir)
        os.mkdir(test_dir)

    return train_im_dir,train_lab_dir,test_dir
