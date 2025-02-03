from transformers import AutoTokenizer, AutoModelForCausalLM

# Load and save the model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/DeepSeek-R1-Distill-Llama-8B")
model = AutoModelForCausalLM.from_pretrained("deepseek-ai/DeepSeek-R1-Distill-Llama-8B")

# Save locally
tokenizer.save_pretrained("./local_model/tokenizer")
model.save_pretrained("./local_model/model")