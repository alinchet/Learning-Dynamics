#!/usr/bin/env python3
"""
Python script to simulate the evolution of parochial (vs. indiscriminate) altruism
by multilevel selection, roughly following Section 4 of García & van den Bergh (2011).

We implement:
1) A population of m groups, each of size up to n.
2) One-step life cycle per generation:
   a) Pairwise interactions (within- or between-group) to calculate payoffs and fitness.
   b) Moran reproduction of exactly one individual, possibly migrating.
   c) Conflict between groups (fraction k of them), with winners duplicating.
   d) Splitting if groups exceed size n (with probability q).

We run until the population is homogeneous, and record fixation probabilities.

Requires: numpy, matplotlib
"""

import numpy as np
import matplotlib.pyplot as plt
import random

# -------------------------------------------------------
# Global utility functions for the PD payoff
# -------------------------------------------------------

def payoff_pair(s1, s2, b, c, same_group=True):
    """
    Returns (payoff_to_s1, payoff_to_s2) from a single PD-like encounter
    given the strategies of each player, s1 and s2 in { 'E', 'A', 'P' }.
    - 'E': Egoist (always defect)
    - 'A': Altruist (cooperate vs. in- and out-group)
    - 'P': Parochialist (cooperate vs. in-group, defect vs. out-group)

    b = benefit of receiving cooperation
    c = cost of cooperating
    same_group = True if they are from same group, else False
    """

    # If an altruist, cooperates always
    def cooperates(strategy, same_grp):
        if strategy == 'E':
            return False
        elif strategy == 'A':
            return True
        elif strategy == 'P':
            # parochialist cooperates only if same group
            return True if same_grp else False

    c1 = cooperates(s1, same_group)
    c2 = cooperates(s2, same_group)

    # payoff to s1
    payoff1 = (b if c2 else 0) - (c if c1 else 0)
    # payoff to s2
    payoff2 = (b if c1 else 0) - (c if c2 else 0)

    return payoff1, payoff2

# -------------------------------------------------------
# Main simulation of the multilevel selection process
# -------------------------------------------------------

