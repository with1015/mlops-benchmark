import io
import argparse
import json

import torch
import torchvision.models as models
import torchvision.transforms as transforms

from PIL import Image
from flask import Flask, request, make_response

parser = argparse.ArgumentParser(description='')
parser.add_argument('--model', type=str, default='resnet18')
parser.add_argument('--gpu-mode', action='store_true')

args = parser.parse_args()
model = models.__dict__[args.model]()

app = Flask(__name__)

if args.gpu_mode:
    model = model.cuda()

def transform_image(byte_imgs):
    transform = transforms.Compose([transforms.Resize(224),
                                    transforms.ToTensor()])
    image = Image.open(io.BytesIO(byte_imgs))
    return transform(image).unsqueeze(0)


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        byte_imgs = request.files('image').read()
        input_imgs = transform_image(byte_imgs)
        outputs = model(input_imgs)
        index = str(outputs.max(1).item())

        res = {
            'class_id' : index
        }
        res = make_response(json)
        res.headers['Content-Type'] = 'application/json'
        return res

if __name__ == '__main__':
    app.run()
