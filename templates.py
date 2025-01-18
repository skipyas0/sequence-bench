templates = {
    "LINEAR_MULTI": """def sequence_item(i):
        if i < {q}:
            return {a1}*i + {b1}
        elif i > {q}:
            return {a2}*i + {b2}
        else:
            return {a3}*i + {b3}""",

    "QUADRATIC_SIMPLE": """def sequence_item(i):
    return {a1}*i*i + {b1}*i + {c1}""",

    "QUADRATIC_MULTI": """def sequence_item(i):
    if i < {q}:
        return {a1}*i*i + {b1}*i + {c1}
    elif i > {q}:
        return {a2}*i*i + {b2}*i + {c2}
    else:
        return {a3}*i*i + {b3}*i + {c3}""",

    "SUM": """def sequence_item(i):
    return sum([{a1}*j+{b1} for j in range(i)])""",

    "SUM_EVEN_ODD": """def sequence_item(i):
    return sum([{a1}*j+{b1} if j%2==0 else {a2}*j+{b2} for j in range(i)])""",

    "ALTERNATING": """def sequence_item(i):
    return {a1} * i + (-1)**i * {a2} * i + {b1} + (-1)**i * {b2}""",

    "RECURRENT": """def sequence_item(i):
    if i == 0:
        return {b1}
    elif i == 1:
        return {b2}
    return {a1} * sequence_item(i-1) + {a2} * sequence_item(i-2)""",

    "LINEAR_MODULO": """def sequence_item(i):
    return ({a1}*i + {b1}) % {q}""",
}