def run_simulation(
    m=10,          # number of groups
    n=10,          # target group size
    b=2.0,         # benefit
    c=1.0,         # cost
    alpha=0.8,     # prob of in-group interaction
    w=0.1,         # intensity of selection
    k=0.025,       # fraction of groups in conflict
    q=0.01,        # group splitting probability
    lambd=0.0,     # migration probability
    z=0.5,         # conflict outcome steepness
    strategy_mut='A',   # 'A' or 'P' for the cooperator mutant
    max_steps=10_000,
    reshuffle=False,
    seed=None
):
    """
    Run one replicate of the entire process, starting with
    a population of Egoists except for ONE mutant of type `strategy_mut`.

    Returns:
        'A' if final population is homogeneous altruist,
        'P' if final population is homogeneous parochialist,
        'E' if final population is homogeneous egoist.
        (We only placed a single "X" mutant, so either E or X wins.)
    """

    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    # Initialize population
    # We'll store it as a list of lists, population[g] is the list of strategies in group g
    # Each group has exactly n individuals, except for we place 1 mutant in a random location
    population = [['E']*n for _ in range(m)]
    # place the single mutant in a random group, random slot:
    g_idx = random.randrange(m)
    i_idx = random.randrange(n)
    population[g_idx][i_idx] = strategy_mut

    # Helper function
    def get_all_strategies():
        """Return a list of all (group, index_in_group, strategy)."""
        # Also keep track easily of total population size:
        all_individuals = []
        for gg in range(m):
            for ii, st in enumerate(population[gg]):
                all_individuals.append((gg, ii, st))
        return all_individuals

    def is_homogeneous():
        """Check if entire population is one strategy."""
        strategies = []
        for gg in range(m):
            strategies.extend(population[gg])
        unique = set(strategies)
        if len(unique) == 1:
            return list(unique)[0]  # return that single strategy
        return None

    # We define a function to compute payoffs for everyone
    def compute_payoffs():
        """
        Each individual i interacts with probability alpha with in-group,
        and (1-alpha) with out-group. For simplicity, let each individual
        have ~2 encounters on average. We do exactly 2 interactions per individual:
          1 with prob alpha from their group
          1 with prob (1-alpha) from outside
        (Or you can do a random draw each time, but the average is simpler.)
        Return an array pay[g][i] with the total payoff of individual i in group g.
        """

        pay = [[0.0]*len(population[gg]) for gg in range(m)]

        all_inds = get_all_strategies()
        total_popsize = len(all_inds)

        for (gg, ii, st) in all_inds:
            # 1) In-group match
            if len(population[gg]) > 1:  # only if at least 2 people
                partner_i = ii
                while partner_i == ii:
                    partner_i = random.randrange(len(population[gg]))
                st_p = population[gg][partner_i]
                p1, p2 = payoff_pair(st, st_p, b, c, same_group=True)
                pay[gg][ii] += p1
                pay[gg][partner_i] += p2

            # 2) Out-group match
            if m > 1:
                # pick a random group that is not gg
                other_gg = gg
                while other_gg == gg:
                    other_gg = random.randrange(m)
                if len(population[other_gg]) > 0:
                    partner_idx = random.randrange(len(population[other_gg]))
                    st_p = population[other_gg][partner_idx]
                    p1, p2 = payoff_pair(st, st_p, b, c, same_group=False)
                    pay[gg][ii] += p1
                    pay[other_gg][partner_idx] += p2

        return pay

    # We define a function for the conflict step
    def do_conflict_step(pay):
        """
        A fraction k of groups on average are chosen to fight in pairs.
        If there's an odd number, we handle that by random add/drop (as in the paper).
        For simplicity, we'll do: from the m groups, pick each group for conflict with prob k,
        then randomly match them in pairs. If there's leftover, ignore it.
        The winner duplicates, replacing the loser group.
        pay[g] = sum of payoffs in group g
        """
        # which groups are flagged for conflict
        groups_in_conflict = []
        for gg in range(m):
            # Bernoulli(k) test:
            if random.random() < k:
                groups_in_conflict.append(gg)

        # shuffle and pair them up
        random.shuffle(groups_in_conflict)
        pairs = []
        while len(groups_in_conflict) >= 2:
            g1 = groups_in_conflict.pop()
            g2 = groups_in_conflict.pop()
            pairs.append((g1, g2))

        # for each pair, fight:
        for (g1, g2) in pairs:
            G1 = pay[g1]
            G2 = pay[g2]
            # total payoff:
            sum1 = sum(G1)
            sum2 = sum(G2)
            # Probability that group g1 wins:
            #    P(g1 wins) = (sum1^(1/z)) / (sum1^(1/z) + sum2^(1/z))
            # If sum1 == sum2 == 0 => tie => pick random
            # handle corner cases:
            if (sum1 == 0.0 and sum2 == 0.0):
                # random 50/50
                if random.random() < 0.5:
                    winner, loser = g1, g2
                else:
                    winner, loser = g2, g1
            else:
                sum1z = sum1**(1.0/z) if sum1>0 else 0.0
                sum2z = sum2**(1.0/z) if sum2>0 else 0.0
                if random.random() < (sum1z/(sum1z+sum2z+1e-12)):
                    winner, loser = g1, g2
                else:
                    winner, loser = g2, g1

            # replicate winner's group
            population[loser] = [st for st in population[winner]]

    # If reshuffle == True, we ignore group structure each generation
    # (only conflict remains). We implement that by:
    def reshuffle_groups():
        """
        Flatten entire population, then reshuffle into m groups of approx size n
        (some might differ if total pop not exactly m*n, but typically it is).
        """
        flat = []
        for gg in range(m):
            flat.extend(population[gg])
        random.shuffle(flat)
        # Now re-split
        newpop = []
        step = len(flat)//m  # integer division
        # for simplicity assume len(flat) == m*n
        # otherwise distribute remainder as well
        idx = 0
        for gg in range(m):
            group_slice = flat[idx:idx+step]
            idx += step
            newpop.append(group_slice)
        # In case of leftover:
        left = flat[idx:]
        for i, st in enumerate(left):
            # put in random group
            newpop[random.randrange(m)].append(st)

        return newpop

    # main loop
    for step_i in range(max_steps):
        # 1) compute payoffs
        pay = compute_payoffs()

        # 2) compute fitness
        # fi = 1-w + w*g_i
        flat_list = []
        for gg in range(m):
            for ii, st in enumerate(population[gg]):
                g_i = pay[gg][ii]
                f_i = (1.0 - w) + w*g_i
                flat_list.append((gg, ii, st, f_i))

        # pick reproducer proportionally to f_i
        fitness_sum = sum([x[3] for x in flat_list])
        if fitness_sum < 1e-12:
            # no difference, pick random
            parent = random.choice(flat_list)
        else:
            r = random.random() * fitness_sum
            ssum = 0.0
            for item in flat_list:
                ssum += item[3]
                if ssum >= r:
                    parent = item
                    break

        parent_group, parent_idx, parent_str, parent_fit = parent

        # produce offspring with the same strategy
        child_str = parent_str

        # choose where the child goes
        if random.random() < lambd:
            # migrate to a random group
            target_group = random.randrange(m)
        else:
            # stay in parent's group
            target_group = parent_group

        # add child
        population[target_group].append(child_str)

        # check size of that group
        if len(population[target_group]) > n:
            # group is too big => either split or remove
            if random.random() < q:
                # split
                # partition at random:
                old_group = population[target_group]
                random.shuffle(old_group)
                half_size = len(old_group)//2
                new_group_1 = old_group[:half_size]
                new_group_2 = old_group[half_size:]
                # one new group replaces the old group
                population[target_group] = new_group_1
                # the other new group replaces a random group
                # (possibly the same if target_group is picked? the paper does that too)
                repl = random.randrange(m)
                population[repl] = new_group_2
            else:
                # remove random individual
                idx_to_remove = random.randrange(len(population[target_group]))
                del population[target_group][idx_to_remove]

        # 3) conflict step
        # we compute group payoff sums from 'pay' and do pairwise conflict
        # pay[g] is the list of payoffs for group g
        group_sums = [sum(pay[g]) for g in range(m)]
        do_conflict_step(pay)

        # 4) optionally reshuffle groups if we want to remove assortment
        if reshuffle:
            population = reshuffle_groups()

        # check for homogeneous
        winner = is_homogeneous()
        if winner is not None:
            return winner  # 'E', 'A', or 'P'

    # if no fixation happened in max_steps => return whichever is majority
    # (rare if you set max_steps large enough)
    all_strats = []
    for gg in range(m):
        all_strats.extend(population[gg])
    from collections import Counter
    ccount = Counter(all_strats)
    maj_str = ccount.most_common(1)[0][0]
    return maj_str


