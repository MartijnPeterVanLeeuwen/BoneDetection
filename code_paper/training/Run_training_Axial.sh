name=Axial_BSv2_v5.yaml
path_to_hyp=data/hyps/Hyp_Axial.yaml
name_exp=Axial_BS_final

cd /home/mleeuwen/Deep\ learning\ Models/Total_bone_detector/yolov5
pwd
device=0
Optimizer='SGD'
Batch_size=-1

python train.py --img 448 --batch-size $Batch_size  --epochs 1000 --data $name --weights yolov5l.pt --device $device --patience=25 --hyp $path_to_hyp --name $name_exp --optimizer $Optimizer
