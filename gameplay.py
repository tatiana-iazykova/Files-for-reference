import pandas as pd
import inspect
from collections import OrderedDict
from events import Rules

class Game:
  def __init__(self, player, meta):
    self.everybody = player
    self.stats = {v.name:v.points for k,v in self.everybody.items()} 
    self.rules = Rules(self.everybody, self.stats)   
    self.meta = Interpret(meta).interpret()
  
  def print_stats(self):
    players = []
    points = []
    for k,v in self.stats.items():
      players.append(k)
      points.append(v)
    return pd.DataFrame({'player': players, 'points': points})
  
  def chosen_politic(self, key):
    return self.everybody[key]

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
      politic.special()

  def show_stats(self, key):
    stat_sum = OrderedDict({'name':'','party': '', 'points':'', 'money': ''})
    for i in inspect.getmembers(self.chosen_politic(key=key)):
      if not i[0].startswith('_'):
        if not inspect.ismethod(i[1]): 
            stat_sum[i[0]] = i[1]
    return pd.DataFrame.from_dict(data=stat_sum, orient='index', columns=[key])
 
  def big_trouble(self, key):
    politic = self.chosen_politic(key=key)
    exec(self.meta[0])
    
  def choose(self, key):
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
