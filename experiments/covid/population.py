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
        # if config["population"]["obstacles"]:
        #     object_loc = config["base"]["object_location"]
        #     scale = [250, 250]
        #
        #     filename = (
        #         "experiments/covid/images/maze.png"
        #         if config["population"]["hospital"]
        #         else "experiments/covid/images/open_square.png"
        #     )
        # #
        #     self.objects.add_object(
        #         file=filename, pos=object_loc, scale=scale, obj_type="obstacle"
        #     )
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
            deniers_pop_size = num_agents * config['population']['deniers_percentage']
            if config['population']['mask']:
                if index < deniers_pop_size:
                    if index == num_agents - 1 or index == num_agents - 2 or index == num_agents - 3:
                        self.add_agent(  # patient zero
                            Person(pos=np.array(coordinates), v=None, population=self, index=index, state='I',
                                   denier=True, age=random_age))
                    self.add_agent(
                        Person(pos=np.array(coordinates), v=None, population=self, index=index, state='S', denier=True,
                               age=random_age))
                else:
                    if index == num_agents - 1 or index == num_agents - 2 or index == num_agents - 3:
                        self.add_agent(  # patient zero
                            Person(pos=np.array(coordinates), v=None, population=self, index=index, state='I',
                                age=random_age))
                    self.add_agent(
                        Person(pos=np.array(coordinates), v=None, population=self, index=index, state='S', mask=True,
                               age=random_age))

            elif not config['population']['mask']:
                if index < deniers_pop_size:
                    if index == num_agents - 1 or index == num_agents - 2 or index == num_agents - 3:
                        self.add_agent(  # patient zero
                            Person(pos=np.array(coordinates), v=None, population=self, index=index, state='I',
                                   denier=True, age=random_age))
                    self.add_agent(
                        Person(pos=np.array(coordinates), v=None, population=self, index=index, state='S', denier=True,
                               age=random_age))
                else:
                    if index == num_agents - 1 or index == num_agents - 2 or index == num_agents - 3:
                        self.add_agent(  # patient zero
                            Person(pos=np.array(coordinates), v=None, population=self, index=index, state='I',
                                   age=random_age))
                    self.add_agent(
                        Person(pos=np.array(coordinates), v=None, population=self, index=index, state='S',
                               age=random_age))

    def add_house(self, pos):
        self.objects.add_object(
            file='experiments/covid/images/square.png', pos=pos, scale=[70, 70], obj_type="site"
        )

    def remove_house(self, pos):
        for i, house in enumerate(self.objects.sites):
            if house.pos[0] == pos[0] and house.pos[1] == pos[1]:
                house.kill()

    def add_hospital(self, pos):
        self.objects.add_object(
            file='experiments/covid/images/hospital.png', pos=pos, scale=[40, 40], obj_type="obstacle"
        )

    def remove_hospital(self, pos):
        for i, hospital in enumerate(self.objects.obstacles):
            if hospital.pos[0] == pos[0] and hospital.pos[1] == pos[1]:
                hospital.kill()

    def count_hospitals(self):
        x = 0
        for hospital in self.objects.obstacles:
            x += 1
        return x