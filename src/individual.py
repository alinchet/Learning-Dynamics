from src.constants import Strategy
from src.config import w
import copy
import uuid


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
            self.payoff = payoff_matrix[self.strategy.value][other.strategy.value]
        except (IndexError, KeyError):
            raise ValueError("Invalid strategy combination in payoff matrix.")

    def calculate_fitness(self) -> float:
        """
        Calculate and update fitness based on payoff.

        Returns:
            float: The calculated fitness value.
        """
        self.fitness = 1 - w + w * self.payoff
        return self.fitness
    
    # --- Copy Methods ---
    def __copy__(self):
        """
        Create a shallow copy of the individual.
        """
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
        return Individual(
            strategy=copy.deepcopy(self.strategy, memo),
            payoff=copy.deepcopy(self.payoff, memo),
            fitness=copy.deepcopy(self.fitness, memo),
            id=copy.deepcopy(self.id, memo)  # Preserve ID in deep copy
        )
    
    # --- Comparison Methods ---
    def __eq__(self, other):
        """Check equality based on the unique ID."""
        if isinstance(other, Individual):
            return self.id == other.id
        return False

    def __hash__(self):
        """Ensure hash consistency with equality."""
        return hash(self.id)

    # --- String Representation ---
    def __repr__(self):
        return (f"Individual(id={self.id}, strategy={self.strategy}, "
                f"payoff={self.payoff}, fitness={self.fitness})")