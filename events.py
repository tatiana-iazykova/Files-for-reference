import numpy as np

class Rules:
  def __init__(self, everybody, stats):
    self.everybody=everybody
    self.stats=stats

  def check_stats(self, politic, stat):
    try:
      return getattr(politic, stat)
    except:
        return False

  def update_points(self, politic):
    assert politic.points
    self.stats[politic.name] = politic.points

  def dice(self, fair=True):
    if fair:
      return np.random.rand()
    else:
      return np.random.rand()+0.25

  def take_bribes(self, politic, c=None):
    c = self.check_stats(politic, 'corrupt')
    if c or politic.money > 50000:
      prob = self.dice(fair=False)
    else:
      prob = self.dice()
    if prob > 0.5:
      politic.corrupt = True
      politic.minus_points(num = 5)
    self.update_points(politic)

  def gives_to_charity(self, politic):
    corrupt = self.check_stats(politic, 'corrupt')
    prob = 0
    if corrupt:
      prob =  self.dice() 
    charity = self.check_stats(politic, 'charity')
    if prob > 0.5:
      self.take_bribes(politic, c=True)
    elif charity:
      if charity < 10:
        politic.charity += 2
        politic.plus_points(num=1)
      elif charity < 50:
        politic.charity += 2
        politic.plus_points(num=5)
      elif charity > 50:
        politic.charity += 2
        politic.plus_points(num=15)
    else:
      politic.charity = 1
      politic.plus_points(num=1)
    self.update_points(politic)

  def loses_election(self, politic):
    election = self.check_stats(politic, 'election')
    if election == 'lose':
      if politic.party == 'UR':
        self.unfair_game(fair= False)
      else:
        self.unfair_game(fair= True)
    else:
      if politic.party != 'UR':
        self.unfair_game(fair= True)
      else:
        self.unfair_game(fair= False)    

  def unfair_game(self, fair=True):
    if fair:
      for pol in self.everybody.values():
        if pol.party == 'UR':
          pol.plus_points(num = 2)
        else:
          pol.minus_points(num = 2)
        self.update_points(pol)
    else:
      for pol in self.everybody.values():
        if pol.party != 'UR':
          pol.plus_points(num = 2)
        else:
          pol.minus_points(num = 2)
        self.update_points(pol)  

  def gain_power(self, politic):
    if self.dice > 0.5:
      politic.power += 7
    else:
      politic.power += 2
  
  def super_power(self, politic):
    politic.special()
    self.update_points(politic)
