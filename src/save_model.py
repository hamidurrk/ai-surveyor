from transformers import AutoTokenizer, AutoModelForCausalLM
import os 

model_name = "deepseek-ai/DeepSeek-R1-Distill-Llama-8B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

cache_dir = os.path.join(os.path.expanduser("~"), ".cache", "huggingface", "transformers")

print(f"Tokenizer path: {os.path.join(cache_dir, model_name, 'tokenizer')}")
print(f"Model path: {os.path.join(cache_dir, model_name, 'model')}")

# tokenizer.save_pretrained("./local_model/tokenizer")
# model.save_pretrained("./local_model/model")