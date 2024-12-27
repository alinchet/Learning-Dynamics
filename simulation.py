import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import bernoulli
import random
import matplotlib.pyplot as plt
import numpy as np


# Parameters
b = 5  # Benefit of cooperation
c = 1  # Cost of cooperation

# Payoff matrices
A_in = np.array([[b - c, -c], [b, 0]])
A_out = np.array([[b - c, -c], [b, 0]])

# Strategies
strategies = {
    "Altruist": (1, 1),    # Cooperates with in- and out-group
    "Parochialist": (1, 0),  # Cooperates with in-group only
    "Traitor": (0, 1),     # Cooperates with out-group only
    "Egoist": (0, 0),      # Does not cooperate
}

def compute_payoff(strategy1, strategy2, in_group=True):
    """Compute the payoff for a pair of strategies."""
    matrix = A_in if in_group else A_out
    return matrix[strategy1, strategy2]

# Example computation
strategy1, strategy2 = 0, 1  # Altruist vs. Egoist
payoff = compute_payoff(strategy1, strategy2, in_group=True)
print(f"Payoff (In-Group): {payoff}")




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


# Initialize parameters
num_groups = 10
group_size = 10
alpha = 0.8
conflict_rate = 0.025

# Initialize population and introduce a mutant
population = Population(num_groups, group_size)
population.introduce_mutant(0, strategy="Parochialist")

# Simulate generations until fixation
max_generations = 1000
for generation in range(max_generations):
    population.simulate_generation(alpha, conflict_rate)
    if population.fixation_probability("Parochialist"):
        print(f"Parochialist strategy fixated in generation {generation + 1}")
        break
else:
    print("Fixation not achieved within the generation limit.")





def simulate_fixation(num_groups, group_size, alpha, conflict_rate, strategy, max_generations=1000):
    """
    Simulate the fixation probability of a strategy under given parameters.

    :param num_groups: Number of groups
    :param group_size: Size of each group
    :param alpha: Probability of in-group interaction
    :param conflict_rate: Frequency of group conflicts
    :param strategy: Strategy to simulate (e.g., "Parochialist", "Altruist")
    :param max_generations: Maximum number of generations to simulate
    :return: Fixation probability (0 or 1)
    """
    repetitions = 100  # Number of independent simulations
    fixation_count = 0

    for _ in range(repetitions):
        population = Population(num_groups, group_size)
        population.introduce_mutant(0, strategy)

        for generation in range(max_generations):
            population.simulate_generation(alpha, conflict_rate)
            if population.fixation_probability(strategy):
                fixation_count += 1
                break

    return fixation_count / repetitions


def plot_fixation_vs_alpha(num_groups, group_size, conflict_rate, strategy):
    """
    Plot fixation probability as a function of alpha (in-group interaction frequency).

    :param num_groups: Number of groups
    :param group_size: Size of each group
    :param conflict_rate: Frequency of group conflicts
    :param strategy: Strategy to simulate
    """
    alphas = np.linspace(0, 1, 20)
    fixation_probs = [
        simulate_fixation(num_groups, group_size, alpha, conflict_rate, strategy)
        for alpha in alphas
    ]

    plt.figure(figsize=(8, 6))
    plt.plot(alphas, fixation_probs, marker="o", label=f"Strategy: {strategy}")
    plt.title(f"Fixation Probability vs. In-Group Interaction Frequency (α)")
    plt.xlabel("In-Group Interaction Frequency (α)")
    plt.ylabel("Fixation Probability")
    plt.legend()
    plt.grid()
    plt.show()


def plot_fixation_vs_b_c_ratio(num_groups, group_size, alpha, conflict_rate, strategy):
    """
    Plot fixation probability as a function of the benefit-cost ratio (b/c).

    :param num_groups: Number of groups
    :param group_size: Size of each group
    :param alpha: Probability of in-group interaction
    :param conflict_rate: Frequency of group conflicts
    :param strategy: Strategy to simulate
    """
    b_c_ratios = np.linspace(1.5, 5, 20)
    global b, c

    fixation_probs = []
    for ratio in b_c_ratios:
        b = ratio * c  # Update the global b to match the new ratio
        fixation_probs.append(simulate_fixation(num_groups, group_size, alpha, conflict_rate, strategy))

    plt.figure(figsize=(8, 6))
    plt.plot(b_c_ratios, fixation_probs, marker="o", label=f"Strategy: {strategy}")
    plt.title(f"Fixation Probability vs. Benefit-Cost Ratio (b/c)")
    plt.xlabel("Benefit-Cost Ratio (b/c)")
    plt.ylabel("Fixation Probability")
    plt.legend()
    plt.grid()
    plt.show()


# Plot fixation probability vs. alpha for "Parochialist"
plot_fixation_vs_alpha(num_groups=10, group_size=10, conflict_rate=0.025, strategy="Parochialist")

# Plot fixation probability vs. benefit-cost ratio for "Parochialist"
plot_fixation_vs_b_c_ratio(num_groups=10, group_size=10, alpha=0.8, conflict_rate=0.025, strategy="Parochialist")
