name=Sagital_BSv2_v5.yaml
path_to_hyp=data/hyps/Hyp_Sagital.yaml
name_exp=Sagital_BS_final

cd /home/mleeuwen/Deep\ learning\ Models/Total_bone_detector/yolov5
pwd
device=2
python train.py --img 672 --batch-size -1  --epochs 1000 --data $name --weights yolov5l.pt --device $device --patience=25 --hyp $path_to_hyp --name $name_exp
