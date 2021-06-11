from experiments.aggregation.cockroach import Cockroach
from experiments.aggregation.config import config
from simulation.utils import *
from simulation.swarm import Swarm


class Aggregations(Swarm):
    """

    """
    def __init__(self, screen_size) -> None:
        """
        This function is the initializer of the class aggregation.
        :param screen_size:
        """
        super(Aggregations, self).__init__(screen_size)
        # self.object_loc = config["aggregation"]["outside"]

    def initialize(self, num_agents: int) -> None:
        """
        Initialize the whole swarm, creating and adding the obstacle objects, and the agent, placing them inside of the
        screen and avoiding the obstacles.
        :param num_agents: int:

        """

        # add obstacle/-s to the environment if present
        object_loc = config["base"]["object_location"]

        scale_obstacle = [800, 800]

        # ''' same size setting'''
        # scale_site1 = [100, 100]
        # scale_site2 = [100, 100]

        ''' big small setting'''
        scale_site1 = [100, 100]
        scale_site2 = [150, 150]

        filename_obstacle = "experiments/flocking/images/redd.png"

        filename_site = "experiments/aggregation/images/greyc1.png"

        # add the big obstacle
        self.objects.add_object(
            file=filename_obstacle, pos=object_loc, scale=scale_obstacle, obj_type="obstacle"
        )

        # add the sites
        self.objects.add_object(
            file=filename_site, pos=[object_loc[0] + 150, object_loc[1]], scale=scale_site1, obj_type="site"
        )
        self.objects.add_object(
            file=filename_site, pos=[object_loc[0] - 150, object_loc[1]], scale=scale_site2, obj_type="site"
        )

        min_x, max_x = area(object_loc[0], scale_obstacle[0])
        min_y, max_y = area(object_loc[1], scale_obstacle[1])

        # add agents to the environment
        for index, agent in enumerate(range(num_agents)):
            coordinates = generate_coordinates(self.screen)

            # if obstacles present re-estimate the coordinates

            while (
                coordinates[0] >= max_x
                or coordinates[0] <= min_x
                or coordinates[1] >= max_y
                or coordinates[1] <= min_y
            ):
                coordinates = generate_coordinates(self.screen)

            self.add_agent(Cockroach(pos=np.array(coordinates), v=None, aggregation=self, index=index))

