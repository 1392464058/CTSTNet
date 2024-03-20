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
# traing the STTC network step by step

```shell
(1) -  Training Stage (b) (Structure Reconstruction Network)
Enter the Transformer folder
Modify the configuration information for main.py:
--GPU_ids is the GPU parameter -- Data_path is the training data path -- Mask_path is the path for the masks
--Validation_path is the validation data path
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
(1) -  Testing Stage (b) (Structure Reconstruction Network)
Go to the Transformer folder
Modify the configuration information in the conference.py file:
--Ckpt_path is the path where the pre trained model is stored -- Image_URL is the path to the test image -- Mask_URL is the path of the mask
--Save_URL is the path where the output is saved
Command: Python conference.py -- BERT -- GELU_2
Save the obtained structure results

(2) -  Testing Stage (b)&(c) (Structure Reconstruction Network) (Image Completion Network)
Go to the Guided_Upsample folder
Modify the configuration information of main.py:
--Path is the path where the pre trained model is stored -- Set the model to 3 -- Input is the path to the test images -- Mask is the path of the mask
--Prior is the path to the structure diagram obtained in stage B --Output The path where the output directory is saved as the restored result
Command: Python test.py
```

The generated images will be saved in the Output directory given by --Output.



## Citation
If you use this code for your research, please cite our paper.

    @inproceedings{lizhan2023,
    title={STTC: Structure Transformer combined with Texture CNN for image inpainting},
    author={Zhan, tec},
    booktitle={},
    pages={},
    year={2023}
    }



