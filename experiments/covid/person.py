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
            self, state, pos, v, population, index: int, image: str = 'experiments/covid/images/green.png'
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

    def change_state(self) -> None:
        if self.state == 'S':
            neighbors = self.population.find_neighbors(self, config["person"]["radius_view"])
            for n in neighbors:
                if n.state == 'I':
                    self.state = 'I'
                    break
            # random_n = np.random.randint(0, 10000)
            # if random_n == 7648:
            #     self.state = 'I'

        if self.state == 'I':
            if not self.started:
                self.start_millis = pygame.time.get_ticks()  # starter tick
                self.started = True
            seconds = (pygame.time.get_ticks() - self.start_millis) / 1000  # calculate how many seconds
            random_noise = np.random.normal(0, 3)
            if self.started and seconds > 15 + random_noise:
                self.state = 'R'
