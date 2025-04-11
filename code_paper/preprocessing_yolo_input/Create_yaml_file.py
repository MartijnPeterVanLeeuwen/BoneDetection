import os

def Create_yaml_file(Path_to_yolo_folder,Label_dict=None,name_experiment=None):

    Path_to_yaml_file=os.path.join(Path_to_yolo_folder,"data/coco.yaml")

    with open(Path_to_yaml_file,'r') as f:
        data=f.readlines()
    f.close()

    Path_dataset="path: ../datasets/%s\n"%name_experiment
    Path_train="train: train/images\n"
    Path_val="val: val/images\n"
    Path_test="test: test/images\n"

    Index_path=[i for i in range(len(data)) if "path: .." in data[i]][0]
    Index_train=[i for i in range(len(data)) if "train:" in data[i]][0]
    Index_val=[i for i in range(len(data)) if "val:" in data[i]][0]
    Index_tets=[i for i in range(len(data)) if "test:" in data[i]][0]

    for i,j in zip([Path_dataset,Path_train,Path_val,Path_test],[Index_path,Index_train,Index_val,Index_tets]):
        data[j]=i

    Index_start_summing_up_classes=data.index('names:\n')
    Start_file=data[:Index_start_summing_up_classes+1]

    Middle_part=[]
    Labels=list(Label_dict.values())
    Class_names=list(Label_dict.keys())

    for ii in range(len(Labels)):

        class_name=[i for i in Class_names if Label_dict[i]==(ii+1)][0]
        print(ii)
        label_string= '  %s: %s\n'%(ii,class_name)
        Middle_part.append(label_string)

    Index_exd_summing_up_classes=data.index('  79: toothbrush\n')
    End_file=data[Index_exd_summing_up_classes+1:]
    Total_file=Start_file+Middle_part+End_file

    Path_to__new_yaml_file=os.path.join(Path_to_yolo_folder,"data/%s.yaml"%name_experiment)
    with open(Path_to__new_yaml_file,'w') as f:
        f.writelines(Total_file)
    f.close()

#Label_dict={"a":1,"b":2,"c":3}
#Path_to_yolo_folder="/home/mleeuwen/Deep learning Models/Total_bone_detector/yolov5"
#Create_yaml_file(Path_to_yolo_folder,name_experiment="Experiment",Label_dict=Label_dict)
