import argparse
import json
import base64
import torch
import mlflow
import mlflow.pyfunc
import mlflow.pytorch

import torchvision.models as models
import torchvision.transforms as transforms

from PIL import Image
from io import BytesIO

parser = argparse.ArgumentParser(description="")
parser.add_argument('--gpu-mode', action="store_true")
parser.add_argument('--model', type=str, default='resnet18')
args = parser.parse_args()

model = models.__dict__[args.model](pretrained=True)

if args.gpu_mode:
    torch.cuda.set_device(0)
    model = model.cuda()
model = model.eval()

normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])
transform = transforms.Compose([transforms.Resize(256),
                                transforms.CenterCrop(224),
                                transforms.ToTensor(),
                                normalize])

with open('./imagenet_labels.json') as f:
    labels = json.load(f)

def class_id_to_label(i):
    return labels[i]


class PytorchServingAritifact(mlflow.pyfunc.PythonModel):

    def __init__(self, model):
        self.model = model

    def predict(self, context, input_json):
        imgs = self._recover_image(input_json)
        input_imgs = self._transform_image(imgs)
        if args.gpu_mode:
            input_imgs = input_imgs.cuda()
        outputs = self.model(input_imgs)
        index = int(outputs.max(1)[0].item())
        result = class_id_to_label(index)
        print("[DEBUG] prediction:", result)
        return [result]

    def _recover_image(self, base_data):
        img = Image.open(BytesIO(base64.b64decode(base_data)))
        return img.convert('RGB')

    def _transform_image(self, imgs):
        return transform(imgs).unsqueeze(0)


if __name__ == "__main__":
    model_path = args.model + "_pretrained"
    wrapped_model = PytorchServingAritifact(model)
    mlflow.pyfunc.save_model(model_path, python_model=wrapped_model)
