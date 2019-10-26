import io

import numpy as np
import torch
import torch.nn as nn
from PIL import Image
from torchvision import transforms, models
import base64

model_name = "model.pth"


class HandClassifier(nn.Module):
    def __init__(self, output):
        super(HandClassifier, self).__init__()

        alexnet = models.alexnet()

        self.process = nn.Sequential(
            alexnet.features,
            nn.Conv2d(256, output, (7, 7)),
            nn.ReLU(),
            nn.Softmax2d()
        )

    def forward(self, inputs):
        return self.process(inputs).squeeze()


model = HandClassifier(3)
model.load_state_dict(torch.load(f"./app/resources/model/{model_name}", map_location=torch.device('cpu')))

loader = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(256),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def convert(image_path):
    image = Image.open(image_path).convert("RGB")
    image = loader(image).float()
    image = torch.tensor(image)

    with torch.no_grad():
        possibility, idx = model(image.unsqueeze(0)).max(0)
    return possibility.item(), idx.item()

def convert_from_base64(image_base64):
    base64_decoded = base64.b64decode(image_base64)

    image = Image.open(io.BytesIO(base64_decoded)).convert("RGB")
    image = loader(image)

    with torch.no_grad():
        possibility, idx = model(image.unsqueeze(0)).max(0)
    return possibility.item(), idx.item()