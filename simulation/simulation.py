import sys
import time

import numpy as np
import matplotlib.pyplot as plt
import pygame
import pandas as pd
import csv
from typing import Union, Tuple

from experiments.aggregation.aggregation import Aggregations
from experiments.covid.population import Population
from experiments.flocking.flock import Flock

counter_inside_right = 0 # counts the number of roaches in the right site
counter_inside_left = 0 # counts the number of roaches in the left site


# def append_to_data(data_tuple): # tuple left than right
#     right_data = open('experiments/aggregation/data_right_bs.csv', 'r+') # open file for reading
#     left_data = open('experiments/aggregation/data_left_bs.csv', 'r+')
#     right_lines = right_data.readlines() # read lines
#     left_lines = left_data.readlines()
#
#     if not right_lines[-1][-1].isnumeric():
#         right_lines[-1] += str(data_tuple[1])  # change the copy
#         left_lines[-1] += str(data_tuple[0])
#     else:
#         right_lines[-1] += ',' + str(data_tuple[1])  # change the copy
#         left_lines[-1] += ',' + str(data_tuple[0])
#
#     with open('experiments/aggregation/data_right_bs.csv', 'w+', newline='') as result_file:
#         # wr = csv.writer(result_file, dialect='excel')
#         # print(right_list)
#         result_file.writelines(right_lines) # update last line with the made copy
#     with open('experiments/aggregation/data_left_bs.csv', 'w+', newline='') as result_file:
#         # wr = csv.writer(result_file, dialect='excel')
#         result_file.writelines(left_lines)
#
#
# def start_recording():
#     with open('experiments/aggregation/data_right_bs.csv', 'a', newline='\n') as result_file:
#         wr = csv.writer(result_file, dialect='excel')
#         wr.writerow([' '])
#     with open('experiments/aggregation/data_left_bs.csv', 'a', newline='\n') as result_file:
#         wr = csv.writer(result_file, dialect='excel')
#         wr.writerow([' '])
#
#
# def save_history(object, start_time):
#     global counter_inside_left
#     global counter_inside_right
#     if int(str(time.time() - start_time).split('.')[0]) % 5 == 0 and int(str(time.time() - start_time).split('.')[1][0]) == 0:
#         for agent in object.swarm.agents:
#             collide1 = pygame.sprite.collide_mask(agent, object.swarm.objects.sites.sprites()[0])
#             collide2 = pygame.sprite.collide_mask(agent, object.swarm.objects.sites.sprites()[1])
#             if collide1 and all(agent.v) == 0:
#                 counter_inside_right += 1
#             elif collide2 and all(agent.v) == 0:
#                 counter_inside_left += 1
#         # list_right.append(counter_inside_right)
#         # list_left.append(counter_inside_left)
#         append_to_data(tuple((counter_inside_left, counter_inside_right)))
#
#         counter_inside_left = 0
#         counter_inside_right = 0


def _plot_covid(data) -> None:
    """
    Plot the data related to the covid experiment. The plot is based on the number of Susceptible,
    Infected and Recovered agents

    Args:
    ----
        data:

    """
    output_name = "experiments/covid/plots/Covid-19-SIR%s.png" % time.strftime(
        "-%m.%d.%y-%H:%M", time.localtime()
    )
    fig = plt.figure()
    plt.plot(data["S"], label="Susceptible", color=(1, 0.5, 0))  # Orange
    plt.plot(data["I"], label="Infected", color=(1, 0, 0))  # Red
    plt.plot(data["R"], label="Recovered", color=(0, 1, 0))  # Green
    plt.plot(data["D"], label="Dead", color=(0, 0, 0))  # Black
    plt.title("Covid-19 Simulation S-I-R")
    plt.xlabel("Time")
    plt.ylabel("Population")
    plt.legend()
    fig.savefig(output_name)
    plt.show()


def _plot_flock() -> None:
    """Plot the data related to the flocking experiment. TODO"""
    pass


def _plot_aggregation() -> None:
    """Plot the data related to the aggregation experiment. TODO"""

    df_right = pd.read_csv('experiments/aggregation/data_right_bs.csv')
    df_left = pd.read_csv('experiments/aggregation/data_left_bs.csv')

    plt.plot(df_right.mean(), color=(1, 0, 0))  # red
    plt.plot(df_left.mean(), color=(0, 1, 0))  # green
    plt.xlabel("5 sec interval")
    plt.ylabel('n of cockroaches')
    plt.xticks([])
    plt.title('Different size sites')
    plt.show()


"""
General simulation pipeline, suitable for all experiments 
"""


class Simulation:
    """
    This class represents the simulation of agents in a virtual space.
    """

    def __init__(
            self,
            num_agents: int,
            screen_size: Union[Tuple[int, int], int],
            swarm_type: str,
            iterations: int):
        """
        Args:
        ----
            num_agents (int):
            screen_size (Union[Tuple[int, int], int]):
            swarm_type (str):
            iterations (int):
        """
        # general settings
        self.screensize = screen_size
        self.screen = pygame.display.set_mode(screen_size)
        self.sim_background = pygame.Color("gray21")
        # self.sim_background = pygame.Color("white")
        self.iter = iterations
        self.swarm_type = swarm_type

        # swarm settings
        self.num_agents = num_agents
        if self.swarm_type == "flock":
            self.swarm = Flock(screen_size)

        elif self.swarm_type == "aggregation":
            self.swarm = Aggregations(screen_size)

        elif self.swarm_type == "covid":
            self.swarm = Population(screen_size)

        else:
            print("None of the possible swarms selected")
            sys.exit()

        # update
        self.to_update = pygame.sprite.Group()
        self.to_display = pygame.sprite.Group()
        self.running = True

    def plot_simulation(self) -> None:
        """Depending on the type of experiment, plots the final data accordingly"""
        if self.swarm_type == "covid":
            _plot_covid(self.swarm.points_to_plot)

        elif self.swarm_type == "Flock":
            _plot_flock()

        elif self.swarm_type == "aggregation":
            _plot_aggregation()

    def initialize(self) -> None:
        """Initialize the swarm, specifying the number of agents to be generated"""

        # initialize a swarm type specific environment
        self.swarm.initialize(self.num_agents)

    def simulate(self) -> None:
        """Here each frame is computed and displayed"""
        self.screen.fill(self.sim_background)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        self.swarm.update()
        self.swarm.display(self.screen)

        pygame.display.flip()

    def run(self) -> None:

        """
        Main cycle where the initialization and the frame-by-frame computation is performed.
        The iteration con be infinite if the parameter iter was set to -1, or with a finite number of frames
        (according to iter)
        When the GUI is closed, the resulting data is plotted according to the type of the experiment.
        """
        # initialize the environment and agent/obstacle positions
        self.initialize()
        # the simulation loop, infinite until the user exists the simulation
        # finite time parameter or infinite

        if self.iter == float("inf"):
            # start_recording()
            # start_time = time.time()
            while self.running:
                # init = time.time()
                self.simulate()
                # save_history(self, start_time)
            self.plot_simulation()
        else:
            # start_recording()
            # start_time = time.time()
            for i in range(self.iter):
                self.simulate()
                # save_history(self, start_time)
            self.plot_simulation()

