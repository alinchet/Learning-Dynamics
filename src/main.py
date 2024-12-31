import matplotlib.pyplot as plt
import numpy as np
import random
import copy
# Import constants and configuration values
from constants import Strategy, A_IN_MATRIX, A_OUT_MATRIX
from config import n, w, alpha, b, c,lambda_mig, q, kappa, z


class Individual:
    """
    Represents an individual in the population with a group ID, strategy, payoff, and fitness.
    """
    def __init__(self, group_id, strategy=Strategy.EGOIST):
        """
        Initialize an Individual.

        :param group_id: The group the individual belongs to.
        :param strategy: Initial strategy of the individual (default is EGOIST).
        """
        self._group_id = group_id
        self._strategy = strategy
        self._payoff = 0.0
        self._fitness = 0.0

        self.reproduction_probability = 0

    # ------------------ PROPERTIES ------------------
    @property
    def group_id(self):
        """Returns the group ID the individual belongs to."""
        return self._group_id

    @group_id.setter
    def group_id(self, value):
        """Validates and sets the group ID."""
        if not isinstance(value, int):
            raise ValueError(f"Invalid group ID '{value}'. Must be an integer.")
        self._group_id = value

    @property
    def fitness(self):
        """Returns the fitness of the individual."""
        return self._fitness

    @fitness.setter
    def fitness(self, value):
        """Validates and sets the fitness."""
        if not isinstance(value, (float, int)):
            raise ValueError(f"Invalid fitness '{value}'. Must be a float or int.")
        self._fitness = float(value)

    @property
    def payoff(self):
        """Returns the payoff of the individual."""
        return self._payoff

    @payoff.setter
    def payoff(self, value):
        """Validates and sets the payoff."""
        if not isinstance(value, (float, int)):
            raise ValueError(f"Invalid payoff '{value}'. Must be a float or int.")
        self._payoff = float(value)

    @property
    def strategy(self):
        """Returns the strategy of the individual."""
        return self._strategy

    @strategy.setter
    def strategy(self, value):
        """Validates and sets the strategy."""
        if not isinstance(value, Strategy):
            raise ValueError(f"Invalid strategy '{value}'. Must be an instance of Strategy Enum.")
        self._strategy = value

    # ------------------ METHODS ------------------
    def compute_fitness(self):
        """
        Computes the fitness based on payoff and updates the fitness attribute.
        """
        self.fitness = 1 - w + w * self.payoff
        return self.fitness

    def __str__(self):
        """Print representation for debugging."""
        return (f"Individual(Group {self.group_id}, Strategy {self.strategy.name}, "
                f"Payoff {self.payoff:.2f}, Fitness {self.fitness:.2f})")


class Group:
    """
    Represents a group of individuals in the population.
    """
    def __init__(self, group_id, group_size):
        self.group_id = group_id
        self.individuals = [Individual(group_id) for _ in range(group_size)]
        self.group_payoff = 0.0

    def reproduction(self):
        # TODO: Implement reproduction process
        pass
    
    def introduce_mutant(self, strategy=Strategy.ALTRUIST):
        """Introduce a mutant in the first position of the group."""
        self.individuals[0].strategy = strategy
    
    def compute_group_payoff(self):
        """Computes and returns the total payoff for the group."""
        self.group_payoff = sum(ind.payoff for ind in self.individuals)
        return self.group_payoff

    def __str__(self):
        """Print representation for debugging."""
        individuals_info = "\n".join(str(ind) for ind in self.individuals)
        return f"Group {self.group_id} (Payoff: {self.group_payoff}):\n{individuals_info}"


