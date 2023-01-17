import torch
import bentoml
import transformers

from bentoml.io import Text, JSON

model_name = "gpt2-medium"
model = bentoml.transformers.load_model(model_name+":latest")

svc = bentoml.Service("gpt2")

@svc.api(input=JSON(), output=JSON())
def predict(input_series):
    text = str(input_series["inputs"])
    result = model(text, max_length=30, num_return_sequences=2)
    print("[DEBUG] generated: ", result)
    return [result]

