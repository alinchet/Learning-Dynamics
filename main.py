import matplotlib.pyplot as plt
from enum import Enum
import numpy as np
import random

# Parameters
m = 10  # Number of groups
n = 10  # Individuals per group
w = 0.1  # Selection intensity
alpha = 0.8  # Probability of ingroup interaction
kappa = 0.025  # Frequency of group conflict
lambda_migration = 0.0  # Migration rate
q_split = 0.01  # Probability of group splitting
z_steepness = 0.5  # Steepness of contest function
b = 2.0  # Benefit of cooperation
c = 1.0  # Cost of cooperation

generations = 1000  # Total number of generations

# Payoff matrices
A_in = np.array([
        [b-c, b-c, -c, -c],
        [b-c, b-c, -c, -c],
        [b, b, 0, 0],
        [b, b, 0, 0],
    ])
A_out = np.array([
        [b-c, -c, b-c, -c],
        [b, 0, b, 0],
        [b-c, -c, b-c, -c],
        [b, 0, b, 0],
    ])

# Strategies
class Strategy(Enum):
    ALTRUIST = 0      # Cooperates with in- and out-group
    PAROCHIALIST = 1  # Cooperates with in-group only
    TRAITOR = 2       # Cooperates with out-group only
    EGOIST = 3        # Does not cooperate

class Individual:
    """Represents an individual in a population with a group ID and strategy."""
    def __init__(self, group_id, initial_strategy=Strategy.EGOIST):
        """
        Initialize an Individual with a group ID and a valid strategy.

        :param group_id: ID of the group the individual belongs to.
        :param initial_strategy: Initial strategy of the individual (default is EGOIST).
        """
        self.group_id = group_id
        self.strategy = initial_strategy
        self.payoff = 0
        self.fitness = 0

    @property #flex
    def strategy(self):
        """Getter for strategy."""
        return self._strategy

    @strategy.setter
    def strategy(self, value):
        """Setter for strategy with validation."""
        if not isinstance(value, Strategy):
            raise ValueError(f"Invalid strategy '{value}'. Must be an instance of Strategy Enum.")
        self._strategy = value
    
    def compute_payoff(self):
        pass

    def compute_fitness(individual:Individual):
        individual.fitness = 1-w+w*individual.payoff   
        
class Group:
    def __init__(self, group_id, group_size):
        self.group_id = group_id
        self.individuals = [Individual(group_id) for _ in range(group_size)]
        
    def reproduction(self):
        # Inside groups, strategies reproduce in proportion to the
        # payoff obtained in the game, following a Moran process.
        pass
    
    def introduce_mutant(self, strategy=Strategy.ALTRUIST):
        self.individuals[0].strategy = strategy
    
    def compute_payoff(self, alpha):
        pass

class Population: #struc that contains the groups, attributes are num groups m, 
    def __init__(self, num_groups, group_size=n, initial_strategy=Strategy.EGOIST):
        """
        Initialize a population of groups.
        
        :param num_groups: Number of groups in the population
        :param group_size: Number of individuals in each group
        :param initial_strategy: Strategy for all individuals at the start
        """
        self.groups = [Group(i, group_size) for i in range(num_groups)] #group size c n 
        self.groups[0].introduce_mutant()
        
        self.num_groups = num_groups
        self.group_size = group_size

    def interaction(self): #temp groups, match random pop. TODO odd number of indiv, at least one interaction? (implying more than 1), maybe attribut to track, or leave the first and pop the rest
        ...
        raise NotImplementedError
    
    

    
    def group_conflict(self, k):
        pass


    def compute_group_payoff(self, group_index, alpha):
        pass
    
########################################
### Simulation

#1. Initialize the Population
def init_groups(m:int ,n:int):
    """
    Start with m groups, each containing n individuals.
    ALL individuals are egoist but only one is altruist or parochialist 
    """
    pass

#2. Pairwise Interactions and Payoff Calculation
def compute_individual_interaction(individual_1:Individual,individual_2:Individual):
    current_payoffs = [0]*2
    
    strat_1_index = Strategy[individual_1.strategy]
    strat_2_index = Strategy[individual_2.strategy]
    
    if individual_1.group_id == individual_2.group_id:
        current_payoffs[0]+=A_in[strat_1_index,strat_2_index]
        current_payoffs[1]+=A_in[strat_1_index,strat_2_index]
    else:
        current_payoffs[0]+=A_out[strat_1_index,strat_2_index]
        current_payoffs[1]+=A_out[strat_1_index,strat_2_index]
    
    individual_1.payoff+=current_payoffs[0]
    individual_2.payoff+=current_payoffs[1]
µ
# create population


# simulation loop:

#compute_interaction()

#compute_payoff()

#compute_fitness()
        
#reproduction()        
    #migration() dapres repro, randomly pick dans les groupes, check id different, migrate

#group_conflict() #pick kappa*m groups, compute payoff, calculate winner based on total payoff , ODD numbers again TODO

#group_splitting() #for each group reaching n if q proba says NO split, delete random individual else split

#repeat until convergence/winning strat, create full simulation pipeline, with plots at the end.
    #return nbr_needed_generation


#plot()