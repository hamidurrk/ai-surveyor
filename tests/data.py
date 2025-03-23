import pandas as pd
import json

# splits = {'train': 'train.csv', 'validation': 'dev.csv', 'test': 'test.csv'}
# df = pd.read_csv("hf://datasets/Adapting/empathetic_dialogues_v2/" + splits["train"])
# df.to_json("./data/output.json", orient="records", lines=True)

df = pd.read_json("./data/output.json", orient="records", lines=True)


transformed_data = df.apply(lambda row: {
    "prompt": row["chat_history"],
    "completion": row["sys_response"]
}, axis=1).tolist()

# Save to JSONL
with open("./data/output.jsonl", "w") as f:
    count = 0
    for entry in transformed_data:
        json.dump(entry, f)
        f.write("\n")
        count += 1
        if count == 100:
            break

print("Data has been transformed and saved to output.jsonl")
