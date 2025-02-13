import os

def Read_txt_file(Path_to_file,Exclude=None):

    x_s=[]
    y_s=[]
    widths=[]
    heights=[]
    confidences=[]
    classes=[]

    with open(Path_to_file,'r') as f:
        data=f.readlines()

    for i in range(len(data)):
        split_line=data[i].split(" ")
        if Exclude!=None :
            if int(split_line[0])!=int(Exclude):
                classes.append(split_line[0])
                x_s.append(split_line[1])
                y_s.append(split_line[2])
                widths.append(split_line[3])
                heights.append(split_line[4])
                confidences.append(split_line[5][:-2])

    Dictionary={"Class":classes,"Confidences":confidences,"X":x_s,"Y":y_s,"Widhts":widths,"Heights":heights}


    return Dictionary
