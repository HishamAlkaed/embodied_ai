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
# file_to_save_to = 'experiments/covid/data_files_w4/data_0to0.10.csv' # Mo# file_to_save_to = 'experiments/covid/data_files_w4/data_0.15to0.25.csv' # Syb
# file_to_save_to = 'experiments/covid/data_files_w4/data_0.30to0.35.csv' # Denise
file_to_save_to = 'experiments/covid/data_files_w4/data_no_restrictions.csv'

def _plot_covid(data) -> None:
    """
    Plot the data related to the covid experiment. The plot is based on the number of Susceptible,
    Infected and Recovered agents

    Args:
    ----
        data:

    """
    susceptible = []
    infected = []
    recovered = []
    dead = []
    hospitalized = []
    total_dead = []
    total_recovered = []
    total_infected = []

    save_run(data)
    with open(file_to_save_to, 'r', newline='\n') as result_file:
        for i, line in enumerate(result_file):
            if i > 0:
                for index, list in enumerate(line.split(',')):
                    if index == 0:
                        susceptible.append(np.array(list[1:].replace("'", '').split(), dtype=int))
                    elif index == 1:
                        infected.append(np.array(list[1:].replace("'", '').split(), dtype=int))
                    elif index == 2:
                        recovered.append(np.array(list[1:].replace("'", '').split(), dtype=int))
                    elif index == 3:
                        dead.append(np.array(list[1:].replace("'", '').split(), dtype=int))
                    elif index == 4:
                        hospitalized.append(np.array(list[1:].replace("'", '').split(), dtype=int))
                    elif index == 5:
                        total_recovered.append(np.array(list[1:].replace("'", '').split(), dtype=int))
                    elif index == 6:
                        total_dead.append(np.array(list[1:].replace("'", '').split(), dtype=int))
                    elif index == 7:
                        total_infected.append(np.array(list[1:].replace("'", '').split(), dtype=int))

    output_name = "experiments/covid/plots/Covid-19-SIRDH%s.png" % time.strftime(
        "-%m.%d.%y_%H.%M", time.localtime()
    )

    fig = plt.figure()
    # for x in susceptible:
    #     plt.plot(x, label="Susceptible", color=(1, 0.5, 0))  # Orange
    # for x in infected:
    #     plt.plot(x, label="Infected", color=(1, 0, 0))  # Orange
    # for x in recovered:
    #     plt.plot(x, label="Recovered", color=(0, 1, 0))  # Orange
    # for x in dead:
    #     plt.plot(x, label="Dead", color=(0, 0, 0))  # Orange
    plt.plot(avgNestedLists(susceptible), label="Susceptible", color=(1, 0.5, 0))  # Orange
    plt.plot(avgNestedLists(infected), label="Infected", color=(1, 0, 0))  # Red
    plt.plot(avgNestedLists(recovered), label="Recovered", color=(0, 1, 0))  # Green
    plt.plot(avgNestedLists(dead), label="Dead", color=(0, 0, 0))  # Black
    plt.plot(avgNestedLists(hospitalized), label="Hospitalized", color=(0, 0, 1))  # Blue
    plt.title("No restrictions")
    plt.xlabel("60 Seconds (60 Days)")
    plt.ylabel("Population")
    plt.tick_params(labelbottom=False)
    plt.legend()
    # fig.savefig(output_name)
    plt.show()
    print(
        f'average dead over all runs: {avgNestedLists(total_dead)} \n average recovered over all runs: {avgNestedLists(total_recovered)} \n average infected over all runs: {50-avgNestedLists(susceptible)[-1]}')
    print('the Variance of the INFECTED PEAK is:', np.var([max(x) for x in infected]))
    print('the Standard Deviation of the INFECTED PEAK is:', np.std([max(x) for x in infected]))
    print('the Variance of the TOTAL DEAD is:', np.var(total_dead))
    print('the Standard Deviation of the TOTAL DEAD is:', np.std(total_dead))

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

def avgNestedLists(nested_vals):
    """
    Averages a 2-D array and returns a 1-D array of all of the columns
    averaged together, regardless of their dimensions.
    """
    output = []
    maximum = 0
    for lst in nested_vals:
        if len(lst) > maximum:
            maximum = len(lst)
    for index in range(maximum): # Go through each index of longest list
        temp = []
        for lst in nested_vals: # Go through each list
            if index < len(lst): # If not an index error
                temp.append(lst[index])
        output.append(np.nanmean(temp))
    return output

def save_run(data):
    start_recording()
    append_to_data(data)
    # df = pd.read_csv('experiments/covid/data.csv')
    # df['S'] = data['S']
    # df['S'] = data['S']
    # df['S'] = data['S']
    # df['S'] = data['S']

def start_recording():
    with open(file_to_save_to, 'a', newline='\n') as result_file:
        wr = csv.writer(result_file, dialect='excel')
        wr.writerow([' '])

def append_to_data(datax): # tuple left than right
    lines = str([str(datax["S"]).replace(',', ' ')[1:-1], str(datax["I"]).replace(',', ' ')[1:-1],
                 str(datax["R"]).replace(',', ' ')[1:-1], str(datax["D"]).replace(',', ' ')[1:-1],
                 str(datax["H"]).replace(',', ' ')[1:-1],
                 datax["R"][-1], datax["D"][-1], datax["I"][-1]])[1:-1] # change the copy
    with open(file_to_save_to, 'a', newline='') as result_file:
        result_file.writelines(lines) # update last line with the made copy

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

