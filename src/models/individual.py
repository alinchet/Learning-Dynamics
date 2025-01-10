from src.settings.constants import Strategy
from src.settings.config import w
from uuid import uuid4
import logging
import copy


class Individual:
    """
    Represents an individual with a strategy, payoff, fitness, and unique ID.
    """

    def __init__(
        self,
        strategy: Strategy = Strategy.EGOIST,
        payoff: float = 0.0,
        fitness: float = 0.0,
        id: str = None,
    ):
        self._strategy = strategy
        self._payoff = payoff
        self._fitness = fitness
        self._id = id or str(uuid4())
        logging.debug("Initialized Individual with ID=%s", self.id)

    # --- Properties ---
    @property
    def strategy(self) -> Strategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Strategy):
        if not isinstance(strategy, Strategy):
            raise ValueError(f"Invalid strategy: {strategy}")
        logging.debug("Updated strategy to %s for ID=%s", strategy, self.id)
        self._strategy = strategy

    @property
    def payoff(self) -> float:
        return self._payoff

    @payoff.setter
    def payoff(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError("Payoff must be a number (float or int).")
        self._payoff = float(value)

    @property
    def fitness(self) -> float:
        return self._fitness

    @fitness.setter
    def fitness(self, value: float):
        if not isinstance(value, (float, int)):
            raise TypeError("Fitness must be a number (float or int).")
        self._fitness = float(value)

    @property
    def id(self) -> str:
        return self._id

    # --- Methods ---
    def calculate_payoff(self, other: "Individual", payoff_matrix: list[list[float]]):
        """
        Updates payoff based on interaction with another individual.
        """
        if not isinstance(other, Individual):
            raise ValueError("Other must be an instance of Individual.")
        try:
            logging.debug("Calculating payoff for ID=%s vs ID=%s", self.id, other.id)
            self.payoff += payoff_matrix[self.strategy.value][other.strategy.value]
            logging.debug("Updated payoff to %.2f for ID=%s", self.payoff, self.id)
        except (IndexError, KeyError) as e:
            raise ValueError("Invalid strategy combination in payoff matrix.") from e

    def calculate_fitness(self) -> float:
        """
        Updates and returns fitness based on the payoff.
        """
        self.fitness = 1 - w + w * self.payoff
        logging.debug("Updated fitness to %.2f for ID=%s", self.fitness, self.id)
        return self.fitness

    def __copy__(self) -> "Individual":
        """Creates a shallow copy."""
        return Individual(
            strategy=self.strategy,
            payoff=self.payoff,
            fitness=self.fitness,
        )

    def __deepcopy__(self, memo) -> "Individual":
        """Creates a deep copy."""
        return Individual(
            strategy=copy.deepcopy(self.strategy, memo),
            payoff=copy.deepcopy(self.payoff, memo),
            fitness=copy.deepcopy(self.fitness, memo),
        )

    def __eq__(self, other: object) -> bool:
        """Compares based on unique ID."""
        return isinstance(other, Individual) and self.id == other.id

    def __hash__(self) -> int:
        """Ensures hash consistency."""
        return hash(self.id)

    def __repr__(self) -> str:
        return (f"Individual(id={self.id}, strategy={self.strategy}, "
                f"payoff={self.payoff}, fitness={self.fitness})")