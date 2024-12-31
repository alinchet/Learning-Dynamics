# **Simulation of Parochial Altruism by Multilevel Selection**  

This project implements the simulation model described in the paper *"Evolution of Parochial Altruism by Multilevel Selection"*. It simulates the dynamics of altruism and parochialism in a population divided into multiple groups, exploring how these traits evolve under selective pressures from within-group and between-group interactions.  

---

## **Overview**  

The model represents an **absorbing Markov chain** where a mutant strategy (either altruistic or parochial) spreads or dies out in a population initially dominated by egoists. Key processes include:  

1. **Reproduction**: Individuals duplicate based on fitness, migrate, or stay within their group.  
2. **Conflict**: Groups engage in contests, and winners replace losing groups.  
3. **Splitting**: Groups split into smaller groups once they exceed a maximum size.  
4. **Absorption**: The simulation continues until the population is homogeneous (either all mutants or all incumbents).  

---

## **Key Features**  

- **Fitness-Driven Selection**: Reproduction depends on fitness values derived from interactions within and between groups.  
- **Dynamic Group Conflicts**: Groups compete, and winners are determined probabilistically based on payoffs.  
- **Splitting Mechanism**: Groups split when they exceed a defined size, maintaining structure and introducing assortment effects.  
- **Parameter Tuning**: Flexible settings for group size, conflict frequency, migration rates, and interaction probabilities.  
- **Fixation Probability Calculation**: Estimates the probability of mutant strategies reaching fixation compared to neutral drift.  

---

## **Model Parameters**  

| Parameter                                         | Range (Default)    |
|---------------------------------------------------|--------------------|
| **κ** (Average Frequency of Groups in Conflict)   | 0.0–0.1 (0.025)    |
| **q** (Splitting Probability)                     | 0–1 (0.01)         |
| **n** (Group Size)                                | 5–20 (10)          |
| **m** (Number of Groups)                          | 5–20 (10)          |
| **b/c** (Benefit-Cost Ratio)                      | 1.5–5 (2.0)        |
| **z** (Steepness of Winning Probability Curve)    | 0–1 (0.5)          |
| **α** (Ingroup Interaction Frequency)             | 0–1 (0.8)          |
| **λ** (Migration Rate)                            | 0–1 (0.0)          |
| **w** (Selection Intensity)                       | 0–1 (0.1)          |

---

## **Payoff Matrices**  

### **Ingroup Payoffs**  

|               | **A**  | **P**  | **E**  |
|---------------|:------:|:------:|:------:|
| **A**         | b − c  | b − c  | −c     |
| **P**         | b − c  | b − c  | −c     |
| **E**         | b      | b      | 0      |

### **Outgroup Payoffs**  

|               | **A**  | **P**  | **E**  |
|---------------|:------:|:------:|:------:|
| **A**         | b − c  | −c     | −c     |
| **P**         | b      | 0      | 0      |
| **E**         | b      | 0      | 0      |

---

## **Installation**  

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/alinchet/Learning-Dynamics.git
   cd Learning-Dynamics
   ```

2. **Set up a Python Environment**  
   ```bash
   python3 -m venv env
   source env/bin/activate
   pip install -r requirements.txt
   ```

3. **Run the Simulation**  
   ```bash
   python src/main.py
   ```

3. **Run a Test**  
   ```bash
   python -m unittest discover -s test -p "test_individual.py"
   python -m unittest discover -s test -p "test_population.py"
   ```

