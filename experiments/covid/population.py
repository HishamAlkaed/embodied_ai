from experiments.covid.config import config
from experiments.covid.person import Person
from simulation.swarm import Swarm
from simulation.utils import *


class Population(Swarm):
    """Class that represents the Population for the Covid experiment. TODO"""

    def __init__(self, screen_size) -> None:
        super(Population, self).__init__(screen_size)
        # Todo

    def initialize(self, num_agents: int) -> None:
        """
        Args:
            num_agents (int):

        """
        # add obstacle/-s to the environment if present
        if config["population"]["obstacles"]:
            object_loc = config["base"]["object_location"]
            scale = [400, 400]

            filename = (
                "experiments/covid/images/maze.png"
                if config["population"]["maze"]
                else "experiments/covid/images/open_square.png"
            )
        #
            self.objects.add_object(
                file=filename, pos=object_loc, scale=scale, obj_type="obstacle"
            )
        # ToDo: code snippet (not complete) to avoid initializing agents on obstacles
        # given some coordinates and obstacles in the environment, this repositions the agent
        for index, agent in enumerate(range(num_agents)):
            coordinates = generate_coordinates(self.screen)
            if config["population"]["obstacles"]:  # you need to define this variable
                for obj in self.objects.obstacles:
                    rel_coordinate = relative(
                        coordinates, (obj.rect[0], obj.rect[1])
                    )
                    try:
                        while obj.mask.get_at(rel_coordinate):
                            coordinates = generate_coordinates(self.screen)
                            rel_coordinate = relative(
                                coordinates, (obj.rect[0], obj.rect[1])
                            )
                    except IndexError:
                        pass
            random_age = random.randint(1, 95)
            mask_pop_size = num_agents * config['population']['mask_percentage']

            if index <= mask_pop_size:
                if index == num_agents-1 or index == num_agents-2:
                    self.add_agent(  # patient zero
                        Person(pos=np.array(coordinates), v=None, population=self, index=index, state='I', mask=True, age=random_age))
                self.add_agent(
                    Person(pos=np.array(coordinates), v=None, population=self, index=index, state='S', mask=True, age=random_age))
            else:
                if index == num_agents-1 or index == num_agents-2:
                    self.add_agent(  # patient zero
                        Person(pos=np.array(coordinates), v=None, population=self, index=index, state='I', age=random_age))
                self.add_agent(Person(pos=np.array(coordinates), v=None, population=self, index=index, state='S', age=random_age))

    def add_house(self, pos):
        self.objects.add_object(
            file='experiments/covid/images/square.png', pos=pos, scale=[90, 90], obj_type="obstacle"
        )

    def remove_house(self, pos):
        for i, house in enumerate(self.objects.obstacles):
            if house.pos[0] == pos[0] and house.pos[1] == pos[1]:
                # self.objects.obstacles[i].remove()
                # print(house.pos, pos)
                house.kill()
        #
        #     min_x, max_x = area(object_loc[0], scale[0])
        #     min_y, max_y = area(object_loc[1], scale[1])
        #
        # # add agents to the environment
        # for index, agent in enumerate(range(num_agents)):
        #     coordinates = generate_coordinates(self.screen)
        #
        #     # if obstacles present re-estimate the corrdinates
        #     if config["flock"]["obstacles"]:
        #         if config["flock"]["outside"]:
        #             while (
        #                     max_x >= coordinates[0] >= min_x
        #                     and max_y >= coordinates[1] >= min_y
        #             ):
        #                 coordinates = generate_coordinates(self.screen)
        #         else:
        #             while (
        #                 coordinates[0] >= max_x
        #                 or coordinates[0] <= min_x
        #                 or coordinates[1] >= max_y
        #                 or coordinates[1] <= min_y
        #             ):
        #                 coordinates = generate_coordinates(self.screen)
        #
        #     self.add_agent(Boid(pos=np.array(coordinates), v=None, flock=self, index=index))