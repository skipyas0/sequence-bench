import json
from model_api import ModelAPI
import matplotlib.pyplot as plt

PROMPT = """You are given a zero-indexed integer sequence with 10 numbers. 
Your task is to generate a python function with the signature
```python
def sequence_generator(i: int) -> int
```
such that it generates the same number sequence for all i, starting with i=0.
Aim to create a general solution as simply as possible.
Only output python code without markdown formatting.
Sequence:
{seq}
"""

PROMPT_REASON = """You are given a zero-indexed integer sequence with 10 numbers. 
Your task is to generate a python function with the signature
```python
def sequence_generator(i: int) -> int
```
such that it generates the same number sequence for all i, starting with i=0.
Aim to create a general solution as simply as possible.
Only output python code without markdown formatting.
You are allowed to explain your reasoning in valid python comments.
Sequence:
{seq}
"""

def get_attempts(ds, template):
    with open(ds, "r") as f:
        data = json.load(f)
    m = ModelAPI("gpt-4o")
    for category, cat_data in data.items():
        for i, sample in enumerate(cat_data):
            seq = sample['question']
            res = m.predict(template.format(seq=seq), 0.0)
            data[category][i].update({"attempt": res})
    with open("eval_"+ds, "w+") as f:
        json.dump(data, f)

def evaluate(ds):
    eval_len = 15
    with open("eval_"+ds, "r") as f:
        data = json.load(f)
    for category, cat_data in data.items():
        for n, sample in enumerate(cat_data):
            print(f"testing sample {n} in categore {category}")
            gold = sample['answer']
            attempt = sample['attempt']
            if "```python\n" in attempt:
                attempt=attempt.replace("```python\n", "").replace("```","")
            try:
                exec(gold, globals())
                fg = globals().get("sequence_item")
                data[category][n].update({"pass": 0})
            except Exception:
                print("gold error")
                continue
            try:
                exec(attempt, globals())
                fa = globals().get("sequence_generator")
            except Exception:
                print("attempt error")
                data[category][n].update({"pass": 0})
                continue
            ng = []
            na = []
            for i in range(eval_len):
                try:
                    ng.append(fg(i))
                except Exception:
                    print("gold failed on", i)
                    break
                try:
                    na.append(fa(i))
                except Exception:
                    print("attempt failed on", i)
                    break
            print("ng", ng)
            print("na", na)
            if len(ng) == len(na) and len(ng) == eval_len:
                if ng == na:
                    score = 1
                    print("success")
                else:
                    score = 0
                    print("not matching")
            else:
                print("invalid lengths")
            data[category][n].update({"pass": score})

    with open("scored_"+ds, "w+") as f:
        json.dump(data, f)

def plot(ds):
    with open("scored_"+ds, "r") as f:
        data = json.load(f)
    score = {}
    for category, cat_data in data.items():
        score[category] = 0
        for n, sample in enumerate(cat_data):
            score[category] += sample['pass']
        score[category] /= len(cat_data)
    plt.figure()
    keys = list(score.keys())
    values = list(score.values())

    # create bar graph
    plt.bar(keys, values, color='skyblue')

    # add labels and title
    plt.xlabel('Categories')
    plt.ylabel('Values')
    plt.title('Bar Graph of Dictionary Data')

    # show grid and display plot
    plt.xticks(rotation=45, ha='right')  # rotate 45 degrees, align labels to the right

    # show grid and display plot
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()  # adjust layout to fit labels
    plt.savefig("plots/"+ds.replace('json', 'png'))

if __name__ == '__main__':
    ds = "data.json"
    get_attempts(ds, PROMPT)
    evaluate(ds)
    plot(ds)