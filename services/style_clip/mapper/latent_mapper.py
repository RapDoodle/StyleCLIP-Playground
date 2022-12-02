import os
from argparse import Namespace

from ..utils import ensure_checkpoint_exists
from ..mapper.scripts.inference import run


def get_meta_data():
    meta_data = {
        'afro': ['afro', False, False, True, 'Afro'], 
        'angry': ['angry', False, False, True, 'Angry'], 
        'smile': ['smile', False, False, True, 'Smile'], 
        'laughing': ['laughing', False, False, True, 'Laughing'], 
        'Beyonce': ['beyonce', False, False, False, 'Beyonce'], 
        'bobcut': ['bobcut', False, False, True, 'Bobcut'], 
        'bowlcut': ['bowlcut', False, False, True, 'Bowlcut'], 
        'curly hair': ['curly_hair', False, False, True, 'Curly hair'], 
        'Hilary Clinton': ['hilary_clinton', False, False, False, 'Hilary Clinton'],
        'Jhonny Depp': ['depp', False, False, False, 'Jhonny Depp'], 
        'mohawk': ['mohawk', False, False, True, 'Mohawk'],
        'purple hair': ['purple_hair', False, False, False, 'Purple hair'], 
        'surprised': ['surprised', False, False, True, 'Surprised'], 
        'Taylor Swift': ['taylor_swift', False, False, False, 'Taylor Swift'],
        'trump': ['trump', False, False, False, 'Trump'], 
        'Mark Zuckerberg': ['zuckerberg', False, False, False, 'Mark Zuckerberg'],
        'jackie chan': ['jackie_chan', False, False, True, 'Jackie Chan']
    }
    return meta_data


def run_mapper(options, device):
    meta_data = get_meta_data()

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
    
