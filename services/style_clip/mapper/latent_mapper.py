import os
from argparse import Namespace

from ..utils import ensure_checkpoint_exists
from ..mapper.scripts.inference import run

def run_mapper(options, device):
    meta_data = {
        'afro': ['afro', False, False, True], 
        'angry': ['angry', False, False, True], 
        'Beyonce': ['beyonce', False, False, False], 
        'bobcut': ['bobcut', False, False, True], 
        'bowlcut': ['bowlcut', False, False, True], 
        'curly hair': ['curly_hair', False, False, True], 
        'Hilary Clinton': ['hilary_clinton', False, False, False],
        'Jhonny Depp': ['depp', False, False, False], 
        'mohawk': ['mohawk', False, False, True],
        'purple hair': ['purple_hair', False, False, False], 
        'surprised': ['surprised', False, False, True], 
        'Taylor Swift': ['taylor_swift', False, False, False],
        'trump': ['trump', False, False, False], 
        'Mark Zuckerberg': ['zuckerberg', False, False, False]
    }

    edit_type = options['edit_type'] #@param ['afro', 'angry', 'Beyonce', 'bobcut', 'bowlcut', 'curly hair', 'Hilary Clinton', 'Jhonny Depp', 'mohawk', 'purple hair', 'surprised', 'Taylor Swift', 'trump', 'Mark Zuckerberg']
    edit_id = meta_data[edit_type][0]
    pretrained_model_path = os.path.join('.', 'services', 'style_clip', 'pretrained', 'mapper', f'{edit_id}.pt')

    ensure_checkpoint_exists(pretrained_model_path)
    n_images = 1 #@param

    args = {
        "mapper_output_path": options['mapper_output_path'],
        "work_in_stylespace": False,
        "exp_dir": "results/", # TODO
        "checkpoint_path": pretrained_model_path,
        "couple_outputs": True,
        "mapper_type": "LevelsMapper",
        "no_coarse_mapper": meta_data[edit_type][1],
        "no_medium_mapper": meta_data[edit_type][2],
        "no_fine_mapper": meta_data[edit_type][3],
        "stylegan_size": 1024,
        "test_batch_size": 1,
        "latents_test_path": options['latent_path'],
        "test_workers": 1,
        "n_images": n_images,
        "device": device
    }

    return run(Namespace(**args))
    
