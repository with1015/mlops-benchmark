import io
import argparse
import json

import torch
import torchvision.models as models
import torchvision.transforms as transforms

import torch.autograd.profiler as profiler

from PIL import Image
from flask import Flask, request, make_response, jsonify

parser = argparse.ArgumentParser(description='')
parser.add_argument('--model', type=str, default='resnet18')
parser.add_argument('--gpu-mode', action='store_true')

args = parser.parse_args()

app = Flask(__name__)

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

with open('imagenet_labels.json') as f:
    labels = json.load(f)


def class_id_to_label(i):
    return labels[i]


def transform_image(byte_imgs):
    image = Image.open(io.BytesIO(byte_imgs))
    return transform(image).unsqueeze(0)


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        global model
        byte_imgs = request.files['file'].read()
        input_imgs = transform_image(byte_imgs)
        if args.gpu_mode:
            input_imgs = input_imgs.cuda()
        outputs = model(input_imgs)
        index = int(outputs.max(1)[0].item())
        result = class_id_to_label(index)
        print('[DEBUG] prediction:', result)
        return jsonify({'result': result})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port='51234',
            use_reloader=False,
            threaded=False)
