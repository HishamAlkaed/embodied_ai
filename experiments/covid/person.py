import numpy as np
import pygame

from experiments.covid.config import config
from simulation.agent import Agent
from simulation.utils import *


class Person(Agent):
    """
    The cockroach main class
    """
    def __init__(
            self, state, pos, v, population, age, index: int, image: str = 'experiments/covid/images/green.png'
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
        self.start_millis = 0  # Saves the time
        self.started = False
        self.age = age

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
        # avoid any obstacles in the environment
        for obstacle in self.population.objects.obstacles:
            collide = pygame.sprite.collide_mask(self, obstacle)
            if bool(collide):
                # If person gets stuck because when avoiding the obstacle ended up inside of the object,
                # resets the position to the previous one and do a 180 degree turn back
                if not self.avoided_obstacles:
                    self.prev_pos = self.pos.copy()
                    self.prev_v = self.v.copy()

                else:
                    self.pos = self.prev_pos.copy()
                    self.v = self.prev_v.copy()

                self.avoided_obstacles = True
                self.avoid_obstacle()
                return

        self.prev_v = None
        self.prev_pos = None
        self.avoided_obstacles = False

        green = 'experiments/covid/images/green_1.png'
        orange = 'experiments/covid/images/orange.png'
        red = 'experiments/covid/images/red.png'
        skull = 'experiments/covid/images/skull.png'

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
                skull, [15, config['agent']['height']]
            )
            self.v = [0, 0]

    def change_state(self) -> None:
        if self.state == 'S':
            neighbors = self.population.find_neighbors(self, config["person"]["radius_view"])
            for n in neighbors:
                if n.state == 'I':
                    self.state = 'I'
                    if self.should_die():
                        self.state = 'D'
                    break

        if self.state == 'I':
            if not self.started:
                self.start_millis = pygame.time.get_ticks()  # starter tick
                self.started = True
            seconds = (pygame.time.get_ticks() - self.start_millis) / 1000  # calculate how many seconds
            if self.started:
                self.recovered_or_not(seconds)

        elif self.state == 'D':
            print(self.age)

    def should_die(self) -> False:
        if 0 <= self.age <= 19:
            dying_prob = np.random.randint(0, config['person']['reference_group_dr'])
            if dying_prob == 1:  # 0.06% chance
                return True
        elif 20 <= self.age <= 29:
            dying_prob = np.random.randint(0, round(config['person']['reference_group_dr'] / 10))
            if dying_prob == 1:  # 0.6% chance
                return True
        elif 30 <= self.age <= 39:
            dying_prob = np.random.randint(0, round(config['person']['reference_group_dr'] / 45))
            if dying_prob == 1:
                return True
        elif 40 <= self.age <= 49:
            dying_prob = np.random.randint(0, round(config['person']['reference_group_dr'] / 130))
            if dying_prob == 1:
                return True
        elif 50 <= self.age <= 59:
            dying_prob = np.random.randint(0, round(config['person']['reference_group_dr'] / 440))
            if dying_prob == 1:
                return True
        elif self.age > 60:
            dying_prob = np.random.randint(0, round(config['person']['reference_group_dr'] / 1300))
            if dying_prob == 1:
                return True

    def recovered_or_not(self, seconds) -> None:
        if 0 <= self.age <= 19:
            random_noise = np.random.uniform(-5.89, 5.89)
            if seconds > 13.61 + random_noise:
                self.recover()
        elif 20 <= self.age <= 29:
            random_noise = np.random.uniform(-5.81, 5.81)
            if seconds > 13.97 + random_noise:
                self.recover()
        elif 30 <= self.age <= 39:
            random_noise = np.random.uniform(-6, 6)
            if seconds > 14.46 + random_noise:
                self.recover()
        elif 40 <= self.age <= 49:
            random_noise = np.random.uniform(-5.72, 5.72)
            if seconds > 14.79 + random_noise:
                self.recover()
        elif 50 <= self.age <= 59:
            random_noise = np.random.uniform(-5.9, 5.9)
            if seconds > 14.81 + random_noise:
                self.recover()
        elif self.age > 60:
            random_noise = np.random.uniform(-5.896, 5.896)
            if seconds > 14.73 + random_noise:
                self.recover()

    def recover(self) -> None:
        self.state = 'R'
        self.started = False
