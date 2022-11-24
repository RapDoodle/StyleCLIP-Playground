
import time
import os
import sys
import numpy as np
from argparse import Namespace

from PIL import Image
import matplotlib.pyplot as plt
import torch
import torchvision.transforms as transforms

import clip
from ..manipulate import Manipulator
from ..StyleCLIP import GetDt,GetBoundary


def run_global_direction(options, device):
    dataset_name='ffhq'

    model, preprocess = clip.load("ViT-B/32", device=device,jit=False)

    module_pretrained_path = os.path.join('.', 'services', 'style_clip', 'global_directions', 'pretrained')
    network_pkl = os.path.join(module_pretrained_path, 'model', f'{dataset_name}.pkl')
    device = torch.device(device)
    M=Manipulator()
    M.device=device
    G=M.LoadModel(network_pkl, device)
    M.G=G
    M.SetGParameters()
    num_img=100_000
    M.GenerateS(num_img=num_img)
    M.GetCodeMS()
    np.set_printoptions(suppress=True)

    file_path=os.path.join(module_pretrained_path, 'npy', f'{dataset_name}')
    fs3=np.load(os.path.join(file_path, 'fs3.npy'))

    img_index = 1

    # mode='real image' #@param ['real image', 'generated image']
    mode = options['mode']

    if mode == 'real image':
        img_index = 0
        latents=torch.load(options['latent_path'])
        dlatents_loaded=M.G.synthesis.W2S(latents)

        img_indexs=[img_index]
        dlatents_loaded=M.S2List(dlatents_loaded)

        dlatent_tmp=[tmp[img_indexs] for tmp in dlatents_loaded]
    elif mode == 'generated image':
        img_indexs=[img_index]
        dlatents_loaded=M.S2List(dlatents_loaded)
        dlatent_tmp=[tmp[img_indexs] for tmp in M.dlatents]
    M.num_images=len(img_indexs)

    M.alpha=[0]
    M.manipulate_layers=[0]
    codes,out=M.EditOneC(0,dlatent_tmp) 
    original=Image.fromarray(out[0,0]).resize((512,512))
    M.manipulate_layers=None
    

    # neutral='face with eyes' #@param {type:"string"}
    neutral = options['neutral']
    # target='face with blue eyes' #@param {type:"string"}
    target = options['target']
    classnames=[target,neutral]
    dt=GetDt(classnames,model,device)

    # beta = 0.15 #@param {type:"slider", min:0.08, max:0.3, step:0.01}
    beta = options['beta']
    # alpha = 4.1 #@param {type:"slider", min:-10, max:10, step:0.1}
    alpha = options['alpha']
    M.alpha=[alpha]
    boundary_tmp2,c=GetBoundary(fs3,dt,M,threshold=beta)
    codes=M.MSCode(dlatent_tmp,boundary_tmp2)
    out=M.GenerateImg(codes)
    generated=Image.fromarray(out[0,0])#.resize((512,512))

    return generated


