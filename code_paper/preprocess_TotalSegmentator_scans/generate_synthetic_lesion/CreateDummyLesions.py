import os
import sys

Current_directory = os.getcwd()
Main_folder = "/".join(Current_directory.split("/")[0:-3])  # Linux
sys.path.append(Main_folder)

from utils.PreProcessing.Loading_and_saving_data import Data_processing
from utils.Packages_file import *
from code_paper.preprocess_TotalSegmentator_scans.Return_label_functions import Return_label_dict

Functions=Data_processing()

def Create_sphere_coords(Input_volume,cx,cy,cz, radius, resolution=20):
    """
    This function creates a sphere at a specified coordinate, with a specific size and resolution.
    """
    for ii in range(radius):
        r=ii
        phi = np.linspace(0, 2*np.pi, 2*resolution)
        theta = np.linspace(0, np.pi, resolution)

        theta, phi = np.meshgrid(theta, phi)

        r_xy = r*np.sin(theta)
        x = cx + np.cos(phi) * r_xy
        y = cy + np.sin(phi) * r_xy
        z = cz + r * np.cos(theta)

        for i in range(resolution):

            xcord=x[:,i].astype(int)
            ycord=y[:,i].astype(int)
            zcord=z[:,i].astype(int)

            for i in range(len(xcord)):
                if xcord[i]>0 and ycord[i]>0 and zcord[i]>0:
                    try:
                        Input_volume[xcord[i],ycord[i],zcord[i]]=1
                    except :
                        continue
    return Input_volume

def CreateDummyLesions(Path_to_images,Path_to_labels,Path_to_storage,Filename,Lesions_per_bone=1,Percentage_bone=0.75,radius=np.ceil(10/1.5).astype(int):
    """
    This function makes use of the complete bone labels to generate a binary file that contains synthetic spherical lesions with a specific radius.
    """
    CT,Header=Functions.Loading_Nifti_data(Path_to_images,Filename,Mute=True)
    Label,Header=Functions.Loading_Nifti_data(Path_to_labels,Filename,Mute=True)



    Nr_unique_structures=np.unique(Label[0])
    Nr_unique_structures=[i for i in Nr_unique_structures if i != 0]

    Dummy_lesion_volume=np.zeros(Label[0].shape)
    Test_volume=Create_sphere_coords(np.zeros(Label[0].shape),int(Label[0].shape[0]/2),int(Label[0].shape[1]/2),int(Label[0].shape[2]/2),
                             radius)
    OG_Percentage_bone=copy.copy(Percentage_bone)
    print(Nr_unique_structures)
    for label_nr in tqdm(range(len(Nr_unique_structures))):
        Mask=Label[0]==Nr_unique_structures[label_nr]
        Regions=regionprops(label(Mask))

        Coordinates=[]
        for region_nr in range(len(Regions)):
            if region_nr==0:
                Coordinates=Regions[region_nr].coords
            else:
                Coordinates=np.concatenate((Coordinates,Regions[region_nr].coords))

        if len(Coordinates)>10:
            for lesion_nr in range(Lesions_per_bone):
                Check=True
                attempt=0
                Total_attempts=0
                Percentage_bone=OG_Percentage_bone
                while Check==True:
                    if attempt>=10:
                        attempt=0
                        Percentage_bone=Percentage_bone*0.5
                        #print("reduced")
                    random_point=random.randint(0,len(Coordinates)-1)
                    Proposed_volume=np.zeros(Dummy_lesion_volume.shape)
                    Proposed_volume=Create_sphere_coords(Proposed_volume,Coordinates[random_point][0],Coordinates[random_point][1],Coordinates[random_point][2], radius)
                    Overlap_bone=np.multiply(Mask,Proposed_volume)

                    if np.sum(Overlap_bone)>0:
                        Overlap_count_bone=np.sum(Overlap_bone)/np.sum(Proposed_volume)
                        Overlap_with_previous_volume=np.multiply(Dummy_lesion_volume,Proposed_volume)
                        Bones_present=sorted(list(np.unique(Overlap_bone)))[1:]
                        if Overlap_count_bone>=Percentage_bone and np.sum(Overlap_with_previous_volume)==0 and len(Bones_present)==1:
                            Check=False
                            Scaled_vol=np.ones(Proposed_volume.shape)*Nr_unique_structures[label_nr]
                            Scaled_vol=np.multiply(Proposed_volume,Scaled_vol)
                            Dummy_lesion_volume+=Scaled_vol

                    attempt+=1
                    Total_attempts+=1
                    if Total_attempts>100:

                        Check=False
    Functions.Save_image_data_as_nifti(Path_to_storage,Filename,Dummy_lesion_volume.astype(int),Header=Header[0] )

    Dummy_lesion_volume=1

    return Dummy_lesion_volume
