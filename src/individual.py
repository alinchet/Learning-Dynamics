from src.constants import Strategy
from src.config import w
import logging
import copy
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Individual:
    """
    Represents an individual with a strategy, payoff, fitness, and unique ID.
    """

    def __init__(
        self,
        strategy: Strategy = Strategy.EGOIST,
        payoff: float = 0.0,
        fitness: float = 0.0,
        id: str = None
    ):
        """
        Initialize an Individual with a strategy, payoff, fitness, and ID.

        Args:
            strategy (Strategy): The individual's strategy.
            payoff (float): Initial payoff value (default 0.0).
            fitness (float): Initial fitness value (default 0.0).
            id (str): Unique identifier for the individual (optional).
        """
        self.strategy = strategy
        self.payoff = payoff
        self.fitness = fitness
        self.id = id if id else str(uuid.uuid4())
        logging.info("Individual initialized with ID=%s", self.id)

    # --- Properties ---
    @property
    def strategy(self) -> Strategy:
        """Get the strategy of the individual."""
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Strategy):
        """Set the strategy, ensuring it is valid."""
        if not isinstance(strategy, Strategy):
            raise ValueError(f"Invalid strategy: {strategy}")
        logging.info("Setting strategy to %s for Individual ID=%s", strategy, self.id)
        self._strategy = strategy

    @property
    def payoff(self) -> float:
        """Get the payoff of the individual."""
        return self._payoff

    @payoff.setter
    def payoff(self, payoff: float):
        """Set the payoff, ensuring it is a valid number."""
        if not isinstance(payoff, (float, int)):
            raise TypeError("Payoff must be a number (float or int).")
        logging.info("Setting payoff to %.2f for Individual ID=%s", float(payoff), self.id)
        self._payoff = float(payoff)

    @property
    def fitness(self) -> float:
        """Get the fitness of the individual."""
        return self._fitness

    @fitness.setter
    def fitness(self, fitness: float):
        """Set the fitness, ensuring it is a valid number."""
        if not isinstance(fitness, (float, int)):
            raise TypeError("Fitness must be a number (float or int).")
        logging.info("Setting fitness to %.2f for Individual ID=%s", float(fitness), self.id)
        self._fitness = float(fitness)

    @property
    def id(self) -> str:
        """Get the ID of the individual."""
        return self._id

    @id.setter
    def id(self, id: str):
        """Set the ID, ensuring it is a valid string."""
        if not isinstance(id, str):
            raise TypeError("ID must be a string.")
        logging.info("Setting ID to %s", id)
        self._id = id

    # --- Methods ---
    def calculate_payoff(self, other: 'Individual', payoff_matrix: list[list[float]]):
        """
        Calculate the payoff based on interaction with another individual.

        Args:
            other (Individual): The other individual in the interaction.
            payoff_matrix (list[list[float]]): Payoff matrix for strategies.
        """
        try:
            logging.info("Calculating payoff for Individual ID=%s against Individual ID=%s", 
                         self.id, other.id)
            self.payoff = payoff_matrix[self.strategy.value][other.strategy.value]
            logging.info("Payoff updated to %.2f for Individual ID=%s", self.payoff, self.id)
        except (IndexError, KeyError):
            raise ValueError("Invalid strategy combination in payoff matrix.")

    def calculate_fitness(self) -> float:
        """
        Calculate and update fitness based on payoff.

        Returns:
            float: The calculated fitness value.
        """
        logging.info("Calculating fitness for Individual ID=%s with payoff=%.2f", 
                     self.id, self.payoff)
        self.fitness = 1 - w + w * self.payoff
        logging.info("Fitness updated to %.2f for Individual ID=%s", self.fitness, self.id)
        return self.fitness
    
    # --- Copy Methods ---
    def __copy__(self):
        """
        Create a shallow copy of the individual.
        """
        logging.info("Creating shallow copy of Individual ID=%s", self.id)
        return Individual(
            strategy=self.strategy,
            payoff=self.payoff,
            fitness=self.fitness,
            id=self.id  # Preserve ID in shallow copy
        )

    def __deepcopy__(self, memo):
        """
        Create a deep copy of the individual.
        """
        logging.info("Creating deep copy of Individual ID=%s", self.id)
        return Individual(
            strategy=copy.deepcopy(self.strategy, memo),
            payoff=copy.deepcopy(self.payoff, memo),
            fitness=copy.deepcopy(self.fitness, memo),
            id=copy.deepcopy(self.id, memo)  # Preserve ID in deep copy
        )
    
    # --- Comparison Methods ---
    def __eq__(self, other):
        """Check equality based on the unique ID."""
        result = isinstance(other, Individual) and self.id == other.id
        logging.info("Comparing Individual ID=%s to Individual ID=%s: %s", 
                     self.id, other.id if isinstance(other, Individual) else "N/A", result)
        return result

    def __hash__(self):
        """Ensure hash consistency with equality."""
        return hash(self.id)

    # --- String Representation ---
    def __repr__(self):
        return (f"Individual(id={self.id}, strategy={self.strategy}, "
                f"payoff={self.payoff}, fitness={self.fitness})")