from PIL import Image
import random
import csv

index_to_rarity = ["Common", "Uncommon", "Rare", "Legendary"]

index_to_trait = ["Clothing", "Head", "Mouth", "Eyes", "Hat"]

rarities = {
    "Common": 0,
    "Uncommon": 40,
    "Rare": 75,
    "Legendary": 100,
}

trait_dict = {
    "Clothing": [["BlackTee", "GreenTee", "PurpleSweater", "RedSweater", "YellowButtondown", "BlueButtondown"],
                 ["SolanaTee", "StripedTee", "TieDyeTee", "GMSweater", "SkullTank"],
                 ["PinkPuffer", "OrangePuffer", "Suit", "Jersey", "Tuxedo"],
                 ["MonkeyCostume"]],

    "Head": [["Red", "Blue", "Green"],
             ["Pink", "Goth"],
             ["Rainbow", "Solana"],
             ["Gold"]],

    "Mouth": [["Neutral", "Noodle", "Frown"],
              ["Yell", "Grimace"],
              ["Vamp"],
              ["Cig", "Beard"]],

    "Eyes": [["Base", "Sad"],
             ["Crybaby", "Ascended"],
             ["LovesickShades", "Shades"],
             ["BlueLazers", "RedLazers"]],

    "Hat": [["None", "Cap", "PinkCap", "GreenHat", "Beanie", "PomPomBeanie", "Sweatband"],
            ["Headshot", "Horns", "Beret", "RedBeret", "Cracked", "Chomped", "MuricaSweatband"],
            ["Halo", "Afro", "SantaHat", "PlumberHat"],
            ["ClownWig", "Crown"]]
}


def generateUniqueToken(tokens, attempt):
    token_traits = []
    for trait_type in trait_dict.keys():
        tier = ""
        tier_roll = random.randint(0, 100)
        for tier_name in rarities:
            if tier_roll >= rarities[tier_name]:
                tier = tier_name
        trait = random.choice(trait_dict[trait_type][index_to_rarity.index(tier)])
        token_traits.append(trait)

    if token_traits not in tokens:
        token_traits.append(random.choice(["Blue", "Red", "Green", "Orange", "Purple", "Yellow"]))
        tokens.append(token_traits)
        return tokens

    else:
        return generateUniqueToken(tokens, attempt + 1)


def generateCollection(num_tokens):
    generated_tokens = []
    for i in range(num_tokens):
        generated_tokens = generateUniqueToken(generated_tokens, 0)
    return generated_tokens


def drawTokens(tokens):
    i = 0
    for token in tokens:
        print(i)

        bg = token[5]
        token_img = Image.open("./traits/Bg/" + bg + "-01.png")

        trait_index = 0
        for trait in token:
            if trait_index <= 4:
                if trait == "Cracked" or trait == "Chomped":
                    trait += bg
                trait_img = Image.open("./traits/" + index_to_trait[trait_index] + "/" + trait + "-01.png")
                token_img.paste(trait_img, (0, 0), trait_img)

                if trait_index == 1:
                    nose_img = Image.open("./traits/Nose-01.png")
                    token_img.paste(nose_img, (0, 0), nose_img)

                trait_index += 1

        if token[0] == "BlueButtondown" or token[0] == "YellowButtondown":
            extra_img = Image.open("./traits/Extras/" + token[0] + "-01.png")
            token_img.paste(extra_img, (0, 0), extra_img)

        if token[2] == "Beard":
            extra_img = Image.open("./traits/Extras/" + token[2] + "-01.png")
            token_img.paste(extra_img, (0, 0), extra_img)

        if token[3] == "BlueLazers" or token[3] == "RedLazers" or token[3] == "Shades" or token[3] == "LovesickShades":
            extra_img = Image.open("./traits/Extras/" + token[3] + "-01.png")
            token_img.paste(extra_img, (0, 0), extra_img)

        token_img.save("./tokens/" + str(i) + ".png")
        i += 1


def writeCSV(tokens):
    f = open('./Tokens.csv', 'w', newline='')
    writer = csv.writer(f)
    writer.writerow(["Clothing", "Head", "Mouth", "Eyes", "Hat", "Bg"])
    for token in tokens:
        writer.writerow(token)


collection = generateCollection(5555)
writeCSV(collection)
drawTokens(collection)
