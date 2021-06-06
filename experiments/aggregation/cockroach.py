from experiments.aggregation.config import config
from simulation.agent import Agent
from simulation.utils import *


class Cockroach(Agent):
    """
    The cockroach main class
    """
    def __init__(
            self, pos, v, aggregation, index: int, image: str = "experiments/aggregation/images/ant_1.png"
    ) -> None:
        """
        Args:
        ----
            pos:
            v:
            aggregation:
            index (int):
            image (str): Defaults to "experiments/aggregation/images/ant_1.png"
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
        self.start_millis = 0
        self.started = False

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
        self.site_behaviour()
        self.change_state()
        print(self.state)


    def change_state(self) -> None:
        ''''
        Each frame, this function is called. It ensures the transition between the different kinds of states.
        '''
        if self.state == 'wandering':
            for site in self.aggregation.objects.sites:
                collide = pygame.sprite.collide_mask(self, site)
                if bool(collide):  # if wandering and the roach is in some site
                    # find all the neighbors of a roach based on its radius view
                    neighbors = self.aggregation.find_neighbors(self, config["roaches"]["radius_view"])
                    p_join = len(neighbors) / config['base']['n_agents']
                    # TODO: utilize the radius view inside of the probability
                    rand_p = np.random.uniform(0, .2) # the lower the radius view is the lower this should be
                    if p_join > rand_p:  # the more neighbors the higher the prob to join
                        self.state = 'joining'
                        break # this is essential when having two sites, once the roach is inside any of the sites,
                        # the joining process should begin immediately

        elif self.state == 'joining':
            if not self.started:
                self.start_millis = pygame.time.get_ticks()  # starter tick
                self.started = True
            random_noise = np.random.normal(0, 1) # this is added to let the roached stop in multiple positions insde the site
            seconds = (pygame.time.get_ticks() - self.start_millis) / 1000  # calculate how many seconds
            if seconds > config['agent']['internal_clock'] + random_noise:
                self.state = 'still'
                self.started = False
            else:  # if after the timer the roach is not anymore inside the site, the roach goes back to wandering state
                self.state = 'wandering'

        elif self.state == 'still':
            neighbors = self.aggregation.find_neighbors(self, config["roaches"]["radius_view"])
            p_leave = len(neighbors) / config['base']['n_agents']
            # TODO: utilize the radius view inside of the probability
            rand = np.random.uniform(0, .03)
            # print(p_leave, rand)
            # if p_leave < config['roaches']['leaving_threshold']:
            if p_leave < rand:
                self.state = 'leave'
            else:
                pass
        elif self.state == 'leave':
            if not self.started:
                self.start_millis = pygame.time.get_ticks()  # starter tick
                self.started = True
                # give some random direction to go towards
                self.steering += truncate(
                    np.random.randint(-60, 60, 2), config["roaches"]["max_force"]
                )
            seconds = (pygame.time.get_ticks() - self.start_millis) / 1000  # calculate how many seconds
            if seconds > 5:
                self.state = 'wandering'
                self.started = False

    def site_behaviour(self) -> None:
        if self.state == 'wandering':
            # do some random movement aka wandering
            wandering_force = self.wander(wander_angle=config['wandering']['wander_angle'],
                                          wander_dist=config['wandering']['wander_dist'],
                                          wander_radius=config['wandering']['wander_radius'])

            # adjust the direction of the roach based on the random wandering force
            self.steering += truncate(
                wandering_force, config["roaches"]["max_force"]
            )

        elif self.state == 'joining':
            # while joining the roach doesn't need to do anything besides the timer and the probability
            # which is made in change_state
            pass

        elif self.state == 'still':
            for site in self.aggregation.objects.sites:
                collide = pygame.sprite.collide_mask(self, site)
                if not bool(collide):
                    self.state = 'wandering'
                    # give some random direction to go towards
                    self.steering += truncate(
                        np.random.randint(-60, 60, 2), config["roaches"]["max_force"]
                    )
                else:
                    self.v = [0, 0]
                    break
        elif self.state == 'leave':
            # while leaving the roach doesn't need to do anything besides the timer and the probability
            # which is made in change_state
            pass
