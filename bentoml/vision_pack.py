import io
import argparse
import json

import torch
import torchvision
import torchvision.models as models
import torchvision.transforms as transforms

from PIL import Image
from bentoml import env, artifacts, api, BentoService
from bentoml.adapters import FileInput, JsonOutput
from bentoml.frameworks.pytorch import PytorchModelArtifact

torch.cuda.set_device(0)
model = models.__dict__['resnet50'](pretrained=True)
model = model.cuda()
model.eval()

normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])
transform = transforms.Compose([transforms.Resize(256),
                                transforms.CenterCrop(224),
                                transforms.ToTensor(),
                                normalize])

with open('./imagenet_labels.json') as f:
    labels = json.load(f)


@env(infer_pip_packages=True)
@artifacts([PytorchModelArtifact('model')])
class PredictServing(BentoService):

    def __init__(self):
        super().__init__()
        self.normalize = transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225])
        self.transform = transforms.Compose([
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                normalize])


    @api(input=FileInput(), batch=False)
    def predict(self, file_streams):
        imgs = Image.open(file_streams).convert('RGB')
        input_imgs = transform_image(imgs)
        input_imgs = input_imgs.cuda()
        outputs = self.artifacts.model(input_imgs)
        index = int(outputs.max(1)[0].item())
        result = class_id_to_label(index)
        print("[DEBUG] prediction:", result)
        return [result]

    def _class_id_to_label(self, i):
        return self.labels[i]

    def _transform_image(self, imgs):
        return transform(imgs).unsqueeze(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="")
    args = parser.parse_args()
    svc = PredictServing()
    svc.pack('model', model)
    svc.save()
