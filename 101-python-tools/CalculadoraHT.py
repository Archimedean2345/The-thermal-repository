# Calculadora de transferencia de calor 1-dimension
# Inputs
# Casos
#   1. Pared
#       a. fluido - pared - fluido
#       b. fluido - pared1 - pared2 - fluido
#       c. solido - pared1
def menu():
    opts = {"1": ("List", list_items), "2": ("Add", add_item), "3": ("Exit", None)}
    while True:
        for k, v in opts.items(): print(f"{k}. {v[0]}")
        c = input("> ").strip()
        if c == "3": break
        if c in opts: opts[c][1]()
        else: print("Invalid.")

# Outputs