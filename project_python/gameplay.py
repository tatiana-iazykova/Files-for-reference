import pandas as pd
import random
import inspect
import json
from collections import OrderedDict
import functools

from events import Rules

def success(func):
  def wrapper(self, key, mode):
      func(self, key=key, mode=mode)
      print('OK!')
  return wrapper

def in_class(func):
  def wrapper(self, opt='self.'):
    return func(self, opt)
  return wrapper   
  
class Interpret:
  def __init__(self, rules):
    self.rules = rules

  @in_class
  def interpret(self, opt=''):
    rules = []
    for i in range(len(self.rules)):
      rule = self.rules[i]
      res = ''
      for key in rule:
        if key == '$condition':
          res+= 'if '
          for k,v in rule[key].items():
            if k == '$gt':
              sign = ' > '
            elif k == '$lt':
              sign = ' < '
            res += list(rule['$condition'][k].keys())[0] + f'{sign}' + str(list(rule['$condition'][k].values())[0]) + ':\t'
        elif key == '$action':
          res += opt+rule[key]
          res += '\nelse:\tprint("You are too weak")'
      rules.append(res)
    return rules
    
class Game:
  def __init__(self, player, meta):
    self.game = 1
    self.everybody = player
    self.stats = {v.name:v.points for k,v in self.everybody.items()} 
    self.rules = Rules(self.everybody, self.stats)   
    self.meta = Interpret(meta).interpret()

  @property  
  def leaderboard(self):
    players = []
    points = []
    for k,v in self.stats.items():
      players.append(k)
      points.append(v)
    return pd.DataFrame({'player': players, 'points': points})
  
  def chosen_politic(self, key):
    return self.everybody[key]

  @success
  def main(self, key, mode):
    politic = self.chosen_politic(key)
    if mode == 'bribes':
      self.rules.take_bribes(politic)
    elif mode == 'charity':
      self.rules.gives_to_charity(politic)
    elif mode == 'loser':
      self.rules.loses_election(politic)
    elif mode == 'gain':
      self.rules.gain_power(politic)
    elif mode == 'special':
      politic.power -= 4
      politic.special()
    elif mode == 'luck':
      self.rules.lucky(politic)
    elif mode == 'power':
      self.rules.gain_power(politic)  

  def show_stats(self, key):
    stat_sum = OrderedDict({'name':'','party': '', 'points':'', 'money': '', 'power':''})
    for i in inspect.getmembers(self.chosen_politic(key=key)):
      if not i[0].startswith('_'):
        if not inspect.ismethod(i[1]): 
            stat_sum[i[0]] = i[1]
    return pd.DataFrame.from_dict(data=stat_sum, orient='index', columns=[key])
 
  def big_trouble(self, key):
    politic = self.chosen_politic(key=key)
    exec(self.meta[0])
    
  def choose(self, key):
    self.chosen_politic(key).power -= 15 
    num = int(input("Pick your poison: 1) bribes, 2) lose "))
    if num == 1: 
       for player in self.everybody:
         if player != key:
          self.chosen_politic(player).corrupt = True          
    elif num == 2:
        for player in self.everybody:
         if player != key:
          self.chosen_politic(player).election = 'lose'
  
  def please_everybody(self, key):
    politic = self.chosen_politic(key=key)
    exec(self.meta[1])

  def spend(self, key):
    mon = 10000/(len(self.everybody)-1)
    for player in self.everybody:
        if player != key:
          self.chosen_politic(player).money += mon
    self.chosen_politic(key).money -= 10000  

  def turn(self, key):
    show_stats = int(input('Do you want to see your stats?\n 1) Yes, 2) No '))
    if show_stats == 1:
      print(self.show_stats(key))
    event = random.choice(['bribes', 'charity', 'loser', 'luck', 'power'])
    meta = int(input('Do you want to do some bad or some good?\n 1) bad, 2) good, 3) None '))
    if meta == 1:
      self.big_trouble(key)
    elif meta == 2:
      self.please_everybody(key)
    else:
      message = int(input('Roll the dice or you want some super action?\n 1) dice, 2) action '))
      if message == 2:
        self.main(key, mode='special')
      else:
        print()
        print(event, 'is happening')
        self.main(key, mode=event)

  def play(self, def_games=5):
    for game in range(def_games):
      for key in self.everybody.keys():
        print(key +"'s turn")
        self.turn(key)
        print('_______________________________________________________________')
      print('_______________________________________________________________')  
      print('game number:', self.game)
      print(self.leaderboard)
      self.game += 1
      print('\n_______________________________________________________________\n')