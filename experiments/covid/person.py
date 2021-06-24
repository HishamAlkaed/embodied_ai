import numpy as np
import pygame

from experiments.covid.config import config
from simulation.agent import Agent
from simulation.utils import *
from simulation.objects import Objects
from simulation.swarm import Swarm


class Person(Agent):
  """
  The Person main class
  """
  def __init__(
      self, state, pos, v, population, age, index: int, mask=False, denier=False, image: str = 'experiments/covid/images/orange.png'
  ) -> None:
    """
    Args:
    ----
        pos:
        v:
        aggregation:
        index (int):
        image (str): Defaults to ""
    """
    super(Person, self).__init__(
      pos,
      v,
      image,
      max_speed=config["agent"]["max_speed"],
      min_speed=config["agent"]["min_speed"],
      width=config["agent"]["width"],
      height=config["agent"]["height"],
      mass=config["agent"]["mass"],
      dT=config["agent"]["dt"],
      index=index
    )
    self.population = population
    self.state = state

    self.avoided_obstacles: bool = False
    self.prev_pos = None
    self.prev_v = None
    self.start_millis_recovery = 0  # Saves the time for recovery time
    self.started_recovery = False  # boolean that indicates whether timer has started or not yet (recovery time)
    self.start_millis_quarantine = 0
    self.started_quarantine = False
    self.start_millis_incubation = 0
    self.started_incubation = False
    self.age = age
    self.objects = Objects()
    self.swarm = Swarm([config['screen']['width'], config['screen']['height']])
    self.rand_noise = 0 # going from infected to in house
    self.rand_noise_bol = False
    self.recover_var = 0
    self.recover_bol = False
    self.wearing_mask = mask
    self.random_chance_mask = 0
    self.mask_bol = False
    self.random_chance = 0
    self.infect_bol = False
    self.assym_chance = 0
    self.assym_bol = False
    self.asymp_bol = False
    self.random_chance_asymp = 0
    self.denier = denier
    self.isolation_in_incubation_bol = False
    self.chance_isolation_in_incubation = 0
    self.preventive_isolation_timer = 0
    self.preventive_isolation_bol = False
    self.previous_time = pygame.time.get_ticks()
    self.speed_before_curfew = self.v
    self.checked_into_hos = False
    self.no_place_in_hospital = False

  def update_actions(self) -> None:
    """
    Every change between frames happens here. This function is called by the method "update" in the class Swarm,
    for every agent/object. Here, it is checked if there is an obstacle in collision (in which case it avoids it by
    going to the opposite direction), align force, cohesion force and separate force between the agent and its neighbors
    is calculated, and the steering force and direction of the agent are updated
    """
    self.general_behaviour()
    self.change_state()
    self.apply_curfew()
    self.population.datapoints.append(self.state)

  def general_behaviour(self) -> None:
    ''' this function:
        1) ensures the right image/color for each individual in each state
    '''

    if self.wearing_mask:
      green = 'experiments/covid/images/green_mask.png'  # for recovered
      orange = 'experiments/covid/images/orange_mask.png'  # for susceptible
      red = 'experiments/covid/images/red_mask.png'  # for infected
      purple = 'experiments/covid/images/purple.png' # TODO
    elif not self.wearing_mask:
      green = 'experiments/covid/images/green_1.png'  # for recovered
      orange = 'experiments/covid/images/orange.png'  # for susceptible
      red = 'experiments/covid/images/red.png'  # for infected
      purple = 'experiments/covid/images/purple.png'

    # skull = 'experiments/covid/images/skull.png'  # for dead
    if self.state == 'S':
      self.image, self.rect = image_with_rect(
        orange, [config['agent']['width'], config['agent']['height']]
      )
    elif self.state == 'R':
      self.image, self.rect = image_with_rect(
        green, [config['agent']['width'], config['agent']['height']]
      )
    elif self.state == 'I' or 'H':
      if self.no_place_in_hospital == True:
        self.image, self.rect = image_with_rect(
          purple, [config['agent']['width'], config['agent']['height']]
        )
      else:
        self.image, self.rect = image_with_rect(
          red, [config['agent']['width'], config['agent']['height']]
        )
  def apply_curfew(self):
    if config['population']['curfew']:
      if self.denier or self.state == 'D':
        pass
      else:
        if (pygame.time.get_ticks() - self.previous_time) < 500: # no curfew
          if not self.in_house(self.pos) and not self.in_hospital(self.pos):
            self.v = self.speed_before_curfew
        elif 500 < (pygame.time.get_ticks() - self.previous_time) < 1000: # curfew
          if any(self.v) != 0:
            self.speed_before_curfew = self.v
            self.v = [0,0]
        elif (pygame.time.get_ticks() - self.previous_time) > 1000: # reset timer
          self.previous_time = pygame.time.get_ticks()

  def change_state(self) -> None:
    # if 10 < (pygame.time.get_ticks() / 1000) < 15:
    if self.state == 'S':
      # if susceptible, check your neighbors each frame rate
      if not self.started_incubation:
        if not self.denier and self.preventive_isolation_bol:
          self.preventive_isolation()
        neighbors = self.population.find_neighbors(self, config["person"]["radius_view"])
        for n in neighbors:
          if n.state == 'I' and not all(n.v) == 0 and not all(self.v) == 0:
            if self.preventive_isolation_chance():  # 15% chance to go in self preventive quarantine
              # if you have a chance to get infected & called only once for the agent that caused us to go in preventive quarantine
              if self.infectable() and not self.preventive_isolation_bol: # preventive_isolation_bol becomes true once preventive_isolation is called
                if self.wearing_mask and not self.mask_prevention(n): # if u wear a mask and it prevents you from infection
                  break
                else:   # else if  no mask or if mask but that doesnt prevent you from infection
                  if n.asymptomatic():
                    if self.asymptomatic_chance():
                      self.start_incubation_timer()
                      break
                  else:
                    self.start_incubation_timer()
                    break
              if not self.denier:
                self.preventive_isolation()
            if not self.preventive_isolation_chance() and self.infectable():  # if you have a chance to get infected
              if self.wearing_mask and not self.mask_prevention(n): # if u wear a mask and it prevents you from infection
                break
              else:   # else if  no mask or if mask but that doesnt prevent you from infection
                if n.asymptomatic():
                  if self.asymptomatic_chance():
                    self.start_incubation_timer()
                    break
                else:
                  self.start_incubation_timer()
                  break

      elif self.started_incubation:
        self.incubation()

    elif self.state == 'I':
      # if infected start timer and check each frame rate whether it has been already enough time to recover or not (given tha age)
      if not self.no_place_in_hospital:
        if not self.started_recovery:
          self.start_millis_recovery = pygame.time.get_ticks()  # starter tick
          self.started_recovery = True
        elif self.started_recovery:
          seconds_r = (pygame.time.get_ticks() - self.start_millis_recovery) / 1000  # calculate how many seconds
          self.recovered_or_not(seconds_r)
          if not self.asymptomatic() and not self.in_house(self.pos):
            if config['population']['hospital']:
              if self.chance_to_hospitalize():
                self.state = 'H'
                self.checked_into_hos = True
                return
              self.checked_into_hos = True
            if self.index != config['base']['n_agents'] - 1 and self.index != config['base']['n_agents'] - 2 \
                and self.index != config['base']['n_agents'] - 3 and not self.denier:
              if not self.started_quarantine:
                self.start_millis_quarantine = pygame.time.get_ticks()  # starter tick
                self.started_quarantine = True
              if self.started_quarantine:
                if not self.rand_noise_bol:
                  self.rand_noise_bol = True
                  # here generate random noise if needed
                elif self.rand_noise_bol:
                  seconds_q = (
                                  pygame.time.get_ticks() - self.start_millis_quarantine) / 1000  # calculate how many seconds
                  if seconds_q > 1:
                    self.add_house()
                    self.started_quarantine = False
      else:
        if self.population.count_hospitals() <= 1:
          self.population.add_hospital(self.pos)
          self.state = 'H'
          self.checked_into_hos = True
          self.no_place_in_hospital = False
          self.v = [0,0]

    elif self.state == 'R' and all(self.v) == 0:
      self.recover()

    elif self.state == 'H':
      if not self.in_hospital(self.pos):
        self.go_to_hospital()
      if not self.started_recovery:
        self.start_millis_recovery = pygame.time.get_ticks()  # starter tick
        self.started_recovery = True
      elif self.started_recovery:
        seconds_r = (pygame.time.get_ticks() - self.start_millis_recovery) / 1000  # calculate how many seconds
        self.recovered_or_not(seconds_r)

    elif self.state == 'D':
      skull = 'experiments/covid/images/skull.png'  # for dead
      self.image, self.rect = image_with_rect(
        skull, [int(config['agent']['width'] * 1.5), config['agent']['height']]
      )
      self.v = [0,0]

  def go_to_hospital(self):
    self.state = 'H'
    if not self.in_hospital(self.pos):
      self.population.add_hospital(self.pos)
    self.v = [0, 0]

  def chance_to_hospitalize(self) -> False:
    # if true, u should be hospitalized
    if not self.checked_into_hos:
      number_of_hospitals = self.population.count_hospitals()
      if 0 <= self.age <= 4:
        hos_prob = np.random.randint(0, round(config['person']['reference_group_hr']/3))
      elif 5 <= self.age <= 17:
        hos_prob = np.random.randint(0, round(config['person']['reference_group_hr']))
      elif 18 <= self.age <= 49:
        hos_prob = np.random.randint(0, round(config['person']['reference_group_hr'] / 25))
      elif 50 <= self.age <= 64:
        hos_prob = np.random.randint(0, round(config['person']['reference_group_hr'] / 65))
      elif 65 <= self.age < 85:
        hos_prob = np.random.randint(0, round(config['person']['reference_group_hr'] / 138))
      elif self.age >= 85:
        hos_prob = np.random.randint(0, round(config['person']['reference_group_hr'] / 172))
      if hos_prob == 0:  # 0.3% chance
        if number_of_hospitals <= 1:
          return True
        else:
          self.no_place_in_hospital = True
          if np.random.randint(0, 100) < 15:
            self.state = 'D'

  def asymptomatic_chance(self) -> False: # 42% lower chance to get infected if the contageous person is asymptomatic
    if not self.asymp_bol:
      self.random_chance_asymp = np.random.randint(0, 100)
      self.asymp_bol = True
    elif self.asymp_bol and self.random_chance_asymp < 42:
      return True

  def mask_prevention(self, neighbor) -> False: # 50% lower chance to get infected with mask
    if not self.mask_bol:
      self.random_chance_mask = np.random.randint(0, 100)
      self.mask_bol = True
    elif self.mask_bol:
      if self.wearing_mask and neighbor.wearing_mask:
        if self.random_chance_mask <= 2:
          return True
      elif not self.wearing_mask and neighbor.wearing_mask:
        if self.random_chance_mask < 5:
          return True
      elif self.wearing_mask and not neighbor.wearing_mask:
        if self.random_chance_mask < 70:
          return True

  def infectable(self) -> False: # 10% chance to get infected
    if not self.infect_bol:
      self.random_chance = np.random.randint(0, 100)
      self.infect_bol = True
    elif self.infect_bol and self.random_chance < 90:
      return True

  def asymptomatic(self) -> False: # true if you are asymptomatic
    if not self.assym_bol:
      self.assym_chance = np.random.randint(0, 100) # 30%
      self.assym_bol = True
    if self.assym_bol and self.assym_chance < 17:
      return True

  def incubation(self):
    seconds_i = (pygame.time.get_ticks() - self.start_millis_incubation) / 1000  # calculate how many seconds
    if self.age < 30 and seconds_i > 4.95:
      self.infected()
    elif 30 <= self.age <= 39 and seconds_i > 5.78:
      self.infected()
    elif 40 <= self.age <= 49 and seconds_i > 5.33:
      self.infected()
    elif 50 <= self.age <= 59 and seconds_i > 6.34:
      self.infected()
    elif 60 <= self.age <= 69 and seconds_i > 4.69:
      self.infected()
    elif self.age >= 70 and seconds_i > 7.56:
      self.infected()

  def preventive_isolation(self):
    if not self.preventive_isolation_bol:
      self.add_house()
      self.v = [0, 0]
      self.preventive_isolation_timer = pygame.time.get_ticks()
      self.preventive_isolation_bol = True
    if self.preventive_isolation_bol:
      seconds_p = (pygame.time.get_ticks() - self.preventive_isolation_timer) / 1000
      if seconds_p >= 10:
        if not self.state == 'I':
          self.population.remove_house(self.pos)
          self.v = self.set_velocity()
        self.preventive_isolation_bol = False

  def preventive_isolation_chance(self) -> False:
    if not self.isolation_in_incubation_bol:
      self.chance_isolation_in_incubation = np.random.randint(0, 100)
      self.isolation_in_incubation_bol = True
    elif self.isolation_in_incubation_bol and self.chance_isolation_in_incubation < 15:
      return True

  def infected(self):
    self.started_incubation = False
    self.state = 'I'
    if not self.asymptomatic():
      self.max_speed = self.max_speed / 3
    if self.should_die():  # once infected it is checked (only once), given the age, the probability to die
      self.state = 'D'

  def should_die(self) -> False:
    # the values used beneath are based upon this research:
    # https://www.cdc.gov/coronavirus/2019-ncov/covid-data/investigations-discovery/hospitalization-death-by-age.html
    if 10 <= self.age <= 19:
      dying_prob = np.random.randint(0, config['person']['reference_group_dr'])
      if dying_prob == 1:  # 0.06% chance
        return True
    elif 20 <= self.age <= 29:
      dying_prob = np.random.randint(0, round(config['person']['reference_group_dr']))
      if dying_prob == 1:  # 10x higher chance to die than the reference age group
        return True
    elif 30 <= self.age <= 39:
      dying_prob = np.random.randint(0, round(config['person']['reference_group_dr']))
      if dying_prob == 1:  # 45x higher chance to die than the reference age group
        return True
    elif 40 <= self.age <= 49:
      dying_prob = np.random.randint(0, round(config['person']['reference_group_dr'] / 2))
      if dying_prob == 1:  # 130x higher chance to die than the reference age group
        return True
    elif 50 <= self.age <= 59:
      dying_prob = np.random.randint(0, round(config['person']['reference_group_dr'] / 6.5))
      if dying_prob == 1:  # 440x higher chance to die than the reference age group
        return True
    elif 60 <= self.age <= 69:
      dying_prob = np.random.randint(0, round(config['person']['reference_group_dr'] / 18))
      if dying_prob == 1:  # 440x higher chance to die than the reference age group
        return True
    elif 70 <= self.age <= 79:
      dying_prob = np.random.randint(0, round(config['person']['reference_group_dr'] / 40))
      if dying_prob == 1:  # 440x higher chance to die than the reference age group
        return True
    elif self.age >= 80:
      dying_prob = np.random.randint(0, round(config['person']['reference_group_dr'] / 74))
      if dying_prob == 1:  # 1300x higher chance to die than the reference age group
        return True

  def recovered_or_not(self, seconds) -> None:
    # the values used beneath are based upon this research:
    #   https://www.worldometers.info/coronavirus/coronavirus-age-sex-demographics/
    if not self.recover_bol:
      self.recover_var = np.random.uniform(-5.81, 5.81)
      self.recover_bol = True
    elif self.recover_bol:
      if 0 <= self.age <= 19 and seconds > 13.61 + self.recover_var:
        self.recover()
      elif 20 <= self.age <= 29 and seconds > 13.97 + self.recover_var:
        self.recover()
      elif 30 <= self.age <= 39 and seconds > 14.46 + self.recover_var:
        self.recover()
      elif 40 <= self.age <= 49 and seconds > 14.79 + self.recover_var:
        self.recover()
      elif 50 <= self.age <= 59 and seconds > 14.81 + self.recover_var:
        self.recover()
      elif self.age >= 60 and seconds > 14.73 + self.recover_var:
        self.recover()

  def recover(self) -> None:
    # simple helper method to avoid code repetition
    self.state = 'R'
    self.started_recovery = False
    if self.in_house(self.pos):
      self.population.remove_house(self.pos)
    elif self.in_hospital(self.pos):
      self.population.remove_hospital(self.pos)
    self.v = self.set_velocity()
    self.recover_bol = False

  def add_house(self):
    self.v = [0, 0]
    self.population.add_house(self.pos)

  def start_incubation_timer(self):
    self.start_millis_incubation = pygame.time.get_ticks()  # starter tick
    self.started_incubation = True

  def in_house(self, pos) -> False:
    for site in self.population.objects.sites:
      if site.pos[1] == pos[1] and site.pos[0] == pos[0]:
        return True

  def in_hospital(self, pos) -> False:
    for obs in self.population.objects.obstacles:
      if obs.pos[1] == pos[1] and obs.pos[0] == pos[0]:
        return True
