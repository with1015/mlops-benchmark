import kserve
import argparse
import logging

from transformers import pipeline, set_seed
from typing import Dict

parser = argparse.ArgumentParser(description='')
parser.add_argument('--model', type=str, default='gpt2')
parser.add_argument('--gpu-mode', action='store_true')

args = parser.parse_args()

set_seed(42)

class CustomModel(kserve.Model):
    def __init__(self, name, model):
        super().__init__(name)
        self.name = name
        self.model = model

    def preprocess(self, request: Dict) -> Dict:
        data = request['data']
        return {"data": data}

    def predict(self, text: Dict) -> Dict:
        text = text['data']
        generated = self.model(text,
                               max_length=30,
                               num_return_sequences=1)
        print(generated)
        return {"result": generated}

    #def postprocess(self, request: Dict) -> Dict:
    #    print('postprocess', request)
    #    return {'result': request}

if __name__ == "__main__":
    if args.gpu_mode:
        model = pipeline('text-generation', model=args.model, device=0)
    else:
        model = pipeline('text-generation', model=args.model, device=-1)
    kube_wrapper = CustomModel("gpt2", model)
    kserve.ModelServer().start([kube_wrapper])
