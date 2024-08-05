# Import the Fruits class from fruits.py
from scripts.fruits import Fruits
from scripts.houses import Houses
from scripts.anime import Anime


def main():
    INTRO()
    x = input("Press number and enter to continue...")
    print()
    if x == '1':
        FRU()
    elif x == '2':
        HOU()
    elif x == '3':
        ANIME()


def FRU():
    fruit_obj = Fruits()
    fruit_obj.load_nut()


def HOU():
    houses_obj = Houses()
    houses_obj.load_per()


def ANIME():
    anime_obj = Anime()


def INTRO():
    print("WELCOME TO SCRIPTS")
    print("-------------------")
    print("CHOOSE THE FOLLOWING")
    print("1. Load nutrition data")
    print("2. Load Housing data")
    print("3. Load Anime")


if __name__ == "__main__":
    main()
