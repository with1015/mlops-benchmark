import bentoml
from transformers import pipeline, set_seed

model_name = 'gpt2-medium'
device = 0
#device = -1

set_seed(42)

generator = pipeline('text-generation', model=model_name, device=device)

if __name__ == "__main__":
    print("[INFO] Saving models...")
    bentoml.transformers.save_model(name=model_name, pipeline=generator)
    tester = bentoml.transformers.load_model(model_name+":latest")
    print("[DEBUG] check saved model done")
