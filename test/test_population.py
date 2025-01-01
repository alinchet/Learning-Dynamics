import unittest
from src.population import Population
from src.individual import Individual
from src.constants import Strategy
import random


class TestPopulation(unittest.TestCase):

    def setUp(self):
        """Set up a default population for testing."""
        self.population = Population(num_groups=2, num_individuals=2)
        random.seed(42)  # Set seed for reproducibility

        # Create test individuals with different fitness values
        self.population.groups[0] = [
            Individual(strategy=Strategy.ALTRUIST, fitness=5.0),
            Individual(fitness=4.0),
            Individual(fitness=3.0)
        ]
        self.population.groups[1] = [
            Individual(fitness=2.0),
            Individual(fitness=1.0),
            Individual(fitness=1.0)
        ]

    # --- POPULATION ANALYSIS TESTS ---

    def test_is_homogeneous_false(self):
        """Test that is_homogeneous returns False for a non-homogeneous population."""
        self.assertFalse(self.population.is_homogeneous())

    def test_get_group(self):
        """Test get_group returns the correct group index for an individual."""
        individual = self.population.groups[0][0]
        self.assertEqual(self.population.get_group(individual), 0)

    def test_get_group_none(self):
        """Test get_group returns None for an individual not in any group."""
        outsider = Individual()
        self.assertIsNone(self.population.get_group(outsider))

    def test_are_in_same_group_true(self):
        """Test are_in_same_group returns True for individuals in the same group."""
        self.assertTrue(self.population.are_in_same_group(
            self.population.groups[0][0], self.population.groups[0][1]))

    def test_are_in_same_group_false(self):
        """Test are_in_same_group returns False for individuals in different groups."""
        self.assertFalse(self.population.are_in_same_group(
            self.population.groups[0][0], self.population.groups[1][0]))

    # --- GAME PLAY LOGIC TESTS ---

    def test_pair_individuals(self):
        """Test pairing individuals across groups."""
        pairs, _ = self.population.pair_individuals()
        self.assertEqual(len(pairs), 3)

    def test_play_game(self):
        """Test that play_game executes without errors."""
        self.population.play_game()

    # --- FITNESS TESTS ---

    def test_calculate_fitness(self):
        """Test calculate_fitness updates fitness values."""
        initial_fitness = self.population.groups[0][0].fitness
        self.population.calculate_fitness()
        self.assertNotEqual(initial_fitness, self.population.groups[0][0].fitness)

    # --- REPRODUCTION TESTS ---

    def test_select_individual_for_duplication(self):
        """Test select_individual_for_duplication returns a valid individual and group index."""
        individual, group_index = self.population.select_individual_for_duplication()
        self.assertIsInstance(individual, Individual)
        self.assertIn(group_index, [0, 1])

    def test_reproduce(self):
        """Test reproduce increases population size."""
        initial_size = sum(len(group) for group in self.population.groups)
        self.population.reproduce()
        new_size = sum(len(group) for group in self.population.groups)
        self.assertGreater(new_size, initial_size)

    # --- CONFLICT TESTS ---

    def test_pair_groups(self):
        """Test pairing groups for conflict."""
        pairs = self.population.pair_groups()
        self.assertEqual(len(pairs), 1)  # Only 2 groups, so 1 pair

    def test_conflict_groups(self):
        """Test conflict_groups resolves conflicts."""
        initial_size = len(self.population.groups)
        self.population.conflict_groups()
        self.assertEqual(len(self.population.groups), initial_size)

    # --- GROUP SPLITTING TESTS ---

    def test_split_group(self):
        """Test split_group splits a group into two."""
        initial_group_count = len(self.population.groups)
        self.population.split_group(0)
        self.assertEqual(len(self.population.groups), initial_group_count + 1)
        self.assertEqual(len(self.population.groups[0]), 1)  # Half of 3 rounded down

    # def test_split_groups(self):
    #     """Test split_groups either splits or eliminates individuals."""
    #     initial_size = sum(len(group) for group in self.population.groups)
    #     self.population.split_groups()
    #     new_size = sum(len(group) for group in self.population.groups)
    #     self.assertNotEqual(initial_size, new_size)

    # --- SIMULATION TESTS ---

    def test_run_simulation(self):
        """Test that run_simulation terminates without errors."""
        self.population.run_simulation()
        self.assertTrue(self.population.is_homogeneous())

    # --- STRING REPRESENTATION TEST ---

    def test_str(self):
        """Test string representation of the population."""
        result = str(self.population)
        self.assertIn("Group 0:", result)
        self.assertIn("Group 1:", result)


if __name__ == '__main__':
    unittest.main()