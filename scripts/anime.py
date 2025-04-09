import requests
import json


class Anime:

  def __init__(self):
    self.url = "https://api.jikan.moe/v4/"
    response = requests.get(self.url)
    self.load_ask()

  def load_ask(self):
    while True:
      print("-------------------")
      print("CHOOSE THE FOLLOWING")
      print("1. Guess the anime")
      print("click anything else to exit")
      user_choice = input("Press number and enter to continue...")
      if user_choice == '1':
        self.guess_anime_intro()
      else:
        break

  def retrive(self, url):
    response = requests.get(url)
    data = {}
    if response.status_code == 200:
      data = response.json()
    else:
      print("ERROR: " + str(response.status_code) + " CODE")
    return data

  def guess_anime_intro(self):
    print(
        "Welcome to Guess the anime, I'm going to give you the sypnosis of an anime and you have to guess the anime."
    )
    print("-------------------")
    print("CHOOSE THE FOLLOWING")
    print("1. LET'S PLAY")
    print("2. Could you explain it differently?")
    print("click anything else to exit")
    while True:
      user_choice = input("Press number and enter to continue...")
      if user_choice == '1':
        self.guess_anime()
        break
      if user_choice == '2':
        print("Nope")
      else:
        break

  def eng_grab(self, data):
    titles = data['data']['titles']
    eng_titles = []
    for i in titles:
      if i['type'] == 'English' or i['type'] == 'Default' or i[
          'type'] == 'Synonym':
        eng_titles.append(i['title'])
    return eng_titles

  def check_syn_with_titles(self, syn, eng_titles):
    for i in eng_titles:
      if syn is None:
        return False
      if i in syn:
        return False
    return True

  def guess_anime(self):
    add = "random/anime"
    url_cur = self.url + add
    data = self.retrive(url_cur)
    eng_titles = self.eng_grab(data)
    while True:
      syn = data['data']['synopsis']
      if self.check_syn_with_titles(syn, eng_titles):
        break
      else:
        url_cur = self.url + add
        data = self.retrive(url_cur)
        eng_titles = self.eng_grab(data)
    print(syn)
    while True:
      guess = input("Now guess the anime: ")
      if guess == "" or guess == " ":
        print("actually put something this time, don't be a dummy")
      else:
        break
    flag = False
    for i in eng_titles:
      if guess == i:
        print("You WIN!")
        flag = True
        break
      elif guess in i and (len(guess) > (len(i) // 6)):
        print("CLOSE ENOUGH!")
        flag = True
        break
    if not flag:
      print("You didn't get it...")
    print("It was: " + eng_titles[0])
    print("Thanks for playing")


if __name__ == "__main__":
  anime_obj = Anime()
  anime_obj.load_ask()
