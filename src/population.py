from src.individual import Individual
from src.constants import Strategy, A_IN_MATRIX, A_OUT_MATRIX
from src.config import n, q, lambda_mig, alpha
import logging
import random
import copy

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Population:
    """Class to represent a population of groups."""

    # --- INITIALIZATION ---

    def __init__(self, num_groups: int = 10, num_individuals: int = 10, mutant_strategy: Strategy = Strategy.ALTRUIST):
        """
        Initialize a population with groups of individuals.

        Args:
            num_groups (int): Number of groups.
            num_individuals (int): Number of individuals per group.
            mutant_strategy (Strategy): Strategy for the mutant individual.
        """
        logging.info(f"Initializing population with {num_groups} groups, {num_individuals} individuals each.")
        self.num_groups = num_groups
        self.num_individuals = num_individuals
        self.groups = self._initialize_population(mutant_strategy)

    def _initialize_population(self, mutant_strategy: Strategy) -> list[list[Individual]]:
        """
        Create groups with individuals, introducing one mutant.

        Args:
            mutant_strategy (Strategy): Strategy for the mutant individual.

        Returns:
            list[list[Individual]]: Groups of individuals.
        """
        logging.info(f"Creating groups of egoists with a single mutant of strategy {mutant_strategy}.")

        # Create groups with egoist individuals by default
        groups = [[Individual() for _ in range(self.num_individuals)] for _ in range(self.num_groups)]
        
        # Introduce a mutant in the first group
        groups[0][0].strategy = mutant_strategy
        
        return groups

    # --- POPULATION ANALYSIS ---

    def is_homogeneous(self) -> bool:
        """
        Check if the population is homogeneous, i.e., 
        consists entirely of either egoists or mutants.

        Returns:
            bool: True if the population is homogeneous, False otherwise.
        """
        strategy = self.groups[0][0].strategy
        homogeneous = all(individual.strategy == strategy for group in self.groups for individual in group)
        logging.info(f"Population homogeneous: {homogeneous}")
        return homogeneous

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

    # --- GAME PLAY LOGIC ---

    def get_random_partner(self, individual) -> Individual:
        """
        Get a random partner for an individual.

        Args:
            individual (Individual): The individual for which to find a partner.

        Returns:
            Individual: A random partner for the individual.
        """
        individuals = self.get_flattened_population()
        individuals.remove(individual)
        partner = random.choice(individuals)
        logging.debug(f"Selected random partner for individual {individual}.")
        return partner

    def play_game(self):
        """
        Simulate interactions between paired individuals.
        """
        logging.info("Playing game between individuals.")
        for group in self.groups:
            for individual in group:
                partner = self.get_random_partner(individual)

                # Determine interaction matrix based on group membership
                matrix = A_IN_MATRIX if self.are_in_same_group(individual, partner) else A_OUT_MATRIX

                # Calculate payoffs for both individuals
                individual.calculate_payoff(partner, matrix)
                partner.calculate_payoff(individual, matrix)

    def calculate_fitness(self):
        """
        Calculate and update fitness for all individuals in the population.
        """
        logging.info("Calculating fitness for all individuals.")
        for group in self.groups:
            for individual in group:
                individual.calculate_fitness()
    
    def random_out_group_member(self, exclude_group=None) -> Individual:
        """
        Selects a random individual from an out-group.

        Args:
            exclude_group (list[Individual]): Group to exclude (in-group).

        Returns:
            Individual: A random individual from an out-group.
        """
        out_group = [ind for group in self.groups if group != exclude_group for ind in group]
        return random.choice(out_group)

    # --- REPRODUCTION ---

    def select_individual_for_duplication(self) -> tuple[Individual, int]:
        """
        Select an individual for duplication based on fitness-proportional probabilities,
        and return the individual along with the index of the group it was selected from.

        Returns:
            tuple: A tuple containing the selected individual and the index of the group it was selected from.
        """
        # Compute total fitness across all groups
        total_fitness = sum(individual.fitness for group in self.groups for individual in group)

        # Handle edge case where all individuals have zero fitness
        if total_fitness == 0:
            logging.warning("All individuals have zero fitness. Selecting randomly.")
            # Select randomly if no fitness differentiation exists
            group_index = random.randint(0, len(self.groups) - 1)
            individual = random.choice(self.groups[group_index])
            return copy.copy(individual), group_index

        # Calculate fitness-proportional probabilities
        probabilities = [individual.fitness / total_fitness for group in self.groups for individual in group]
        individuals = [individual for group in self.groups for individual in group]
        group_indices = [i for i in range(len(self.groups)) for _ in self.groups[i]]

        # Select one individual based on fitness-weighted probabilities
        selected_individual = random.choices(individuals, weights=probabilities, k=1)[0]

        # Find the group index of the selected individual
        selected_group_index = group_indices[individuals.index(selected_individual)]

        logging.info(f"Selected individual {selected_individual} from group {selected_group_index} for duplication.")
        return copy.copy(selected_individual), selected_group_index

    def reproduce(self):
        """ Simulate reproduction based on fitness-proportional selection. """
        # Select an individual to duplicate
        new_individual, parent_group_index = self.select_individual_for_duplication()

        if random.random() < lambda_mig:
            # Migration: Add to a random different group
            target_group_index = random.choice(
                [i for i in range(len(self.groups)) if i != parent_group_index]
            )
            self.groups[target_group_index].append(new_individual)
            logging.info(f"New individual migrated to group {target_group_index}.")
        else:
            # Stay in the same group
            self.groups[parent_group_index].append(new_individual)
            logging.info(f"New individual added to group {parent_group_index}.")

    # --- GROUP CONFLICT ---

    def pair_groups(self) -> list[tuple[list[Individual], list[Individual]]]:
        """
        Randomly pairs groups for conflicts. Ensures an even number of groups.

        Returns:
            list[tuple[list[Individual], list[Individual]]]: Paired groups for conflict.
        """
        indices = list(range(len(self.groups)))

        # If the number of groups is odd, duplicate or remove a random group to ensure even pairing
        if len(indices) % 2 == 1:
            if random.random() < 0.5:
                indices.append(random.choice(indices))  # Duplicate a random group
            else:
                indices.remove(random.choice(indices))  # Remove a random group

        random.shuffle(indices)
        # Create pairs of groups for conflict
        return [(self.groups[indices[i]], self.groups[indices[i + 1]]) for i in range(0, len(indices), 2)]

    def conflict_groups(self):
        """
        Simulate conflicts between paired groups. 
        Winning group replaces the losing group based on fitness comparison.
        """
        logging.info("Simulating conflicts between groups.")
        for group_1, group_2 in self.pair_groups():
            # Calculate the total payoff (fitness) of each group
            fitness_1 = sum(individual.fitness for individual in group_1)
            fitness_2 = sum(individual.fitness for individual in group_2)

            # Determine the winning group based on fitness comparison
            if fitness_1 > fitness_2:
                winner, loser = group_1, group_2
            elif fitness_2 > fitness_1:
                winner, loser = group_2, group_1
            else:  # If equal fitness, pick a random winner
                winner, loser = (group_1, group_2) if random.random() < 0.5 else (group_2, group_1)

            # Replace the losing group with a copy of the winning group
            new_group = [copy.copy(individual) for individual in winner]
            self.groups[self.groups.index(loser)] = new_group
            logging.info(f"Conflict resolved. Winner replaces loser.")
        
     # --- GROUP SPLITTING ---

    def split_group(self, index: int):
        """
        Split a group into two smaller groups.

        Args:
            index (int): Index of the group to split.
        """
        group = self.groups[index]
        half = len(group) // 2
        # Split the group into two smaller groups
        self.groups[index] = group[:half]
        self.groups.append(group[half:])
        logging.info(f"Group {index} split into two.")

    def split_groups(self):
        """ Split oversized groups or eliminate individuals based on group size. """
        for i, group in enumerate(self.groups):
            # Check if the group size exceeds the threshold
            if len(group) > n:
                if random.random() < q:
                    # Split the group
                    self.split_group(i)
                else:
                    # Eliminate a random individual from the group
                    group.pop(random.randint(0, len(group) - 1))
                    logging.info(f"Removed individual from oversized group {i}.")

    # --- SIMULATION ---

    def run_simulation(self):
        """
        Execute the full simulation process.
        """
        logging.info("Starting simulation.")
        while not self.is_homogeneous():
            self.play_game()
            self.calculate_fitness()
            self.reproduce()
            self.conflict_groups()
            self.split_groups()
            self.calculate_fitness()
        logging.info("Simulation complete. Population is homogeneous.")
    
    # --- String Representation ----
    def __str__(self):
        to_return = ""
        for i, group in enumerate(self.groups):
            to_return += f"Group {i}:\n"
            for individual in group:
                to_return += f"\t{individual}\n"
        return to_return