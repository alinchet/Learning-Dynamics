import unittest
from src.classes.individual import Individual
from src.settings.constants import Strategy, A_IN_MATRIX, A_OUT_MATRIX
from src.settings.config import c, w

class TestIndividual(unittest.TestCase):

    # Test initialization with default values
    def test_initialization_default(self):
        individual = Individual()
        self.assertEqual(individual.strategy, Strategy.EGOIST)
        self.assertEqual(individual.payoff, 0.0)
        self.assertEqual(individual.fitness, 0.0)

    # Test initialization with custom values
    def test_initialization_custom(self):
        individual = Individual(strategy=Strategy.ALTRUIST, payoff=2.0, fitness=0.5)
        self.assertEqual(individual.strategy, Strategy.ALTRUIST)
        self.assertEqual(individual.payoff, 2.0)
        self.assertEqual(individual.fitness, 0.5)

    # Test invalid strategy type
    def test_invalid_strategy(self):
        with self.assertRaises(ValueError):
            individual = Individual(strategy="INVALID")

    # Test invalid payoff type
    def test_invalid_payoff(self):
        individual = Individual()
        with self.assertRaises(TypeError):
            individual.payoff = "invalid"

    # Test invalid fitness type
    def test_invalid_fitness(self):
        individual = Individual()
        with self.assertRaises(TypeError):
            individual.fitness = "invalid"

    # Test payoff calculation for different strategy interactions
    def test_calculate_payoff(self):
        individual1 = Individual(strategy=Strategy.ALTRUIST)
        individual2 = Individual(strategy=Strategy.EGOIST)
        individual1.calculate_payoff(individual2, payoff_matrix=A_IN_MATRIX)
        self.assertEqual(individual1.payoff, - c)

    # Test fitness calculation
    def test_calculate_fitness(self):
        individual = Individual(strategy=Strategy.EGOIST, payoff=2.0)
        fitness = individual.calculate_fitness()
        expected_fitness = 1 - w + w * 2.0
        self.assertEqual(fitness, expected_fitness)

    # Test copy method (shallow copy)
    def test_copy(self):
        individual = Individual(strategy=Strategy.PAROCHIALIST, payoff=1.0, fitness=0.5)
        individual_copy = individual.__copy__()
        self.assertEqual(individual.strategy, individual_copy.strategy)
        self.assertEqual(individual.payoff, individual_copy.payoff)
        self.assertEqual(individual.fitness, individual_copy.fitness)
        self.assertIsNot(individual, individual_copy)  # Ensure it's a new object

    # Test deepcopy method
    def test_deepcopy(self):
        individual = Individual(strategy=Strategy.ALTRUIST, payoff=3.0, fitness=0.8)
        individual_deepcopy = individual.__deepcopy__({})
        self.assertEqual(individual.strategy, individual_deepcopy.strategy)
        self.assertEqual(individual.payoff, individual_deepcopy.payoff)
        self.assertEqual(individual.fitness, individual_deepcopy.fitness)
        self.assertIsNot(individual, individual_deepcopy)  # Ensure it's a new object

    # Test invalid payoff matrix interaction
    def test_invalid_payoff_matrix(self):
        individual1 = Individual(strategy=Strategy.ALTRUIST)
        individual2 = Individual(strategy=Strategy.PAROCHIALIST)
        with self.assertRaises(ValueError):
            individual1.calculate_payoff(individual2, payoff_matrix=[[]])  # Invalid matrix

if __name__ == "__main__":
    unittest.main()