# -------------------------------------------------------
# Running multiple replicates + producing a plot
# Example: Fixation prob vs b/c
# -------------------------------------------------------

def experiment_vary_bc(
    bc_values = [1.1, 1.3, 1.5, 2.0, 3.0, 4.0, 5.0],
    n_reps=100,
    strategy_mut='A',
    conflict=True,
    assortment=True,
):
    """
    For each b/c, run n_reps simulations, measure how often the
    cooperator mutant takes over. Then return arrays (bc_values, fix_prob).
    If conflict=False => k=0
    If assortment=False => reshuffle=True (no splitting if m>1)
    """
    fix_probs = []
    for bc in bc_values:
        b_over_c = bc
        b = b_over_c
        c = 1.0

        successes = 0
        for r in range(n_reps):
            final_str = run_simulation(
                m=10, n=10,
                b=b, c=c,
                alpha=0.8,
                w=0.1,
                k=0.025 if conflict else 0.0,
                q=0.01 if assortment else 0.0,
                lambd=0.0,
                z=0.5,
                strategy_mut=strategy_mut,
                reshuffle= (not assortment) and conflict,
                max_steps=20000,
                seed=None  # or set a seed if you want repeatability
            )
            if final_str == strategy_mut:  # means cooperator took over
                successes += 1
        fix_prob = successes / n_reps
        fix_probs.append(fix_prob)
    return bc_values, fix_probs


