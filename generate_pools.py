import random
import sys
import copy
import os
import re

seed = sys.argv[1]
print("Seed: ", seed)
print()

random.seed(seed)

players = ["Sylvie", "Andrew", "Carlos", "Christos", "Zaq", "J", "Noah", "August"]
sets = ["IKO", "MRD", "ROE", "KLD", "KTK", "THB", "NEO", "GTC"]
rarities = ["C", "U", "R", "M"]
os.makedirs("./pools", exist_ok=True)

def read_set_from_csv(set_code):
  card_dict = {}
  for rarity in rarities:
    card_dict[rarity] = []
  with open(f"data/{set_code}.txt") as file:
    cards = file.readlines()
    for card in cards:
      card = card.strip()
      card_name = f"{card[:-2]} ({set_code})"
      cleaned_name = re.sub(r"[^a-zA-Z0-9,'()/ -]", '', card_name)
      card_rarity = card[-1:]
      card_dict[card_rarity].append(cleaned_name)
  return card_dict

def generate_single_card_by_rarity(card_dict, rarity):
  card_index = random.randint(0, len(card_dict[rarity]) - 1)
  return card_dict[rarity][card_index]

def generate_pack(card_dict):
  pack = []
  commons = copy.deepcopy(card_dict["C"])
  uncommons = copy.deepcopy(card_dict["U"])
  num_commons = 10
  num_uncommons = 3

  has_foil = random.randint(1,3)
  if has_foil == 1:
    num_commons -= 1
    foil_rarity = random.randint(1, 100)
    if foil_rarity <= 2 and len(card_dict["M"]) > 0:
      pack.append(generate_single_card_by_rarity(card_dict, "M"))
    elif foil_rarity <= 15:
      pack.append(generate_single_card_by_rarity(card_dict, "R"))
    elif foil_rarity <= 50:
      pack.append(generate_single_card_by_rarity(card_dict, "U"))
    else:
      pack.append(generate_single_card_by_rarity(card_dict, "C"))

  for i in range(num_commons):
    card_index = random.randint(0, len(commons) - 1)
    pack.append(commons.pop(card_index))
  for i in range(num_uncommons):
    card_index = random.randint(0, len(uncommons) - 1)
    pack.append(uncommons.pop(card_index))
  is_mythic = random.randint(1,8)
  if is_mythic == 1 and len(card_dict["M"]) > 0:
    pack.append(generate_single_card_by_rarity(card_dict, "M"))
  else:
    pack.append(generate_single_card_by_rarity(card_dict, "R"))
  return pack

def generate_pool(set_dictionaries, big_set):
  packs = []
  for set_code in sets:
    card_dict = set_dictionaries[set_code]
    packs_for_set = 3
    if set_code == big_set:
      packs_for_set += 3
    for i in range(packs_for_set):
      packs.append(generate_pack(card_dict))
  pool = {}
  for pack in packs:
    for card in pack:
      if card not in pool:
        pool[card] = 0
      pool[card] += 1
  return pool, packs

def write_pool(pool, packs, player):
  print(f"Writing Pool for {player}")
  with open(f"pools/{player}.txt", "w") as file:
    for card in pool:
      card_str = f"{pool[card]} {card}"
      file.write(card_str + "\n")
      print(card_str)
  print()
  print(f"Writing Packs for {player}")
  for pack in packs:
    print(pack)
  print()
  print()
    

set_dictionaries = {}
for set_code in sets:
  set_dictionaries[set_code] = read_set_from_csv(set_code)
for i in range(len(sets)):
  pool, packs = generate_pool(set_dictionaries, sets[i])
  write_pool(pool, packs, players[i])
