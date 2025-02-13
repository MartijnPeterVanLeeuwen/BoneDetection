import os


def Check_storage_dir(Storage_dir,max_experiments=10):

    if os.path.isdir(Storage_dir)==False:
        os.mkdir(Storage_dir)

    elif os.path.isdir(Storage_dir+'_1')==False:
        os.mkdir(Storage_dir+'_1')
    else:
        Storage_dir=Storage_dir+'_1'
        search=True
        counter=1
        while search==True:
            new_instance=str(counter+1)
            new_path="_".join(Storage_dir.split('_')[:-1])+'_%s'%new_instance

            if os.path.isdir(new_path)==False:
                os.mkdir(new_path)
                search=False
                Storage_dir=new_path
            else:
                counter+=1

            if counter>max_experiments:
                raise Exception("Maximum number of Experiments reached")


    return Storage_dir
