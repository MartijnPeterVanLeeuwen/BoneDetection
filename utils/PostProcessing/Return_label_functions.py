def Return_label_dict(Path_to_desired_labels_txt):

    Labels = sorted(Return_desired_labels(Path_to_desired_labels_txt))
    Label_dict = dict()
    
    for i in range(len(Labels)):
        Label_dict[Labels[i].split(".")[0]] = i + 1

    return Label_dict

def Return_desired_labels(Path_to_label_txt_file):

    with open(Path_to_label_txt_file,'r') as f:
        List_of_labels=f.readlines()
    f.close()
    List_of_labels=[i.split("\n")[0] for i in List_of_labels]

    return List_of_labels
