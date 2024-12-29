import random

class Population:
    def __init__(self, num_groups, group_size, initial_strategy="Egoist"):
        """
        Initialize a population of groups.
        
        :param num_groups: Number of groups in the population
        :param group_size: Number of individuals in each group
        :param initial_strategy: Strategy for all individuals at the start
        """
        self.groups = [
            [initial_strategy] * group_size for _ in range(num_groups)
        ]
        self.num_groups = num_groups
        self.group_size = group_size

    def introduce_mutant(self, group_index, strategy="Altruist"):
        """
        Introduce a mutant with a specific strategy into a group.
        
        :param group_index: Index of the group to mutate
        :param strategy: Strategy of the mutant
        """
        self.groups[group_index][0] = strategy

    def compute_group_payoff(self, group_index, alpha):
        """
        Compute the total payoff of a group considering intergroup (1-alpha)
        and intragroup (alpha) interactions.
        
        :param group_index: Index of the group
        :param alpha: Probability of in-group interaction
        :return: Total group payoff
        """
        group = self.groups[group_index]
        in_group_payoff = 0
        out_group_payoff = 0
        
        for i, strategy in enumerate(group):
            for j, other_strategy in enumerate(group):
                in_group_payoff += compute_payoff(
                    strategy1=strategies[strategy][0],
                    strategy2=strategies[other_strategy][0],
                    in_group=True
                )
            for other_group_index in range(self.num_groups):
                if other_group_index != group_index:
                    other_group = self.groups[other_group_index]
                    out_group_payoff += compute_payoff(
                        strategy1=strategies[strategy][1],
                        strategy2=strategies[random.choice(other_group)][1],
                        in_group=False
                    )
        return alpha * in_group_payoff + (1 - alpha) * out_group_payoff

    def group_conflict(self, alpha):
        """
        Simulate group conflicts and update the population.
        
        :param alpha: Probability of in-group interaction
        """
        pairings = random.sample(range(self.num_groups), 2)
        payoffs = [
            self.compute_group_payoff(group, alpha) for group in pairings
        ]
        
        # Higher payoff group wins, lower is replaced
        if payoffs[0] > payoffs[1]:
            self.groups[pairings[1]] = self.groups[pairings[0]][:]
        elif payoffs[1] > payoffs[0]:
            self.groups[pairings[0]] = self.groups[pairings[1]][:]

    def simulate_generation(self, alpha, conflict_rate=0.025):
        """
        Simulate one generation of the population dynamics.
        
        :param alpha: Probability of in-group interaction
        :param conflict_rate: Frequency of group conflicts
        """
        for _ in range(int(self.num_groups * conflict_rate)):
            self.group_conflict(alpha)

    def fixation_probability(self, target_strategy):
        """
        Check if the target strategy has fixated in the population.
        
        :param target_strategy: Strategy to check for fixation
        :return: True if fixated, False otherwise
        """
        for group in self.groups:
            if any(individual != target_strategy for individual in group):
                return False
        return True