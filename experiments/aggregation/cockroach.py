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
        self.state = 'wandering'

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

        # print(self.state)
        self.change_state()
        self.site_behaviour()

    def change_state(self) -> None:
        ''''

        '''
        if self.state == 'wandering':
            for site in self.aggregation.objects.sites:
                collide = pygame.sprite.collide_mask(self, site)
                if bool(collide):
                    # find all the neighbors of a roach based on its radius view
                    neighbors = self.aggregation.find_neighbors(self, config["roaches"]["radius_view"])
                    p_join = len(neighbors) / config['base']['n_agents']
                    rand_p = np.random.uniform(0, 1)
                    if p_join > rand_p:
                        self.state = 'joining'

        elif self.state == 'joining':
            # TODO: the timer is not working here, it is only dependant on the random noise generated
            start_ticks = pygame.time.get_ticks()  # starter tick
            seconds = (pygame.time.get_ticks() - start_ticks) / 1000  # calculate how many seconds
            random_noise = np.random.normal(0, 1)
            if seconds > config['agent']['internal_clock'] + random_noise:  # if more than 2 seconds close the game
                self.state = 'still'
                pass

        elif self.state == 'still':
            neighbors = self.aggregation.find_neighbors(self, config["roaches"]["radius_view"])
            p_leave = len(neighbors) / config['base']['n_agents']
            # rand_p = np.random.uniform(0, 1)
            if p_leave > config['roaches']['leaving_threshold']:
                self.state = 'leave'

        elif self.state == 'leave':
            # TODO: change state to wandering, now they are leaving but not changing the state
            start_ticks = pygame.time.get_ticks()  # starter tick
            seconds = (pygame.time.get_ticks() - start_ticks) / 1000  # calculate how many seconds
            # random_noise = np.random.normal(0, 1)
            # print(seconds)
            if seconds > 5:
                self.state = 'wandering'
                # print('yes')



    def site_behaviour(self) -> None:
        '''
            Returns:
        '''
        if self.state == 'wandering':
            # do some random movement aka wandering
            wandering_force = self.wander(wander_angle=config['wandering']['wander_angle'],
                                          wander_dist=config['wandering']['wander_dist'],
                                          wander_radius=config['wandering']['wander_radius'])

            # adjust the direction of the boid
            self.steering += truncate(
                wandering_force, config["roaches"]["max_force"]
            )

        elif self.state == 'joining':
            pass

        elif self.state == 'still':
            for site in self.aggregation.objects.sites:
                collide = pygame.sprite.collide_mask(self, site)
                if not bool(collide):
                    self.state = 'wandering'
                    pass
                else:
                    self.v = [0, 0]

        elif self.state == 'leave':
            # TODO: make the v direction random
            self.v = [20, 20]
            # self.v = np.random.randint(20, 2)[:]
            # self.v =
