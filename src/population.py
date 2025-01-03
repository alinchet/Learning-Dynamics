import logging
import random
import copy

from src.individual import Individual
from src.constants import Strategy, A_IN_MATRIX, A_OUT_MATRIX
from src.config import n, q, z, lambda_mig, alpha, kappa

# --- Logging Setup ---
logging.basicConfig(
    filename='run_logs/population.log',  # Log file name
    level=logging.INFO,          # Log level (you can adjust to DEBUG, ERROR, etc.)
    format='%(asctime)s - %(levelname)s - %(message)s'  # Log format with timestamp
)

class Population:
    """
    Class to represent a population of groups.

    This class manages:
      - Initialization of groups (mostly egoists, plus one mutant).
      - Game-playing among individuals (pairwise interactions).
      - Fitness calculation based on accumulated payoff.
      - Fitness-proportional reproduction (with possible migration).
      - Conflicts between groups.
      - Group splitting or elimination of individuals when groups exceed max size.
    """

    # --- INITIALIZATION ---

    def __init__(self,
                 num_groups: int = 10,
                 num_individuals: int = 10,
                 mutant_strategy: Strategy = Strategy.ALTRUIST):
        """
        Initialize a population with groups of individuals.

        Args:
            num_groups (int): Number of groups.
            num_individuals (int): Number of individuals per group.
            mutant_strategy (Strategy): Strategy for the mutant individual.
        """
        logging.info(
            f"Initializing population with {num_groups} groups, "
            f"{num_individuals} individuals each."
        )
        self.num_groups = num_groups
        self.num_individuals = num_individuals
        self.groups = self._initialize_population(mutant_strategy)

    def _initialize_population(self, mutant_strategy: Strategy) -> list[list[Individual]]:
        """
        Create groups of individuals (egoists by default), introducing one mutant
        with a given strategy in the first group.

        Args:
            mutant_strategy (Strategy): Strategy for the mutant individual.

        Returns:
            list[list[Individual]]: A list of groups, each a list of Individuals.
        """
        logging.info(
            f"Creating groups of egoists with a single mutant of strategy "
            f"{mutant_strategy}."
        )

        # Create groups with egoist individuals by default
        groups = [[Individual() for _ in range(self.num_individuals)]
                  for _ in range(self.num_groups)]

        # Introduce a mutant in the first group
        groups[0][0].strategy = mutant_strategy

        return groups

    # --- POPULATION ANALYSIS ---

    def is_homogeneous(self) -> bool:
        """
        Check if the population is homogeneous, i.e., 
        consists entirely of individuals with the same strategy.

        Returns:
            bool: True if the population is homogeneous, False otherwise.
        """
        first_strategy = self.groups[0][0].strategy
        homogeneous = all(
            individual.strategy == first_strategy
            for group in self.groups
            for individual in group
        )
        logging.info(f"Population homogeneous: {homogeneous}")
        return homogeneous
    
    def get_population_distribution(self) -> dict[Strategy, int]:
        """
        Get the distribution of strategies in the population.

        Returns:
            dict[Strategy, int]: A dictionary with the count of each strategy.
        """
        distribution = {
            Strategy.EGOIST: 0,
            Strategy.ALTRUIST: 0,
            Strategy.PUNISHER: 0
        }
        for group in self.groups:
            for individual in group:
                distribution[individual.strategy] += 1
        return distribution

    def get_homogeneous_strategy(self) -> Strategy:
        """
        Get the strategy of the homogeneous population.
        """
        return self.groups[0][0].strategy

    def get_group(self, individual: Individual) -> int | None:
        """
        Get the group index to which an individual belongs.

        Args:
            individual (Individual): The individual to locate.

        Returns:
            int | None: Index of the group or None if the individual is not found.
        """
        for index, group in enumerate(self.groups):
            if individual in group:
                return index
        return None

    def are_in_same_group(self, individual_1: Individual, individual_2: Individual) -> bool:
        """
        Check if two individuals belong to the same group.

        Args:
            individual_1 (Individual): First individual.
            individual_2 (Individual): Second individual.

        Returns:
            bool: True if both individuals are in the same group, False otherwise.
        """
        same_group = self.get_group(individual_1) == self.get_group(individual_2)
        logging.debug(f"Individuals in same group: {same_group}")
        return same_group

    def get_flattened_population(self) -> list[Individual]:
        """
        Get a flattened list of all individuals in the population.

        Returns:
            list[Individual]: Flattened list of all individuals.
        """
        return [individual for group in self.groups for individual in group]

    # --- PARTNER SELECTION ---

    def random_out_group_member(self, exclude_group: list[Individual]) -> Individual:
        """
        Select a random individual from an out-group.

        Args:
            exclude_group (list[Individual]): The group to exclude.

        Returns:
            Individual: A random individual from any group except exclude_group.
        """
        out_group = [ind for group in self.groups if group != exclude_group for ind in group]
        return random.choice(out_group)

    def random_in_group_member(self, individual: Individual, group_index: int) -> Individual:
        """
        Select a random individual from the same group as `individual`, excluding that individual.

        Args:
            individual (Individual): The individual we are finding a partner for.
            group_index (int): The index of the group to select from.

        Returns:
            Individual: A random individual from the specified in-group.
        """
        in_group = [ind for ind in self.groups[group_index] if ind != individual]
        if not in_group:
            logging.warning("No in-group members found.") #TODO check what should we do? jsp ce qui cause un groupe vide
            return None  # or raise, or handle differently
        return random.choice(in_group)

    def get_random_partner(self, individual: Individual) -> Individual:
        """
        Get a random partner for an individual, either from the same group or a different one
        based on the probability alpha.

        Args:
            individual (Individual): The individual for which to find a partner.

        Returns:
            Individual: A random partner for the individual.
        """
        group_idx = self.get_group(individual)
        if random.random() < alpha:
            # Randomly select an individual from the same group
            return self.random_in_group_member(individual, group_idx) #TODO handle group of size 1 ?
        else:
            # Randomly select an individual from a different group
            return self.random_out_group_member(self.groups[group_idx])

    # --- GAME PLAY & PAYOFFS ---

    def play_game(self):
        """
        Simulate interactions (games) between individuals and their randomly selected partners.
        Each pair calculates payoffs based on whether they are in the same group or different groups.
        """
        logging.info("Playing game between individuals.")
        for group in self.groups:
            for individual in group:
                partner = self.get_random_partner(individual)
                # Choose the payoff matrix based on in-group vs out-group
                matrix = A_IN_MATRIX if self.are_in_same_group(individual, partner) else A_OUT_MATRIX

                # Calculate payoffs for both individuals
                individual.calculate_payoff(partner, matrix)
                partner.calculate_payoff(individual, matrix)

    def calculate_fitness(self):
        """
        Calculate and update fitness for all individuals in the population,
        typically after payoffs are calculated.
        """
        logging.info("Calculating fitness for all individuals.")
        for group in self.groups:
            for individual in group:
                individual.calculate_fitness()

    # --- REPRODUCTION ---

    def select_individual_for_duplication(self) -> tuple[Individual, int]:
        """
        Select an individual for duplication based on fitness-proportional probabilities.
        Returns the selected individual (as a copy) and the index of the group 
        it was originally selected from.

        Returns:
            (Individual, int): A copy of the selected individual, and the group index.
        """
        total_fitness = sum(ind.fitness for group in self.groups for ind in group)

        # If all individuals have zero fitness, select randomly
        if total_fitness == 0:
            logging.warning("All individuals have zero fitness. Selecting randomly.")
            group_index = random.randint(0, len(self.groups) - 1)
            individual = random.choice(self.groups[group_index])
            return copy.deepcopy(individual), group_index

        # Build lists for random.choices
        individuals = [ind for group in self.groups for ind in group]
        group_indices = []
        probabilities = []
        for i, group in enumerate(self.groups):
            for ind in group:
                group_indices.append(i)
                probabilities.append(ind.fitness / total_fitness)

        # Select an individual based on fitness-weighted probabilities
        selected_individual = random.choices(individuals, weights=probabilities, k=1)[0]
        selected_group_index = group_indices[individuals.index(selected_individual)]
        logging.info(
            f"Selected individual {selected_individual} from group {selected_group_index} "
            "for duplication."
        )
        return copy.deepcopy(selected_individual), selected_group_index

    def reproduce(self):
        """
        Simulate reproduction based on fitness-proportional selection.
        With probability lambda_mig, the new individual migrates to a different group.
        Otherwise, it stays in its parent's group.
        """
        new_individual, parent_group_index = self.select_individual_for_duplication()

        if random.random() < lambda_mig:
            # Migration: Add to a random different group
            target_group_index = random.choice([
                i for i in range(len(self.groups)) 
                if i != parent_group_index
            ])
            self.groups[target_group_index].append(new_individual)
            logging.info(f"New individual migrated to group {target_group_index}.")
        else:
            # Stay in the same group
            self.groups[parent_group_index].append(new_individual)
            logging.info(f"New individual added to group {parent_group_index}.")

    def random_in_group_member2(self, individual: Individual, group_index: int) -> Individual | None:
        in_group = [ind for ind in self.groups[group_index] if ind != individual]
        if not in_group:
            logging.warning("No in-group members found.")
            return None  # or raise, or handle differently
        return random.choice(in_group)


    # --- GROUP CONFLICT ---

    #__________________________________________OLD VERSION__________________________________________
    def pair_groups(self) -> list[tuple[list[Individual], list[Individual]]]:
        """
        Randomly pairs groups for conflict. If the number of groups is odd,
        duplicate or remove a random group to make it even.

        Returns:
            list[tuple[list[Individual], list[Individual]]]: A list of paired groups.
        """
        num_groups_involved = round(len(self.groups) * kappa) #TODO check if this is correct, kappa tends to be very small (tjr 0 en gros)
        groups_involved = [group for group in random.sample(self.groups, num_groups_involved)]
        groups_not_involved = [group for group in self.groups if group not in groups_involved]

        if (num_groups_involved % 2) != 0:
            # Duplicate or remove a random group to make the number even

            if num_groups_involved == len(self.groups):
                # If all groups are involved, remove a random group
                random_group = random.choice(groups_involved)
                groups_involved.remove(random_group)
                logging.info("Removed a random group for conflict.")
            else:
                if random.random() < 0.5:
                    # Add a group to groups_involved
                    random_group = random.choice(groups_not_involved)
                    groups_involved.append(random_group)
                    groups_not_involved.remove(random_group)
                    logging.info("Duplicated a random group for conflict.")
                else:
                    # Remove a random group
                    groups_involved.pop(random.randint(0, len(groups_involved) - 1))
                    logging.info("Removed a random group for conflict.")
        
        # Pair the groups
        random.shuffle(groups_involved)
        return [(groups_involved[i], groups_involved[i + 1]) for i in range(0, len(groups_involved), 2)]

    def conflict_groups(self):
        """
        Simulate conflicts between paired groups.
        The group with higher total fitness wins and replaces the loser group.
        In case of a tie, a random winner is chosen.
        """
        logging.info("Simulating conflicts between groups.")
        for group_1, group_2 in self.pair_groups():
            payoff_1 = sum(ind.payoff for ind in group_1)
            payoff_2 = sum(ind.payoff for ind in group_2)
            
            if payoff_1 == payoff_2:
                win_probability_1 = 0.5
            else:
                win_probability_1 = payoff_1**(1 / z) / (payoff_1**(1 / z) + payoff_2**(1 / z))
            
            if random.random() < win_probability_1:
                winner, loser = group_1, group_2
            else:
                winner, loser = group_2, group_1

            # Replace the losing group with a (copied) version of the winning group
            new_group = copy.deepcopy(winner)
            loser_index = self.groups.index(loser)
            self.groups[loser_index] = new_group
            logging.info("Conflict resolved. Winner replaces loser.")

    #__________________________________________NEW VERSION__________________________________________
    def select_conflict_groups(self):
        """
        This function check for all individuals and verify if they gonna conflict or not with kappa proba.
        

        Returns: 
            conflict_individuals : list[Individual] that gonna conflict
            groups_involved : list[Individual] corresponding groups involved in a conflict
            groups_not_involved : list[Individual] rest of the group, they do not participate to the conflict
        """

        conflict_individuals = []
        groups_involved = []
        for group in self.groups:
            for ind in group:
                if random.random() < kappa:
                    conflict_individuals.append(ind)
                    groups_involved.append(group) if group not in groups_involved else groups_involved
        groups_not_involved = [group for group in self.groups if group not in groups_involved]

        return conflict_individuals,groups_involved,groups_not_involved
    
    def pairs_conflict_groups(self):
        conflict_individuals,groups_involved,groups_not_involved = self.select_conflict_groups()

        num_groups_involved = len(groups_involved)
        if (num_groups_involved % 2) != 0:
            # Duplicate or remove a random group to make the number even

            if num_groups_involved == len(self.groups):
                # If all groups are involved, only remove a random group to get even number of groups
                random_group = random.choice(groups_involved)
                groups_involved.remove(random_group)
                logging.info("Removed a random group for conflict.")
            else:
                if random.random() < 0.5:
                    # Add a group to groups_involved
                    random_group = random.choice(groups_not_involved)
                    groups_involved.append(random_group)
                    groups_not_involved.remove(random_group)
                    logging.info("Duplicated a random group for conflict.")
                else:
                    # Remove a random group
                    groups_involved.pop(random.randint(0, len(groups_involved) - 1))
                    logging.info("Removed a random group for conflict.")
        
        # Pair the groups
        random.shuffle(groups_involved)
        return conflict_individuals,[(groups_involved[i], groups_involved[i + 1]) for i in range(0, len(groups_involved), 2)]

    def conflict_groups_with_conflict_individuals(self):
        """
        Simulate conflicts between paired groups.
        The group with higher total fitness wins and replaces the loser group.
        In case of a tie, a random winner is chosen.
        """
        logging.info("Simulating conflicts between groups.")

        conflict_individuals, group_pairs = self.pairs_conflict_groups()
        for group_1, group_2 in group_pairs:
            payoff_1 = sum(ind.payoff if ind in conflict_individuals else 0 for ind in group_1 )
            payoff_2 = sum(ind.payoff if ind in conflict_individuals else 0 for ind in group_2 )
            
            if payoff_1 == payoff_2:
                win_probability_1 = 0.5
            else:
                win_probability_1 = payoff_1**(1 / z) / (payoff_1**(1 / z) + payoff_2**(1 / z))
            
            if random.random() < win_probability_1:
                winner, loser = group_1, group_2
            else:
                winner, loser = group_2, group_1

            # Replace the losing group with a (copied) version of the winning group
            new_group = copy.deepcopy(winner)
            loser_index = self.groups.index(loser)
            self.groups[loser_index] = new_group
            logging.info("Conflict resolved. Winner replaces loser.")
        
        
    # --- GROUP SPLITTING ---

    def split_group(self, index: int):
        """
        Split the group at the given index into two smaller groups of equal (or nearly equal) size.

        Args:
            index (int): The index of the group to split.
        """
        group = self.groups[index]

        new_group_1 = []
        new_group_2 = []

        # Randomly assign individuals to the new groups
        for individual in group:
            if random.random() < 0.5:
                new_group_1.append(individual)
            else:
                new_group_2.append(individual)

        if len(new_group_1) == 0 or len(new_group_2) == 0:
            # If one group is empty, merge them back together
            logging.info("Group splitting failed. Merging groups back together.")
            self.split_group(index)
        
        self.groups[index] = new_group_1
        self.groups[random.choice([i for i in range(len(self.groups)) if i != index])] = new_group_2

    def split_groups(self):
        """
        If a group exceeds the maximum size n, either split it (with probability q)
        or eliminate a random individual (with probability 1 - q).
        """
        for i, group in enumerate(self.groups):
            # Check if the group size exceeds the threshold
            if len(group) > n:
                if random.random() < q:
                    self.split_group(i)
                else:
                    # Eliminate a random individual
                    group.pop(random.randint(0, len(group) - 1))
                    logging.info(f"Removed an individual from oversized group {i}.")

    def reset_payoffs_and_fitness(self):
        """
        Reset the payoff and fitness values for all individuals in the population.
        """
        for group in self.groups:
            for individual in group:
                individual.payoff = 0.0
                individual.fitness = 0.0
    
    # --- SIMULATION ---

    def run_simulation(self):
        """
        Execute the full simulation loop until the population becomes homogeneous.
        The loop includes:
          1. Game play between individuals
          2. Fitness calculation
          3. Reproduction (with possible migration)
          4. Group conflict
          5. Group splitting (if needed)
        """
        logging.info("Starting simulation.")
        while not self.is_homogeneous():
            self.play_game()
            self.calculate_fitness()
            self.reproduce()
            #self.conflict_groups()
            self.conflict_groups_with_conflict_individuals()
            self.split_groups()
            self.calculate_fitness()
            self.reset_payoffs_and_fitness() # TODO check if necessary
        
        logging.info(f"Simulation complete. Population is homogeneous -> {self.get_homogeneous_strategy()}.")
        print(f"Population is homogeneous -> {self.get_homogeneous_strategy()}.")
        return self.get_homogeneous_strategy()
        

    # --- STRING REPRESENTATION ---

    def __str__(self):
        """
        Show a summary of the groups and their members.
        """
        to_return = ""
        for i, group in enumerate(self.groups):
            to_return += f"Group {i}:\n"
            for individual in group:
                to_return += f"  {individual}\n"
        return to_return
