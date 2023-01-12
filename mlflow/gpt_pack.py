import argparse
import json
import base64
import torch
import mlflow
import mlflow.pyfunc
import mlflow.pytorch

from transformers import pipeline, set_seed
from io import BytesIO

parser = argparse.ArgumentParser(description="")
parser.add_argument('--gpu-mode', action="store_true")
parser.add_argument('--model', type=str, default='gpt2')
args = parser.parse_args()

set_seed(42)

if args.gpu_mode:
    torch.cuda.set_device(0)
    generator = pipeline('text-generation', model=args.model, device=0)
else:
    generator = pipeline('text-generation', model=args.model, device=-1)


class PytorchServingAritifact(mlflow.pyfunc.PythonModel):

    def __init__(self, model):
        self.model = model

    def predict(self, context, input_string):
        result = self.model(str(input_string),
                            max_length=30,
                            num_return_sequences=1)
        print("[DEBUG] generate:", result)
        return [result]


if __name__ == "__main__":
    model_path = args.model + "_pretrained"
    wrapped_model = PytorchServingAritifact(generator)
    mlflow.pyfunc.save_model(model_path, python_model=wrapped_model)
