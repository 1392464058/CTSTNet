import os
import cv2
import random
import numpy as np
import torch
import argparse
from shutil import copyfile
from src.config import Config
from src.Guided_Upsampler import Guided_Upsampler

# train：mode=1
def main(mode=None):
    r"""starts the model

    Args:
        mode (int): 1: train, 2: test, 3: eval, reads from config file if not specified
    """


    config = load_config(mode)

    # init device
    if torch.cuda.is_available():
        config.DEVICE = torch.device("cuda:1")
        torch.backends.cudnn.benchmark = True   # cudnn auto-tuner
    else:
        config.DEVICE = torch.device("cpu")

    # set cv2 running threads to 1 (prevents deadlocks with pytorch dataloader)
    cv2.setNumThreads(0)


    # initialize random seed
    torch.manual_seed(config.SEED)
    torch.cuda.manual_seed_all(config.SEED)
    np.random.seed(config.SEED)
    random.seed(config.SEED)



    # build the model and initialize
    model = Guided_Upsampler(config)
    # model.to(config.DEVICE)
    model.load()  # 这里会根据model来load预训练参数的

    # print(mod)

    # model training
    if config.MODE == 1:
        config.print()
        print('\nstart training...\n')
        model.train()  #会根据model来训练对应的模型的

    # model test
    elif config.MODE == 2:
        print('\nstart testing...\n')
        model.test()

    # eval mode
    else:
        print('\nstart eval...\n')
        model.eval()


def load_config(mode=None):
    r"""loads model config

    Args:
        mode (int): 1: train, 2: test, 3: eval, reads from config file if not specified
    """

    parser = argparse.ArgumentParser()
    #
    parser.add_argument('--path', '--checkpoints', type=str, default='/mnt/data/wyn/sttc/Guided_Upsample/test5_ckpt', help='model checkpoints path (default: ./checkpoints)')
    # 要训练的模型  默认训练edge阶段
    parser.add_argument('--model', type=int, default=3,choices=[1, 2, 3, 4], help='1: edge model, 2: inpaint model, 3: edge-inpaint model, 4: joint model')
    # 其余配置
    parser.add_argument('--config_file',type=str,default='./config_list/config_template.yml',help='The config file of each experiment ')

    parser.add_argument('--Discriminator',type=int,default=0,help='0: original, 1: refect pad')
    parser.add_argument('--Generator',type=int,default=4,help='Remove IN')
    #？在训练过程中，偏离多远
    parser.add_argument('--prior_random_degree',type=int,default=1,help='during training, how far deviate from')
    # 先不用
    parser.add_argument('--use_degradation_2',action='store_true',help='use the new degradation function')

    # test mode
    if mode == 2:
        parser.add_argument('--input', type=str, default='/mnt/data/wyn/sttc/Guided_Upsample/testimage/image',help='path to the input images directory or an input image')
        parser.add_argument('--mask', type=str,default='/mnt/data/wyn/sttc/Guided_Upsample/testimage/mask', help='path to the masks directory or a mask file')

        # edge  或者  ？？
        parser.add_argument('--prior', type=str, default='/mnt/data/wyn/sttc/Guided_Upsample/testimage/structure',help='path to the edges directory or an edge file')

        # parser.add_argument('--output', type=str, default='./savereslut', help='path to the output directory')
        parser.add_argument('--output', type=str, default='./test5_result', help='path to the output directory')
        parser.add_argument('--same_face',action='store_true',help='Same face will be saved in one batch')
        parser.add_argument('--test_batch_size',type=int,default=10,help='equals to the condition number')
        parser.add_argument('--merge',action='store_true',help='merge the unmasked region')


        parser.add_argument('--score',action='store_true')
        parser.add_argument('--condition_num',type=int,default=10,help='Use how many BERT output')

    args = parser.parse_args()
    config_path = os.path.join(args.path, 'config.yml')  #用于复制后的路径

    # create checkpoints path if does't exist
    if not os.path.exists(args.path):
        os.makedirs(args.path)

    # copy config template if does't exist
    # if not os.path.exists(config_path):
    if mode==1:
        copyfile(args.config_file, config_path) ## Training, always copy

    # load config file
    # 用复制后的config_path得到config
    config = Config(config_path)

    # train mode
    if mode == 1:
        config.MODE = 1
        if args.model:
            config.MODEL = args.model
        
        config.Discriminator=args.Discriminator  #0
        config.Generator=args.Generator  #4
        config.prior_random_degree=args.prior_random_degree  #1
        config.use_degradation_2=args.use_degradation_2

    # test mode
    elif mode == 2:
        config.MODE = 2
        config.MODEL = args.model if args.model is not None else 3
        config.INPUT_SIZE = 256

        if args.input is not None:
            config.TEST_FLIST = args.input

        if args.mask is not None:
            config.TEST_MASK_FLIST = args.mask

        if args.prior is not None:
            config.TEST_EDGE_FLIST = args.prior

        if args.output is not None:
            config.RESULTS = args.output

        config.Generator=args.Generator
        config.EDGE=2  ## Load the prior from transformer output
        config.same_face=args.same_face
        config.test_batch_size=args.test_batch_size
        config.merge=args.merge

        config.score=args.score
        config.Discriminator=args.Discriminator
        config.condition_num=args.condition_num
    # eval mode
    elif mode == 3:
        config.MODE = 3
        config.MODEL = args.model if args.model is not None else 3

    return config


if __name__ == "__main__":
    main()
