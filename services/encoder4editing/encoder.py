import os
from argparse import Namespace

import numpy as np
import dlib
import torch
import torchvision.transforms as transforms
from PIL import Image

from .utils.common import tensor2im
from .models.psp import pSp
from .utils.alignment import align_face


def encode_to_latent(image_path, latent_path, device):
    experiment_type = 'ffhq_encode'
    model_file = 'e4e_ffhq_encode.pt'
    shape_predictor_path = os.path.join('.', 'services', 'encoder4editing', 'pretrained', 'shape_predictor_68_face_landmarks.dat')

    EXPERIMENT_ARGS = {
        "model_path": os.path.join('.', 'services', 'encoder4editing', 'pretrained', model_file)
    }
    EXPERIMENT_ARGS['transform'] = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor(),
        transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])])
    resize_dims = (256, 256)

    model_path = EXPERIMENT_ARGS['model_path']
    ckpt = torch.load(model_path, map_location='cpu')
    opts = ckpt['opts']
    # pprint.pprint(opts)  # Display full options used
    # update the training options
    opts['checkpoint_path'] = model_path
    opts['device'] = device
    opts= Namespace(**opts)
    net = pSp(opts)
    net.eval()
    net.to(device)
    print(f'Model {model_file} successfully loaded')

    #@title Align image
    original_image = Image.open(image_path)
    original_image = original_image.convert('RGB')

    def run_alignment(image_path):
        predictor = dlib.shape_predictor(shape_predictor_path)
        aligned_image = align_face(filepath=image_path, predictor=predictor) 
        print("Aligned image has shape: {}".format(aligned_image.size))
        return aligned_image 

    if experiment_type == "ffhq_encode":
        input_image = run_alignment(image_path)
    else:
        input_image = original_image

    input_image.resize(resize_dims)

    #@title Invert the image
    img_transforms = EXPERIMENT_ARGS['transform']
    transformed_image = img_transforms(input_image)

    def run_on_batch(inputs, net):
        images, latents = net(inputs.to(device).float(), randomize_noise=False, return_latents=True)
        if experiment_type == 'cars_encode':
            images = images[:, :, 32:224, :]
        return images, latents

    with torch.no_grad():
        images, latents = run_on_batch(transformed_image.unsqueeze(0), net)
        result_image, latent = images[0], latents[0]
    torch.save(latents, latent_path)

    # Display inversion:
    # display_alongside_source_image(tensor2im(result_image), input_image)