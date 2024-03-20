# STTC

The official pytorch implementation of our paper STTC: Structure Transformer combined with Texture CNN for image inpainting.


>  STTC: Structure Transformer combined with Texture CNN for image inpainting
> 
> Zhan Li, etc.
> 


## Prerequisites
- Pytorch 1.5
- requirements.txt

## Training
```shell
(1) -  Training Stage (b) (Structure Reconstruction Network)
Enter the Transformer folder
Modify the configuration information in main.py:
--GPU_ids is the GPU parameter-- Data_path is the training data path-- Mask_path is the path for training the mask;
--Validation_path is the validation data path;
Command: Python main.py


(2) -  Training Stage (a) (Texture Reconstruction Network)
Go to the Guided_Upsample folder
Modify the configuration file under config_list:
Among them, trainflist, valflist, and testflist are the paths of the images for training, validation, and testing, respectively;
Train_maskflist, val_maskflist, and test_maskflist are the paths of the training, validation, and testing masks, respectively;
LR is the learning rate;
Modify the parameters of main.py:
--Model is 1
Command: Python train.py

(3) -  Training Stage (c) (Image Completion Network)
Go to the Guided_Upsample folder
Modifying configuration file parameters under config_list is the same as training in stage A
Modify the parameters of main.py:
--Model is 2
Command: Python train.py
```



## Testing
```shell
python test.py --name results/flower_selfunet --gpu 0
```

The generated images will be saved in `results/flower_selfunet/test`.


## Evaluation
```shell
python main_metric.py --gpu 0 --dataset flower \
--name results/flower_selfunet \
--real_dir datasets/for_fid/flower --ckpt gen_00100000.pt \
--fake_dir test_for_fid
```

## Citation
If you use this code for your research, please cite our paper.

    @inproceedings{lizhan2023,
    title={SelfUNet: Self-attention enhanced UNet for few-shot image generation},
    author={Zhan, tec},
    booktitle={},
    pages={},
    year={2023}
    }



