import torch
from .model_1dconv import Yoga1DCnnModel
import os

def load_model(resume="final.pt", device=None):
    model_args = {
            "hidden_layers": [
                16,
                32,
                32,
                32
            ],
            "num_classes": 45,
            "easy_margin": False,
            "m": 0.1,
            "arc_margin": True,
            "kernel_size": 15,
            "pool": 2
        }
    model = Yoga1DCnnModel(**model_args)

    if device is None:
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    print('loading score model =======>', resume, device)
    checkpoint = torch.load(resume, map_location=device)
    state_dict = checkpoint['state_dict']
    model.load_state_dict(state_dict)

    
    model = model.to(device)
    model.eval()

    return model

@torch.no_grad()
def inference(model, keypoints_1, keypoints_2):
    keypoints = [keypoints_1, keypoints_2]
    features = []
    for kp in keypoints:
        if torch.is_tensor(kp):
            if kp.ndim < 3:
                kp_tensor = torch.unsqueeze(kp, 0)
            else:
                kp_tensor = kp
        else:
            kp_tensor = torch.unsqueeze(torch.from_numpy(kp), 0)
        features.append(model.encode(kp_tensor))

    score = torch.diagonal(torch.mm(features[0], features[1].T), 0)[0].cpu().detach().numpy()
    return score
