import pandas as pd

splits = {'train': 'train.csv', 'validation': 'dev.csv', 'test': 'test.csv'}
df = pd.read_csv("hf://datasets/Adapting/empathetic_dialogues_v2/" + splits["train"])

print(df.head())