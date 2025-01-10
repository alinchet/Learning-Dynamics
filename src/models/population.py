import logging
import random
import copy
from src.models.individual import Individual
from src.settings.constants import Strategy, A_IN_MATRIX, A_OUT_MATRIX
from src.settings.config import kappa, q, z, alpha, lambda_mig


class Population:
    """
    Represents a population of groups, where individuals interact, reproduce, and undergo conflicts.
    """

    def __init__(self, num_groups: int = 10, num_individuals: int = 10, mutant_strategy: Strategy = Strategy.ALTRUIST):
        """
        Initialize the population with groups of individuals, including a mutant.

        Args:
            num_groups (int): Number of groups.
            num_individuals (int): Number of individuals per group.
            mutant_strategy (Strategy): Strategy of the mutant individual.
        """
        logging.info(f"Initializing population with {num_groups} groups, {num_individuals} individuals each.")
        self.num_groups = num_groups
        self.num_individuals = num_individuals
        self.groups = self._initialize_population(mutant_strategy)

    def _initialize_population(self, mutant_strategy: Strategy) -> list[list[Individual]]:
        """
        Create groups of individuals with a single mutant in the first group.

        Args:
            mutant_strategy (Strategy): Strategy of the mutant.

        Returns:
            list[list[Individual]]: List of groups.
        """
        logging.info(f"Creating groups with one mutant of strategy {mutant_strategy}.")
        groups = [[Individual() for _ in range(self.num_individuals)] for _ in range(self.num_groups)]
        groups[0][0].strategy = mutant_strategy
        return groups

    # Population Analysis Methods

    def is_homogeneous(self) -> bool:
        """
        Determine if the population consists of a single strategy.

        Returns:
            bool: True if homogeneous, False otherwise.
        """
        first_strategy = self.groups[0][0].strategy
        return all(ind.strategy == first_strategy for group in self.groups for ind in group)

    def get_population_distribution(self) -> dict[Strategy, int]:
        """
        Count the occurrences of each strategy in the population.

        Returns:
            dict[Strategy, int]: Distribution of strategies.
        """
        distribution = {strategy: 0 for strategy in Strategy}
        for group in self.groups:
            for individual in group:
                distribution[individual.strategy] += 1
        return distribution

    def get_homogeneous_strategy(self) -> Strategy:
        """
        Retrieve the strategy of a homogeneous population.

        Returns:
            Strategy: Strategy if homogeneous; behavior undefined if not.
        """
        return self.groups[0][0].strategy

    # Interaction Methods

    def get_random_partner(self, individual: Individual) -> Individual | None:
        """
        Select a random partner for an individual based on in-group or out-group probabilities.

        Args:
            individual (Individual): The individual to find a partner for.

        Returns:
            Individual | None: A partner or None if no partner is available.
        """
        group_idx = self._get_group_index(individual)
        if group_idx is None:
            return None

        if random.random() < alpha:
            return self._random_in_group_member(individual, group_idx)
        return self._random_out_group_member(group_idx)

    def _get_group_index(self, individual: Individual) -> int | None:
        """
        Find the group index of a given individual.

        Args:
            individual (Individual): The individual to locate.

        Returns:
            int | None: Group index or None if not found.
        """
        for idx, group in enumerate(self.groups):
            if individual in group:
                return idx
        return None

    def _random_in_group_member(self, individual: Individual, group_index: int) -> Individual | None:
        """
        Select a random in-group partner for an individual.

        Args:
            individual (Individual): The individual to exclude.
            group_index (int): The group index.

        Returns:
            Individual | None: A partner or None if no other members are available.
        """
        in_group = [ind for ind in self.groups[group_index] if ind != individual]
        return random.choice(in_group) if in_group else None

    def _random_out_group_member(self, exclude_group_index: int) -> Individual | None:
        """
        Select a random individual from any group except the specified one.

        Args:
            exclude_group_index (int): Group index to exclude.

        Returns:
            Individual | None: A partner or None if no other groups are available.
        """
        out_group = [
            ind
            for idx, group in enumerate(self.groups)
            if idx != exclude_group_index
            for ind in group
        ]
        return random.choice(out_group) if out_group else None

    # Gameplay and Payoff Methods

    def play_game(self):
        """
        Simulate pairwise interactions and update payoffs.
        """
        for group in self.groups:
            for individual in group:
                partner = self.get_random_partner(individual)
                if not partner:
                    continue

                matrix = A_IN_MATRIX if self._get_group_index(individual) == self._get_group_index(partner) else A_OUT_MATRIX
                individual.calculate_payoff(partner, matrix)
                partner.calculate_payoff(individual, matrix)

    def calculate_fitness(self):
        """
        Update fitness for all individuals in the population.
        """
        for group in self.groups:
            for individual in group:
                individual.calculate_fitness()

    # Reproduction Methods

    def reproduce(self):
        """
        Simulate reproduction and potential migration.
        """
        new_individual, parent_group_idx = self._select_individual_for_duplication()

        if random.random() < lambda_mig:
            target_group_idx = random.choice([i for i in range(self.num_groups) if i != parent_group_idx])
            self.groups[target_group_idx].append(new_individual)
        else:
            self.groups[parent_group_idx].append(new_individual)

    def _select_individual_for_duplication(self) -> tuple[Individual, int]:
        """
        Select an individual for duplication using fitness-proportional probabilities.

        Returns:
            tuple[Individual, int]: The individual and its group's index.
        """
        total_fitness = sum(ind.fitness for group in self.groups for ind in group)
        if total_fitness == 0:
            random_group_idx = random.randint(0, self.num_groups - 1)
            random_individual = random.choice(self.groups[random_group_idx])
            return copy.deepcopy(random_individual), random_group_idx

        individuals = [ind for group in self.groups for ind in group]
        group_indices = [i for i, group in enumerate(self.groups) for _ in group]
        probabilities = [ind.fitness / total_fitness for ind in individuals]

        selected = random.choices(individuals, weights=probabilities, k=1)[0]
        selected_group_idx = group_indices[individuals.index(selected)]
        return copy.deepcopy(selected), selected_group_idx

    # --- GROUP CONFLICT ---

    def pair_groups(self) -> list[tuple[list[Individual], list[Individual]]]:
        """
        Randomly pairs groups for conflict. If the number of groups is odd,
        duplicate or remove a random group to make it even.

        Returns:
            list[tuple[list[Individual], list[Individual]]]: A list of paired groups.
        """
        groups_involved = []
        groups_not_involved = []

        for group in self.groups:
            if random.random()< kappa:
                groups_involved.append(group)
        groups_not_involved = [group for group in self.groups if group not in groups_involved]

        if (len(groups_involved) % 2) != 0:
            # Duplicate or remove a random group to make the number even

            if len(groups_involved) == len(self.groups):
                # If all groups are involved, we have to remove a random group
                random_group = random.choice(groups_involved)
                groups_involved.remove(random_group)
                logging.debug("Removed a random group for conflict.")
            else:
                if random.random() < 0.5:
                    # Add a group to groups_involved
                    random_group = random.choice(groups_not_involved)
                    groups_involved.append(random_group)
                    groups_not_involved.remove(random_group)
                    logging.debug("Duplicated a random group for conflict.")
                else:
                    # Remove a random group
                    groups_involved.pop(random.randint(0, len(groups_involved) - 1))
                    logging.debug("Removed a random group for conflict.")
        
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

        paired_groups = self.pair_groups()
    
        if not paired_groups:
            logging.info("No groups paired for conflict. Skipping conflict resolution.")
            return
        for group_1, group_2 in paired_groups:
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

    # --- GROUP SPLITTING ---

    def split_group(self, index: int):
        """
        Splits a group at the given index into two smaller groups.

        Args:
            index (int): The index of the group to split.
        """
        group = self.groups[index]
        new_group_1, new_group_2 = [], []

        for individual in group:
            (new_group_1 if random.random() < 0.5 else new_group_2).append(individual)

        if not new_group_1 or not new_group_2:
            logging.debug("One group is empty after split. Forcing redistribution.")
            self.split_group(index)

        self.groups[index] = new_group_1
        other_index = random.choice([i for i in range(len(self.groups)) if i != index])
        self.groups[other_index] = new_group_2
        logging.info(
            f"Group {index} split into two groups with sizes {len(new_group_1)} and {len(new_group_2)}."
        )

    def split_groups(self):
        """
        Splits or shrinks groups exceeding the maximum size `n`.
        """
        for i, group in enumerate(self.groups):
            if len(group) > self.num_individuals:
                if random.random() < q:
                    logging.info(f"Group {i} exceeds size limit. Attempting to split.")
                    self.split_group(i)
                else:
                    removed_individual = group.pop(random.randint(0, len(group) - 1))
                    logging.info(f"Group {i} exceeds size limit. Removed individual: {removed_individual}.")

    # --- PAYOFFS AND FITNESS ---

    def reset_payoffs_and_fitness(self):
        """
        Resets the payoff and fitness values for all individuals in all groups.
        """
        for group in self.groups:
            for individual in group:
                individual.payoff = 0.0
                individual.fitness = 0.0
        logging.info("Payoffs and fitness values reset for all individuals.")

    # --- SIMULATION ---

    def run_simulation(self) -> Strategy:
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
            logging.info("Population is not homogeneous. Continuing simulation.")
            
            # Step 1: Play the game between individuals
            self.play_game()

            # Step 2: Calculate fitness of all individuals
            self.calculate_fitness()

            # Step 3: Reproduce individuals (with migration)
            self.reproduce()

            # Step 4: Simulate group conflict
            self.conflict_groups()

            # Step 5: Split groups if necessary
            self.split_groups()

            # Recalculate fitness after group changes
            self.calculate_fitness()

            # Reset payoffs for the next iteration
            self.reset_payoffs_and_fitness()

        homogeneous_strategy = self.get_homogeneous_strategy()
        logging.info(f"Simulation complete. Population is homogeneous -> {homogeneous_strategy}.")
        return homogeneous_strategy

    # --- STRING REPRESENTATION ---

    def __str__(self):
        """
        Show a summary of the groups and their members.
        """
        logging.debug("Generating string representation of the population.")
        to_return = ""
        for i, group in enumerate(self.groups):
            to_return += f"Group {i}:\n"
            for individual in group:
                to_return += f"  {individual}\n"
        return to_return