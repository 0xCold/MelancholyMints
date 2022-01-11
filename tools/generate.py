from PIL import Image
import random
import csv
from collections import defaultdict
import pandas as pd
import numpy as np
import json

desired_unique_combo = ["Mint", "Body", "Head", "Eyes"]

banned_combos = {"Robot": ["Crybaby", "Earrings", "Hoop Earrings", "Astronaut Helmet", "Cracked", "Chomped", "Headshot", "Red Sweatband", "Green Sweatband", "Flag Sweatband", "Halo", "Black Turtleneck 1", "Red Turtleneck 1", "Sunset Turtleneck 1", "Space Helmet"],
                 "Alien": ["Astronaut Helmet", "Cracked", "Chomped", "Headshot", "Horns"],
                 "Zombie": ["Chomped", "Cracked", "Horns", "Red Sweatband", "Green Sweatband", "Flag Sweatband"],
                 "Monkey": ["Chomped", "Headphones"],
                 "Crybaby": ["Drool"]}

guaranteed_combos = {
                        # Cold
                        0: {"Background": "Red", "Mint Type": "Blue", "Head": "Brown Wig", 'Eyes': "KOd", "Mouth": "Vamp", "Body": "Red Puffer"},
                        1: {"Mint Type": "Alien"},
                        2: {"Mint Type": "Monkey"},
                        3: {"Mint Type": "Robot"},
                        4: {"Mint Type": "Zombie"},
                        5: {"Mint Type": "Solid Gold"},
                        6: {"Mint Type": "Flag"},
                        # Dabib
                        7: {"Background": "Red", "Mint Type": "Blue", "Head": "Brown Wig", 'Eyes': "KOd", "Mouth": "Vamp",
                            "Body": "Red Puffer"},
                        8: {"Mint Type": "Alien"},
                        9: {"Mint Type": "Monkey"},
                        10: {"Mint Type": "Robot"},
                        11: {"Mint Type": "Zombie"},
                        12: {"Mint Type": "Solid Gold"},
                        13: {"Mint Type": "Flag"},
                        # Mikef
                        13: {"Background": "Red", "Mint Type": "Blue", "Head": "Brown Wig", 'Eyes': "KOd", "Mouth": "Vamp",
                            "Body": "Red Puffer"},
                        14: {"Mint Type": "Alien"},
                        15: {"Mint Type": "Monkey"},
                        16: {"Mint Type": "Robot"},
                        17: {"Mint Type": "Zombie"},
                        # Nacho
                        18: {"Background": "Red", "Mint Type": "Blue", "Head": "Brown Wig", 'Eyes': "KOd", "Mouth": "Vamp",
                            "Body": "Red Puffer"},
                        19: {"Mint Type": "Alien"},
                        20: {"Mint Type": "Monkey"},
                        21: {"Mint Type": "Robot"},
                        22: {"Mint Type": "Zombie"},
                        # Ghoul
                        23: {"Background": "Red", "Mint Type": "Blue", "Head": "Brown Wig", 'Eyes': "KOd", "Mouth": "Vamp",
                            "Body": "Red Puffer"},
                        24: {"Mint Type": "Alien"},
                        25: {"Mint Type": "Monkey"},
                        26: {"Mint Type": "Robot"},
                        27: {"Mint Type": "Zombie"},
                        # Chris
                        23: {"Background": "Red", "Mint Type": "Blue", "Head": "Brown Wig", 'Eyes': "KOd", "Mouth": "Vamp",
                            "Body": "Red Puffer"},
                        24: {"Mint Type": "Alien"},
                        25: {"Mint Type": "Monkey"},
                        26: {"Mint Type": "Robot"},
                        27: {"Mint Type": "Zombie"},

                        # Nacho
                        12: ["Solana Suit", "Zombie", "Bitcoin Bucket Hat", "Red Lazers", "Blue", "Shoulder Parrot", "Bubblegum"],

# Ghoul

                        # Chris

                        # Parents

                        # BMoney

                        # Luke

                        # Beve

                        # Carter

                        # Steve

                        # Miranda

                        # Karly

                        # Harlow

                        # Nalin

                        # Milkman

                        # Boop

                        # Sofia


trait_layer_priorities = ["Background", "Body", "Accessory", "Mint", "Mouth", "Eyes", "Head"]

index_to_trait = ["Body", "Mint", "Head", "Eyes", "Background", "Accessory", "Mouth"]


index_to_rarity = ["Common", "Uncommon", "Rare", "Legendary"]
rarities = {
    "Common": 0,
    "Uncommon": 40,
    "Rare": 70,
    "Legendary": 95,
}

trait_dict = {
    "Background": [
        # Common
        [["Red", "Blue", "Green", "Yellow", "Orange"]],
        [["Red", "Blue", "Green", "Yellow", "Orange"]],
        [["Red", "Blue", "Green", "Yellow", "Orange"]],
        [["Red", "Blue", "Green", "Yellow", "Orange"]]
    ],

    "Body": [
        # Common
        [["Black Tee", "Purple Tee", "GM Tee", "Camo Tee", "Solana Tee", "Bitcoin Tee", "Merch Tee"],
         ["Black Tanktop", "Blue Tanktop", "Red Buttondown 1", "Blue Buttondown 1", "Flannel 1"],
         ["GN Sweater", "Pink Sweater", "Apron", "Red Turtleneck 1", "Sunset Sweater", "Pink Sweater"]],

        # Uncommon
        [["Sunset Puffer", "Red Puffer", "Blue Puffer"],
         ["Black Turtleneck 1", "Flag Suspenders", "Pink Tanktop", "Tie Dye Tee"]],

        # Rare
        [["Suit", "Basketball Jersey", "Tuxedo", "Solana Turtleneck 1"]],

        # Legendary
        ["Solana Suit", "Doctor Coat 1", "Smock", "Shirtless"]
    ],

    "Accessory": [
        # Common
        [["None"]],

        # Uncommon
        [["None"]],

        # Rare
        [["Earrings", "Chain", "Hoop Earrings"]],

        # Legendary
        ["Solana Chain", "Shoulder Parrot"]
    ],

    "Mint": [
        # Common
        [["Red", "Blue", "Green"]],

        # Uncommon
        [["Rainbow", "Solana"]],

        # Rare
        [["Monkey", "Alien", "Robot", "Zombie"]],

        # Legendary
        [["Solid Gold", "Flag", "Solana"]]
    ],

    "Mouth": [
        # Common
        [["Neutral", "Noodle", "Frown", "Lips"]],

        # Uncommon
        [["Grimace", "Tongue", "Buck Teeth", "Drool"]],

        # Rare
        [["Lipstick", "Beard", "Yell", "Vamp"]],

        # Legendary
        [["Cig", "Lit Cig"],
         ["Bubblegum"]]
    ],

    "Head": [
        # Common
        [["None"],
         ["Black Beanie", "Winter Hat", "Cap", "Bitcoin Cap", "Merch Cap", "Black Beret"],
         ["Green Sweatband", "Red Sweatband", "Flag Sweatband", "Bucket Hat", "Bitcoin Bucket Hat", "Headphones"]],

        # Uncommon
        [["Cracked", "Chomped", "Headshot"],
         ["Hardhat", "Propeller Hat", "Sailor Hat", "Pink Beanie", "Red Viking Helmet"],
         ["Blonde Wig 2", "Brunette Wig 2"],
         ["Long Blonde Wig 2", "Long Brunette Wig 2"]],

        # Rare
        [["Halo", "Horns", "Long Purple Wig 2"],
         ["Military Helmet", "Camo Beret", "Solana Bucket Hat"],
         ["Firefighter Hat", "Blue Viking Helmet", "Pirate Hat", "Grandma Wig"]],

        # Legendary
        [["Clown Wig", "Crown", "Space Helmet", "Sombrero"]]
    ],

    "Eyes": [
        # Common
        [["Base", "Sad"],
         ["Glasses", "Square Glasses"]],

        # Uncommon
        [["KOd", "Mutated"],
         ["Shades", "Flag Shades"]],

        # Rare
        [["Heart Shades", "3D Glasses", "Solana Shades"]],

        # Legendary
        [["Blue Lazers", "Red Lazers"],
         ["Crybaby"]]
    ]
}


def generateUniqueToken(tokens, attempt):
    token_traits = []
    for trait_type in trait_dict.keys():
        tier = ""
        if trait_type in desired_unique_combo:
            tier_roll = random.randint(0, 100)
            for tier_name in rarities:
                if tier_roll >= rarities[tier_name]:
                    tier = tier_name
            trait = random.choice(trait_dict[trait_type][index_to_rarity.index(tier)])
            while not isinstance(trait, str):
                trait = random.choice(trait)
            token_traits.append(trait)

    banned_traits = []
    for trait in token_traits:
        banned_traits += banned_combos.get(trait, [])

    for trait in token_traits:
        if trait in banned_traits:
            print(trait, "is banned, retrying!")
            return generateUniqueToken(tokens, attempt + 1)

    if token_traits not in tokens:
        tokens.append(token_traits)
        return tokens

    else:
        return generateUniqueToken(tokens, attempt + 1)


def completeTokens(unique_tokens):
    completed_tokens = []
    for token in unique_tokens:
        final_token = token.copy()
        for trait_type in trait_dict.keys():
            tier = ""
            if trait_type not in desired_unique_combo:
                tier_roll = random.randint(0, 100)
                for tier_name in rarities:
                    if tier_roll >= rarities[tier_name]:
                        tier = tier_name
                trait = random.choice(trait_dict[trait_type][index_to_rarity.index(tier)])
                while not isinstance(trait, str):
                    trait = random.choice(trait)
                final_token.append(trait)

        if final_token[2] == "Chomped" or final_token[2] == "Cracked":
            background_type = final_token[4]
            final_token[2] = final_token[2] + " " + background_type
        completed_tokens.append(final_token)
    return completed_tokens


def generateCollection(num_tokens):
    generated_tokens = []
    for i in range(num_tokens):
        generated_tokens = generateUniqueToken(generated_tokens, 0)
    completed_tokens = completeTokens(generated_tokens)
    return completed_tokens


def drawTokens(tokens):
    for i in range(len(tokens)):
        print(i)

        token = tokens[i]
        background = Image.open("./traits/Background/" + token[4] + "-01.png")

        for trait_name in trait_layer_priorities:
            j = index_to_trait.index(trait_name)
            trait = token[j]

            if trait_name == "Mint":
                mint_type = token[1]
                body_type = token[0]
                if mint_type in ["Alien", "Monkey", "Robot", "Zombie", "Solid Gold"]:
                    if body_type in ["Black Tee", "Purple Tee", "Bitcoin Tee", "Solana Tee", "Smock", "Flag Suspenders", "Camo Tee", "Apron", "Tie Dye Tee", "Merch Tee", "GM Tee"]:
                        extra_trait_img = Image.open("./traits/Extra/" + "Tee Arms " + mint_type + ".png")
                        background.paste(extra_trait_img, (0, 0), extra_trait_img)

                    elif body_type in ["Black Tanktop", "Pink Tanktop", "Basketball Jersey", "Blue Tanktop"]:
                        extra_trait_img = Image.open("./traits/Extra/" + "Tanktop Arms " + mint_type + ".png")
                        background.paste(extra_trait_img, (0, 0), extra_trait_img)

                    elif body_type in ["Shirtless"]:
                        extra_trait_img = Image.open("./traits/Body/" + "Shirtless " + mint_type + "-01.png")
                        background.paste(extra_trait_img, (0, 0), extra_trait_img)

            if trait != "None":
                trait_type = index_to_trait[j]
                if trait_type in ["Shades", "Solana Shades", "Flag Shades", "Heart Shades", "Glasses", "Square Glasses", "3D Glasses"] and token[6] == "Beard":
                    None
                elif trait_type in ["Red Lazers", "Blue Lazers", "Bubblegum", "Space Helmet"]:
                    None
                else:
                    trait_img = Image.open("./traits/" + trait_type + "/" + trait + "-01.png")
                    background.paste(trait_img, (0, 0), trait_img)

            if trait_name == "Background":
                if token[2] in ["Long Blonde Wig 2", "Long Brunette Wig 2", "Long Purple Wig 2"]:
                    print("./traits/Head/" + token[2][:-1] + "1-01.png")
                    extra_trait_img = Image.open("./traits/Head/" + token[2][:-1] + "1-01.png")
                    background.paste(extra_trait_img, (0, 0), extra_trait_img)

            if trait_name == "Accessory":
                mint_type = token[1]
                if mint_type in ["Alien", "Monkey", "Robot"]:
                    extra_trait_img = Image.open("./traits/Extra/" + mint_type + ".png")
                    background.paste(extra_trait_img, (0, 0), extra_trait_img)

            if trait_name == "Mint":
                mint_type = token[1]
                if mint_type in ["Alien", "Monkey", "Robot", "Zombie", "Solid Gold"]:
                    extra_trait_img = Image.open("./traits/Nose/" + mint_type + ".png")
                    background.paste(extra_trait_img, (0, 0), extra_trait_img)
                else:
                    extra_trait_img = Image.open("./traits/Nose/Base.png")
                    background.paste(extra_trait_img, (0, 0), extra_trait_img)

                if mint_type in ["Zombie"]:
                    extra_trait_img = Image.open("./traits/Extra/" + mint_type + ".png")
                    background.paste(extra_trait_img, (0, 0), extra_trait_img)

            if trait_name == "Accessory":
                mint_type = token[1]
                if mint_type in ["Alien", "Monkey", "Robot", "Zombie"]:
                    extra_trait_img = Image.open("./traits/Extra/" + mint_type + ".png")
                    background.paste(extra_trait_img, (0, 0), extra_trait_img)

        if token[0] in ["Blue Buttondown 1", "Red Buttondown 1", "Doctor Coat 1", "Flannel 1", "Black Turtleneck 1", "Sunset Turtleneck 1", "Red Turtleneck 1"]:
            extra_trait_img = Image.open("./traits/Body/" + token[0][:-1] + "2-01.png")
            background.paste(extra_trait_img, (0, 0), extra_trait_img)

        if token[6] == "Beard":
            extra_trait_img = Image.open("./traits/Mouth/" + "Beard-01" + ".png")
            background.paste(extra_trait_img, (0, 0), extra_trait_img)

            if token[3] in ["Shades", "Solana Shades", "Flag Shades", "Heart Shades", "Glasses", "Square Glasses", "3D Glasses"]:
                extra_trait_img = Image.open("./traits/Eyes/" + token[3] + "-01.png")
                background.paste(extra_trait_img, (0, 0), extra_trait_img)

        if token[5] == "Shoulder Parrot":
            extra_trait_img = Image.open("./traits/Accessory/" + "Shoulder Parrot-01" + ".png")
            background.paste(extra_trait_img, (0, 0), extra_trait_img)

        if token[6] in ["Bubblegum"]:
            extra_trait_img = Image.open("./traits/Mouth/" + token[6] + "-01.png")
            background.paste(extra_trait_img, (0, 0), extra_trait_img)

        if token[3] in ["Red Lazers", "Blue Lazers"]:
            extra_trait_img = Image.open("./traits/Eyes/" + token[3] + "-01.png")
            background.paste(extra_trait_img, (0, 0), extra_trait_img)

        if token[2] in ["Space Helmet"]:
            extra_trait_img = Image.open("./traits/Head/" + token[2] + "-01.png")
            background.paste(extra_trait_img, (0, 0), extra_trait_img)

        background.save("./tokens/" + str(i) + ".png")


def generateMetadata(tokens):
    collection_name = "Melancholy Mints"
    collection_symbol = "MM"
    collection_description = "6,666 Slightly-Sad Mints Working Together on the Solana Blockchain"
    collection_seller_fee_basis_points = 500
    image_suffix = ".png"
    collection_creators = [{"address": "AbNPZaGjJ2baLa4RoAS7M2xNxqEku1k2hmVSoNmGsafk", "share": 100}]
    collection_files = [{"uri": "", "type": "image/png"}]
    collection_info = {"name": collection_name, "family": "Genesis"}
    collection_properties = {"creators": collection_creators, "files": collection_files}

    for index, row in tokens.iterrows():
        metadata = {"name": collection_name + " #" + str(index),
                    "symbol": collection_symbol,
                    "description": collection_description,
                    "seller_fee_basis_points": collection_seller_fee_basis_points,
                    "image": str(index) + image_suffix,
                    "attributes": [],
                    "properties": collection_properties,
                    "collection": collection_info
                    }
        metadata["properties"]["files"][0]["uri"] = str(index) + ".json"
        for trait_type in index_to_trait:
            metadata["attributes"].append({"trait_type": trait_type, "value": row[trait_type]})

        with open("../assets/tokens/"+str(index)+".json", "w") as outfile:
            json.dump(metadata, outfile)


def getTokensWithTraitVal(df, trait_type, trait_val):
    tokens = df.loc[df[trait_type] == trait_val]
    return tokens

def editSpecificToken(tokens, indexes_to_edit new_tokens):
    for token in tokens[indexes_to_edit]:
        tokens[indexes_to_edit] = new_tokens[indexes_to_edit]

    return tokens


def writeCSV(tokens):
    f = open('./Tokens.csv', 'w', newline='')
    f.truncate()
    writer = csv.writer(f)
    writer.writerow(index_to_trait)
    for token in tokens:
        writer.writerow(token)


#collection = generateCollection(5555)
#writeCSV(collection)
#drawTokens(collection)

collection_df = pd.read_csv('../assets/Tokens.csv')
generateMetadata(collection_df)

