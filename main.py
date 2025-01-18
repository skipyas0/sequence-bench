from templates import templates
from random import randint
import json

N = 10
COEF_TH = 5
SAMPLES_PER_TEMPLATE = 50

def generate_from_template(template: str) -> tuple[list[int], str]:
    kwargs = {v: randint(-COEF_TH, COEF_TH) for v in ["b1", "b2", "b3", "c1", "c2", "c3"]}
    kwargs.update({v: randint(1,COEF_TH) for v in ["a1", "a2", "a3"]})
    kwargs.update({"q": randint(1, N)})
    func = template.format(**kwargs)
    exec(func, globals())
    sequence_item = globals().get("sequence_item")
    seq = []
    for i in range(N):
        seq.append(sequence_item(i))
    return seq, func
    
if __name__ == "__main__":
    data = {}
    for template_name, template_func in templates.items():
        samples = []
        for s in range(SAMPLES_PER_TEMPLATE):
            seq, func = generate_from_template(template_func)
            samples.append({
                "question": seq,
                "answer": func
            })
        data[template_name] = samples
    with open("data_large.json", "w+") as f:
        json.dump(data, f, indent=4,  separators=(',', ': '))