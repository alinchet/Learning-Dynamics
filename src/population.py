from constants import *
from config import *
import random


class Population:
    """ Class to represent a population of groups """

    def __init__(self, num_groups, num_individuals, mutant_strategy=Strategy.ALTRUIST):
        self.num_groups = num_groups
        self.num_individuals = num_individuals
        self.groups = self._initialize_population(mutant_strategy)

    def _initialize_population(self, mutant_strategy):
        """
        Initialize m groups each with n individuals, where all individuals
        are egoists except for a mutant altruist or parochialist.
        """
        groups = [[Strategy.EGOIST] * self.num_individuals for _ in range(self.num_groups)]
        groups[0][0] = mutant_strategy  # Introduce a mutant in group 1
        return groups

    def calculate_payoff(self, individual_1, individual_2):
        """
        Calculate payoffs for individuals based on interactions.
        """
        payoffs = []
        ... #TODO: Implement payoff calculation
        return payoffs

    def calculate_fitness(self, payoffs):
        """
        Calculate fitness for each group based on payoffs.
        f_i = 1 - w + w * g_i, where g_i is the group's payoff.
        """
        fitness = []
        for payoff in payoffs:
            fitness.append(1 - w + w * payoff)
        return fitness

    def reproduce(self, fitness):
        ... #TODO: Implement reproduction

    def resolve_conflicts(self):
        ... #TODO: Implement conflict resolution

    def split_groups(self):
        """ Split groups if they exceed the maximum size """
        for i in range(len(self.groups)):
            if len(self.groups[i]) > n:
                if random.random() < q:
                    # Split the group
                    self._split_groups(i)
                else:
                    # Eliminate a random individual
                    self._eliminate_individual(i)

    def _split_groups(self, group_index):
        """
        Split the group at group_index into two daughter groups.
        """
        parent_group = self.groups[group_index]
        daughter_group_1, daughter_group_2 = [], []

        while parent_group:
            individual = parent_group.pop(random.randint(0, len(parent_group) - 1))
            if random.random() < 0.5:
                daughter_group_1.append(individual)
            else:
                daughter_group_2.append(individual)

        # Replace the parent group and randomly replace another group
        self.groups[group_index] = daughter_group_1
        random_group_idx = random.randint(0, len(self.groups) - 1)
        self.groups[random_group_idx] = daughter_group_2

    def _eliminate_individual(self, group_index):
        """
        Eliminate a random individual from the group at group_index.
        """
        random_individual_idx = random.randint(0, len(self.groups[group_index]) - 1)
        self.groups[group_index].pop(random_individual_idx)
    
    def run_simulation(self):
        ... #TODO: Implement simulation logic

