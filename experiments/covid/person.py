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
        self.denier = denier

    def update_actions(self) -> None:
        """
        Every change between frames happens here. This function is called by the method "update" in the class Swarm,
        for every agent/object. Here, it is checked if there is an obstacle in collision (in which case it avoids it by
        going to the opposite direction), align force, cohesion force and separate force between the agent and its neighbors
        is calculated, and the steering force and direction of the agent are updated
        """
        self.general_behaviour()
        self.change_state()
        self.population.datapoints.append(self.state)

    def general_behaviour(self) -> None:
        ''' this function:
            1) checks for collisions with any obstacles
            2) ensures the right image/color for each individual in each state
        '''

        # avoid any obstacles in the environment

        # for obstacle in self.population.objects.obstacles:
        #     collide = pygame.sprite.collide_mask(self, obstacle)
        #     if bool(collide):
        #         # If person gets stuck because when avoiding the obstacle ended up inside of the object,
        #         # resets the position to the previous one and do a 180 degree turn back
        #         if not self.avoided_obstacles:
        #             self.prev_pos = self.pos.copy()
        #             self.prev_v = self.v.copy()
        #             # print(obstacle.rect, obstacle.pos, self.pos)
        #             if obstacle.rect[0] < self.pos[0] < obstacle.rect[0]+obstacle.rect[2] and \
        #                     obstacle.rect[1] < self.pos[1] < obstacle.rect[1]+obstacle.rect[3] and\
        #                     all(self.v) != 0 and any([n for n in self.population.find_neighbors(self, config["person"]["radius_view"]) \
        #                                               if all(n.v) == 0 and n.state == 'I']):
        #                 # print('\n', obstacle.rect, obstacle.pos, self.pos)
        #                 self.pos = np.array([self.pos[0] - obstacle.rect[2], self.pos[1]])
        #                 self.v = [-self.v[0], -self.v[1]]
        #                 return
        #         else:
        #             self.pos = self.prev_pos.copy()
        #             self.v = self.prev_v.copy()
        #
        #         self.avoided_obstacles = True
        #         self.avoid_obstacle()
        #         return
        #
        # self.prev_v = None
        # self.prev_pos = None
        # self.avoided_obstacles = False
        if self.wearing_mask:
            green = 'experiments/covid/images/green_mask.png'  # for recovered
            orange = 'experiments/covid/images/orange_mask.png'  # for susceptible
            red = 'experiments/covid/images/red_mask.png'  # for infected
        elif not self.wearing_mask:
            green = 'experiments/covid/images/green_1.png'  # for recovered
            orange = 'experiments/covid/images/orange.png'  # for susceptible
            red = 'experiments/covid/images/red.png'  # for infected

        skull = 'experiments/covid/images/skull.png'  # for dead
        if self.state == 'S':
            self.image, self.rect = image_with_rect(
                orange, [config['agent']['width'], config['agent']['height']]
        )
        elif self.state == 'R':
            self.image, self.rect = image_with_rect(
                green, [config['agent']['width'], config['agent']['height']]
            )
        elif self.state == 'I':
            self.image, self.rect = image_with_rect(
                red, [config['agent']['width'], config['agent']['height']]
            )
        elif self.state == 'D':
            self.image, self.rect = image_with_rect(
                skull, [int(config['agent']['width']*1.5), config['agent']['height']]
            )
            self.v = [0, 0]

    def change_state(self) -> None:
        if self.state == 'S':
            # if susceptible, check each frame rate your neighbors and if any of them is infected u r infected
            if not self.started_incubation:
                neighbors = self.population.find_neighbors(self, config["person"]["radius_view"])
                for n in neighbors:
                    if n.state == 'I' and not all(n.v) == 0:
                        if self.infectable():  # if you have a chance to get infected
                            if self.wearing_mask:
                                if not self.mask_prevention():  # if the mask can prevent the agent from getting infected
                                    break
                                elif self.mask_prevention(): # if not then start the incubation time
                                    self.start_millis_incubation = pygame.time.get_ticks()  # starter tick
                                    self.started_incubation = True
                                    # print(n.v)
                                    break
                            else:   # if no mask
                                self.start_millis_incubation = pygame.time.get_ticks()  # starter tick
                                self.started_incubation = True
                                # print(n.v)
                                break
            elif self.started_incubation:
                self.incubation()

        elif self.state == 'I':
            # if infected start timer and check each frame rate whether it has been already enough time to recover or not (given tha age)
            if not self.started_recovery:
                self.start_millis_recovery = pygame.time.get_ticks()  # starter tick
                self.started_recovery = True
            seconds_r = (pygame.time.get_ticks() - self.start_millis_recovery) / 1000  # calculate how many seconds
            if self.started_recovery:
                self.recovered_or_not(seconds_r)
            if self.index != config['base']['n_agents'] - 1 and self.index != config['base']['n_agents'] - 2\
                    and self.index != config['base']['n_agents'] - 3:
                    # and self.index !=  config['base']['n_agents'] - 4\
                    # and self.index !=  config['base']['n_agents'] - 5: # patient zero
                if not self.started_quarantine:
                    self.start_millis_quarantine = pygame.time.get_ticks()  # starter tick
                    self.started_quarantine = True
                if self.started_quarantine:
                    if not self.rand_noise_bol:
                        # self.rand_noise = np.random.uniform(2, 5)
                        self.rand_noise_bol = True
                    elif self.rand_noise_bol:
                        seconds_q = (
                            pygame.time.get_ticks() - self.start_millis_quarantine) / 1000  # calculate how many seconds
                        if seconds_q > 1:
                            if not self.denier:
                                # print(self.index)
                                if not self.asymptomatic():
                                    self.add_house()
                                    self.started_quarantine = False
        elif self.state == 'R' and all(self.v) == 0:
            self.recover()

    def mask_prevention(self) -> False: # 50% lower chance to get infected with mask
        if not self.mask_bol:
            self.random_chance_mask = np.random.randint(0, 100)
            self.mask_bol = True
        elif self.mask_bol and self.random_chance_mask < 38:
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
        if self.assym_bol and self.assym_chance < 30:
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

        self.population.remove_house(self.pos)
        self.v = self.set_velocity()
        self.recover_bol = False

    def add_house(self):
        self.v = [0, 0]
        self.population.add_house(self.pos)