def main():
    # Example usage:
    bc_vals = [1.1, 1.3, 1.5, 2.0, 3.0, 4.0, 5.0]

    # 1) Only assortment, no conflict:
    bc, fixP_A = experiment_vary_bc(
        bc_values=bc_vals,
        n_reps=200,
        strategy_mut='A',
        conflict=False,
        assortment=True
    )
    bc, fixP_P = experiment_vary_bc(
        bc_values=bc_vals,
        n_reps=200,
        strategy_mut='P',
        conflict=False,
        assortment=True
    )
    # Neutral threshold is 1/(m*n) = 1/(10*10)=0.01
    neutral_threshold = 0.01

    plt.figure(figsize=(7,5))
    plt.plot(bc, fixP_A, 'go-', label='Altruist mutant (A)')
    plt.plot(bc, fixP_P, 'ro-', label='Parochialist mutant (P)')
    plt.axhline(neutral_threshold, color='k', linestyle='--', label='Neutral fixation = 1/(m*n)')
    plt.xlabel('b/c ratio')
    plt.ylabel('Fixation probability')
    plt.title('Fixation Probability vs b/c (No Conflict, Only Assortment)')
    plt.legend()
    plt.tight_layout()
    plt.show()

    # 2) Conflict + assortment
    bc, fixP_A_conf = experiment_vary_bc(
        bc_values=bc_vals,
        n_reps=200,
        strategy_mut='A',
        conflict=True,
        assortment=True
    )
    bc, fixP_P_conf = experiment_vary_bc(
        bc_values=bc_vals,
        n_reps=200,
        strategy_mut='P',
        conflict=True,
        assortment=True
    )
    plt.figure(figsize=(7,5))
    plt.plot(bc, fixP_A_conf, 'go-', label='Altruist mutant (A) + conflict')
    plt.plot(bc, fixP_P_conf, 'ro-', label='Parochialist mutant (P) + conflict')
    plt.axhline(neutral_threshold, color='k', linestyle='--', label='Neutral fixation = 0.01')
    plt.xlabel('b/c ratio')
    plt.ylabel('Fixation probability')
    plt.title('Fixation Probability vs b/c (Conflict + Assortment)')
    plt.legend()
    plt.tight_layout()
    plt.show()

    # 3) Conflict only, no assortment:
    bc, fixP_A_confOnly = experiment_vary_bc(
        bc_values=bc_vals,
        n_reps=200,
        strategy_mut='A',
        conflict=True,
        assortment=False
    )
    bc, fixP_P_confOnly = experiment_vary_bc(
        bc_values=bc_vals,
        n_reps=200,
        strategy_mut='P',
        conflict=True,
        assortment=False
    )

    plt.figure(figsize=(7,5))
    plt.plot(bc, fixP_A_confOnly, 'g^--', label='Altruist mutant (A) conflict-only')
    plt.plot(bc, fixP_P_confOnly, 'r^--', label='Parochialist mutant (P) conflict-only')
    plt.axhline(neutral_threshold, color='k', linestyle='--', label='Neutral fixation = 0.01')
    plt.xlabel('b/c ratio')
    plt.ylabel('Fixation probability')
    plt.title('Fixation Probability vs b/c (Conflict only, no assortment)')
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
