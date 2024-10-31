import math

human_oxigen = 0.5
oak_50_years = 20
utree_25_years = 32
year = 365

oxigen_for_human = (human_oxigen * year)
answer2 = math.ceil(oxigen_for_human / utree_25_years)
answer3 = math.ceil(oxigen_for_human / oak_50_years)

print(f"{oxigen_for_human} {answer2} {answer3}")