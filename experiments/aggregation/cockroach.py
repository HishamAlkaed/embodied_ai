from experiments.aggregation.config import config
from simulation.agent import Agent
from simulation.utils import *


class Cockroach(Agent):
    """ """

    def __init__(
            self, pos, v, aggregation, index: int, image: str = "experiments/aggregation/images/ant.png"
    ) -> None:
        """
        Args:
        ----
            pos:
            v:
            flock:
            index (int):
            image (str): Defaults to "experiments/aggregation/images/ant.png"
        """
        super(Cockroach, self).__init__(
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
        self.aggregation = aggregation

    def update_actions(self) -> None:
        """
        Every change between frames happens here. This function is called by the method "update" in the class Swarm,
        for every agent/object. Here, it is checked if there is an obstacle in collision (in which case it avoids it by
        going to the opposite direction), align force, cohesion force and separate force between the agent and its neighbors
        is calculated, and the steering force and direction of the agent are updated
        """

        # avoid any obstacles in the environment
        for obstacle in self.aggregation.objects.obstacles:
            collide = pygame.sprite.collide_mask(self, obstacle)
            if bool(collide):
                self.avoid_obstacle()

        # do some random movement aka wandering
        wandering_force = self.wander(wander_angle=config['wandering']['wander_angle'],
                    wander_dist=config['wandering']['wander_dist'], wander_radius=config['wandering']['wander_radius'])

        # adjust the direction of the boid
        self.steering += truncate(
            wandering_force, config["roaches"]["max_force"]
        )