class Population:
    """
    Represents the entire population of groups.
    """
    def __init__(self, num_groups, group_size=n, initial_strategy=Strategy.EGOIST):
        """
        Initialize a population of groups.
        
        :param num_groups: Number of groups in the population
        :param group_size: Number of individuals in each group
        :param initial_strategy: Strategy for all individuals at the start
        """
        self.groups = [Group(i, group_size) for i in range(num_groups)]
        self.groups[0].introduce_mutant()  # Introduce a mutant in the first group
        
        self.num_groups = num_groups
        self.group_size = group_size
    

    ### Setup
    def find_corresponding_group(self,group_id):
        ...
    ### PHASE 1: Interaction (individual payoff and fitness)
    def in_group_interaction(self, group, individual):
        """Handles interactions within the group."""
        if len(group.individuals) < 2:
            return
        partner = random.choice(group.individuals)
        while partner is individual:
            partner = random.choice(group.individuals)

        individual.payoff += A_IN_MATRIX[individual.strategy.value][partner.strategy.value]
        partner.payoff += A_IN_MATRIX[partner.strategy.value][individual.strategy.value]

    def out_group_interaction(self, group, individual):
        """Handles interactions across groups."""
        other_groups = [g for g in self.groups if g is not group]
        if not other_groups:
            return

        random_group = random.choice(other_groups)
        partner = random.choice(random_group.individuals)

        individual.payoff += A_OUT_MATRIX[individual.strategy.value][partner.strategy.value]
        partner.payoff += A_OUT_MATRIX[partner.strategy.value][individual.strategy.value]

    def interaction(self):
        """Simulates interactions within and across groups."""
        for group in self.groups:
            for individual in group.individuals:
                if random.random() < alpha: #TODO check that works as alpha and 1-alpha
                    self.in_group_interaction(group, individual)
                else:
                    self.out_group_interaction(group, individual)

    def test_interaction(self):
        """Test function to check interactions and payoffs."""
        self.interaction()
        for group in self.groups:
            print(group)

    ### PHASE 2: Reproduction (TODO)
    def compute_reproduction_probabilities(self):
        population_fitness = 0
        for group in self.groups:
            for indvidual in group.individuals:
                population_fitness+=indvidual.fitness
        
        for group in self.groups:
            for indvidual in group.individuals:
                indvidual.reproduction_probability = indvidual.fitness/population_fitness

    def pick_value(self,values_list, probabilities_list):
        """
        Picks a value from a list based on the given probabilities.

        :param values: List of values to choose from.
        :param probabilities: List of probabilities corresponding to each value.
        :return: Selected value.
        """
        if len(values_list) != len(probabilities_list):
            raise ValueError("Values and probabilities must have the same length.")

        if not (0.99 <= sum(probabilities_list) <= 1.01):
            raise ValueError("Probabilities must sum up to 1.")

        return random.choices(values_list, probabilities_list)[0]

    def pick_indvidual_to_reproduce(self):
        #TODO REFACTOR list of Individual as population attribute 
        indvidual_list = []
        probability_list = []
        
        for group in self.groups:
            for indvidual in group.individuals:
                indvidual_list.append(indvidual)
                probability_list.append(indvidual.reproduction_probability)
        
        return self.pick_value(indvidual_list,probability_list)

    def reproduce_selected_indvidual(self,selected_indvidual):
        individual_copy = copy.deepcopy(selected_indvidual)
        

        if random.random() < lambda_mig:
            self.migrate_individual(individual_copy)
        else:
            #Stay in the same group
            ...


        
    
    def migrate_individual(self,individual):
        #Find the corresponging old group and pop the individual from the old group's list
        self.groups[individual.group_id].individuals.remove(individual) #TODO maintenir structure de donnée cohérente
        
        new_group = random.choice([g for g in self.groups if g.group_id != individual.group_id])
        while new_group == individual.group_id:
            new_group = random.choice([g for g in self.groups if g.group_id != individual.group_id])
        individual.group_id = new_group.group_id
        
        new_group.individuals.append(individual)
        

        
    def check_N_for_split(self,group_id):
        group = self.groups[group_id]
        if len(group.individuals) > n:
            if random.random() < q:
                self.split_group(group)
            else:
                self.remove_random_individual(group)
    
    ### PHASE 3: Group Conflict (TODO)
    def group_conflict(self):
        pass

    ### PHASE 4: Group Splitting (TODO)
    def group_splitting(self):
        pass

    def __str__(self):
        """Print representation for debugging."""
        return "\n".join(str(group) for group in self.groups)


# --------------------------- SIMULATION ---------------------------

# Initialize Population
population = Population(10, 10, Strategy.EGOIST)

# Test Interaction
population.test_interaction()




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