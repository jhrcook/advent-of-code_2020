from collections import Counter
from itertools import product
from pathlib import Path

import colorama
import numpy as np

# Prepare colorama to highlight printed solutions.
colorama.init(autoreset=True)
answer_highlight = colorama.Fore.BLUE + colorama.Style.BRIGHT


# Input data.
DEBUG = False
if DEBUG:
    input_data_file = Path("data", "day_21", "input_test.txt")
else:
    input_data_file = Path("data", "day_21", "input.txt")

foods = []
with open(input_data_file, "r") as file:
    for line in file:
        foods.append(line.rstrip())

allergens_map = {}
ingredients = []

for food in foods:
    ingrts, algns = [x.strip() for x in food.split("(contains")]

    ingrts = ingrts.split(" ")
    ingredients = ingredients + ingrts

    algns = algns.replace(",", "").replace(")", "").split(" ")

    for a in algns:
        if a in allergens_map.keys():
            s = allergens_map[a]
            allergens_map[a] = s.intersection(set(ingrts))
        else:
            allergens_map[a] = set(ingrts)

if DEBUG:
    for a, i in allergens_map.items():
        print(f"{a}: {i}")

allergen_associated_ingredients = set([])
for igs in allergens_map.values():
    allergen_associated_ingredients = allergen_associated_ingredients.union(igs)

allergen_free_ingredients = set(ingredients).difference(allergen_associated_ingredients)
ingredient_count = Counter(ingredients)
count_of_not_allergy = 0
for ig in allergen_free_ingredients:
    count_of_not_allergy += ingredient_count[ig]

print(
    answer_highlight + f"count of ingredients without allergens: {count_of_not_allergy}"
)


for alg, igs in allergens_map.items():
    filtered_igs = igs.difference(allergen_free_ingredients)
    allergens_map[alg] = filtered_igs


allergens_order = {a: i for i, a in enumerate(allergens_map.keys())}
ingredients_order = {ig: i for i, ig in enumerate(ingredients)}
ingredient_allergen_mat = np.zeros((len(allergens_map.keys()), len(ingredients)))

if DEBUG:
    print(ingredient_allergen_mat)
    print(allergens_order)
    print(ingredients_order)

for i in range(ingredient_allergen_mat.shape[0]):
    allergen = list(allergens_order.keys())[i]
    ingrts = allergens_map[allergen]
    for ingrt in ingrts:
        ingredient_allergen_mat[i, ingredients_order[ingrt]] = 1

if DEBUG:
    print(ingredient_allergen_mat)


nrow = ingredient_allergen_mat.shape[0]
ncol = ingredient_allergen_mat.shape[1]

while not np.all(np.sum(ingredient_allergen_mat, axis=1) == 1):
    for i in range(nrow):
        if np.sum(ingredient_allergen_mat[i, :]) == 1:
            which_col = np.where(ingredient_allergen_mat[i, :] == 1)
            ingredient_allergen_mat[:, which_col] = 0
            ingredient_allergen_mat[i, which_col] = 1


allergy_containing_ingredients = []
associated_allergens = []
for j in range(ncol):
    which_cols = ingredient_allergen_mat[:, j] == 1
    if np.any(which_cols):
        allergy_containing_ingredients.append(ingredients[j])
        associated_allergens.append(
            list(allergens_map.keys())[np.where(which_cols)[0][0]]
        )

allergy_containing_ingredients = np.array(allergy_containing_ingredients)
associated_allergens = allergy_containing_ingredients[np.argsort(associated_allergens)]
canonical_dangerous_ingredient = ",".join(associated_allergens)
print(
    answer_highlight
    + f"canonical dangerous ingredient list: {canonical_dangerous_ingredient}"
)
