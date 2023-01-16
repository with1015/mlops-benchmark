import argparse
import json
import base64
import kserve

import torch
import torchvision.models as models
import torchvision.transforms as transforms

from typing import Dict
from PIL import Image
from io import BytesIO

parser = argparse.ArgumentParser(description='')
parser.add_argument('--model', type=str, default="resnet18")
parser.add_argument('--gpu-mode', action='store_true')

args = parser.parse_args()

if args.gpu_mode:
    torch.cuda.set_device(0)


class CustomModel(kserve.Model):
    def __init__(self, name, model, args):
        super().__init__(name)
        self.name = name
        self.model = model
        self.normalize = transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225])
        self.transform = transforms.Compose([
                transforms.Resize(256),
                transforms,CenterCrop(224),
                transforms.ToTensor(),
                normalize])
        if args.gpu_mode:
            self.model = self.model.cuda()
        with open('./imagenet_labels.json') as f:
            self.labels = json.load(f)

    def preprocess(self, request: Dict) -> Dict:
        data = request['data']
        img = Image.open(BytesIO(base64.b64decode(data)))
        return {"img", img}

    def predict(self, input_img: Dict) -> Dict:
        img = input_img["img"]
        output = self.model(img)
        index = int(output.max(1)[0].item())
        return {"index": index}

    def postprocess(self, index: Dict) -> Dict:
        idx = index["index"]
        result = self.labels[idx]
        return {'result': result}


if __name__ == "__main__":
    model = models.__dict__[args.model](pretrained=True)
    kube_wrapper = CustomModel("vision", model, args)
    kserve.ModelServer().start([kube_wrapper])
