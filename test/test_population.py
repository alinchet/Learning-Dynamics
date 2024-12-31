import unittest
from src.constants import Strategy
from src.population import Population


class TestPopulation(unittest.TestCase):

    def setUp(self):
        """Set up a default population for testing."""
        self.population = Population(num_groups=5, num_individuals=5, mutant_strategy=Strategy.ALTRUIST)
        self.individual_1 = self.population.groups[0][0]
        self.individual_2 = self.population.groups[0][1]
        self.individual_3 = self.population.groups[1][0]

    def test_initialization(self):
        """Test that the population is initialized correctly."""
        self.assertEqual(len(self.population.groups), 5)  # 5 groups
        self.assertEqual(len(self.population.groups[0]), 5)  # 5 individuals per group
        self.assertEqual(self.population.groups[0][0].strategy, Strategy.ALTRUIST)  # First individual is a mutant

    def test_is_homogeneous(self):
        """Test if the population is homogeneous."""
        self.assertFalse(self.population.is_homogeneous())
        # Manually make the population homogeneous
        for group in self.population.groups:
            for individual in group:
                individual.strategy = Strategy.EGOIST
        self.assertTrue(self.population.is_homogeneous())

    def test_get_group(self):
        """Test the get_group method."""
        group_index = self.population.get_group(self.individual_1)
        self.assertEqual(group_index, 0)  # The first individual should belong to group 0

    def test_are_in_same_group(self):
        """Test if two individuals are in the same group."""
        self.assertTrue(self.population.are_in_same_group(self.individual_1, self.individual_2))
        self.assertFalse(self.population.are_in_same_group(self.individual_1, self.individual_3))

    def test_pair_individuals(self):
        """Test pairing of individuals across groups."""
        pairs, _ = self.population.pair_individuals(alpha=0.5)
        self.assertGreater(len(pairs), 0)  # There should be at least one pair
        self.assertEqual(len(pairs[0]), 2)  # Each pair should have two individuals

    def test_play_game(self):
        """Test the game simulation between paired individuals."""
        self.population.play_game(alpha=0.5)  # Should not raise any exceptions
        # Check if payoffs have been calculated (e.g., by checking their fitness)
        self.assertIsNotNone(self.individual_1.payoff)

    def test_select_individual_for_duplication(self):
        """Test fitness-proportional selection for duplication."""
        individual = self.population.select_individual_for_duplication()
        self.assertIn(individual, [ind for group in self.population.groups for ind in group])

    def test_reproduce(self):
        """Test reproduction in the population."""
        initial_population_size = sum(len(group) for group in self.population.groups)
        self.population.reproduce()
        new_population_size = sum(len(group) for group in self.population.groups)
        self.assertGreater(new_population_size, initial_population_size)  # Population size should increase

    def test_split_groups(self):
        """Test the splitting of groups if they exceed the size threshold."""
        original_group_size = len(self.population.groups[0])
        self.population.split_groups()
        new_group_size = len(self.population.groups[0])
        self.assertLess(new_group_size, original_group_size)  # Group should be split

    def test_conflict_groups(self):
        """Test conflict resolution between groups."""
        original_fitness_group_1 = sum(individual.fitness for individual in self.population.groups[0])
        original_fitness_group_2 = sum(individual.fitness for individual in self.population.groups[1])
        self.population.conflict_groups()
        new_fitness_group_1 = sum(individual.fitness for individual in self.population.groups[0])
        new_fitness_group_2 = sum(individual.fitness for individual in self.population.groups[1])

        # The fitness of the winning group should be greater
        self.assertNotEqual(original_fitness_group_1, new_fitness_group_1)
        self.assertNotEqual(original_fitness_group_2, new_fitness_group_2)

    def test_run_simulation(self):
        """Test running the full simulation process."""
        # To test the full simulation, we run it and ensure no exceptions are thrown
        self.population.run_simulation()  # Should run without any errors


if __name__ == "__main__":
    unittest.main()