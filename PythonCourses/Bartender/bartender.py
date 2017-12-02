# Ho Thanh Phong
import random

#init dictionaries question
questions = {
    "strong": "Do ye like yer drinks strong?",
    "salty": "Do ye like it with a salty tang?",
    "bitter": "Are ye a lubber who likes it bitter?",
    "sweet": "Would ye like a bit of sweetness with yer poison?",
    "fruity": "Are ye one for a fruity finish?",
}

#init dictionaries ingredients
ingredients = {
    "strong": ["glug of rum", "slug of whisky", "splash of gin"],
    "salty": ["olive on a stick", "salt-dusted rim", "rasher of bacon"],
    "bitter": ["shake of bitters", "splash of tonic", "twist of lemon peel"],
    "sweet": ["sugar cube", "spoonful of honey", "spash of cola"],
    "fruity": ["slice of orange", "dash of cassis", "cherry on top"],
}

def run():
    #make question from dictionaries questions
    for key in questions:
        print(questions[key])
        while True:
            print("Your answer (yes/no): ")
            ans = input()
            if(ans[0].lower() == "y"):
                #make answer random from dictionaries ingredients
                print(random.choice(ingredients[key]))
                break
            elif ans[0].lower() == "n":
                break
            else: print("Wrong answer format, please answer again.")
run()

